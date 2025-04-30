import streamlit as st
from scipy.stats import rankdata, wilcoxon
import pandas as pd
import numpy as np

st.title("Wilcoxon Signed Rank Test (with Rank Calculations)")
st.write("Enter paired data (Before and After) to perform the Wilcoxon Signed Rank Test.")

# Input
sample1 = st.text_area("Enter *Before* data (comma-separated)", "65,75,66,80,70,85,60,68,72,77")
sample2 = st.text_area("Enter *After* data (comma-separated)", "70,78,64,85,74,85,58,70,74,79")

if st.button("Run Test"):
    try:
        before = list(map(float, sample1.strip().split(",")))
        after = list(map(float, sample2.strip().split(",")))

        if len(before) != len(after):
            st.error("❌ Error: The number of values in both samples must be the same.")
        else:
            # Calculate differences
            diff = [a - b for a, b in zip(after, before)]
            abs_diff = [abs(d) for d in diff]

            # Remove zero differences
            data = [(b, a, d, abs(d)) for b, a, d in zip(before, after, diff) if d != 0]
            if not data:
                st.error("All differences are zero. Cannot perform test.")
            else:
                df = pd.DataFrame(data, columns=["Before", "After", "Difference", "Abs_Diff"])
                df["Rank"] = rankdata(df["Abs_Diff"])
                df["Sign"] = df["Difference"].apply(lambda x: "+" if x > 0 else "-")
                df["Signed Rank"] = df.apply(lambda row: row["Rank"] if row["Sign"] == "+" else -row["Rank"], axis=1)

                st.markdown("### 📊 Calculated Data Table")
                st.dataframe(df)

                W_pos = df[df["Sign"] == "+"]["Rank"].sum()
                W_neg = df[df["Sign"] == "-"]["Rank"].sum()
                test_stat = min(W_pos, W_neg)

                st.markdown("### 🧮 Rank Sums")
                st.write(f"**W⁺ (Sum of positive ranks):** {W_pos}")
                st.write(f"**W⁻ (Sum of negative ranks):** {W_neg}")
                st.write(f"**Test Statistic (smaller of W⁺ or W⁻):** {test_stat}")

                # Perform actual Wilcoxon test (ignores zero diffs)
                valid_before = [b for b, a, d in zip(before, after, diff) if d != 0]
                valid_after = [a for b, a, d in zip(before, after, diff) if d != 0]
                stat, p = wilcoxon(valid_after, valid_before)

                st.markdown("### 🧪 Wilcoxon Signed Rank Test Result")
                st.write(f"**Scipy Test Statistic:** {stat}")
                st.write(f"**P-value:** {p:.4f}")

                alpha = 0.05
                if p < alpha:
                    st.error("Reject the null hypothesis: Significant difference detected.")
                else:
                    st.success("Fail to reject the null hypothesis: No significant difference.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
