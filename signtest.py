import streamlit as st
import pandas as pd
from scipy.stats import binomtest, ttest_1samp

st.title("Sign Test Calculator (Paired & Unpaired Samples)")

st.markdown("""
This calculator compares **paired data** or **unpaired data** (Before vs After or Sample vs Mean) using the non-parametric **Sign Test** (for paired samples) and **One-Sample t-test** (for unpaired samples).
""")

st.markdown("### 📥 Enter Your Data")

# Radio button to switch between paired and unpaired test
test_type = st.radio("Select Test Type:", ("Paired Test", "Unpaired Test"))

if test_type == "Paired Test":
    col1, col2 = st.columns(2)

    with col1:
        before_input = st.text_area("Enter 'Before' values (comma-separated):", placeholder="e.g., 23, 45, 30, 41")

    with col2:
        after_input = st.text_area("Enter 'After' values (comma-separated):", placeholder="e.g., 25, 40, 29, 44")

    alpha = st.number_input("Significance level α:", min_value=0.001, max_value=0.10, value=0.05, step=0.001)

    if st.button("Run Sign Test"):
        try:
            before_vals = [float(x.strip()) for x in before_input.split(",") if x.strip()]
            after_vals = [float(x.strip()) for x in after_input.split(",") if x.strip()]

            if len(before_vals) != len(after_vals):
                st.error("The number of 'Before' and 'After' values must be the same.")
            elif len(before_vals) == 0:
                st.warning("Please enter valid data in both fields.")
            else:
                # Build DataFrame
                df = pd.DataFrame({"Before": before_vals, "After": after_vals})
                df["Difference"] = df["After"] - df["Before"]
                df["Sign"] = df["Difference"].apply(lambda x: "+" if x > 0 else ("−" if x < 0 else "0"))

                n_pos = sum(df["Sign"] == "+")
                n_neg = sum(df["Sign"] == "−")
                n_effective = n_pos + n_neg

                st.markdown("### 🧮 Step-by-Step Output")
                st.dataframe(df)

                st.write(f"**Positive Signs (+):** {n_pos}")
                st.write(f"**Negative Signs (−):** {n_neg}")
                st.write(f"**Ties (0):** {sum(df['Sign'] == '0')}")
                st.write(f"**Effective Sample Size (excluding ties):** {n_effective}")

                if n_effective == 0:
                    st.warning("All differences are 0 (ties). Cannot perform test.")
                else:
                    p_value = binomtest(min(n_pos, n_neg), n=n_effective, p=0.5, alternative="two-sided").pvalue
                    st.write(f"**Binomial Test p-value:** {p_value:.4f}")

                    if p_value < alpha:
                        st.success("Reject the null hypothesis: There is a significant median difference.")
                    else:
                        st.info("Fail to reject the null hypothesis: No significant median difference found.")

        except Exception as e:
            st.error(f"Error parsing input: {e}")

elif test_type == "Unpaired Test":
    col1, col2 = st.columns(2)

    with col1:
        sample_input = st.text_area("Enter sample values (comma-separated):", placeholder="e.g., 23, 45, 30, 41")

    with col2:
        mean_value = st.number_input("Enter the mean value for comparison:", value=0.0)

    alpha = st.number_input("Significance level α:", min_value=0.001, max_value=0.10, value=0.05, step=0.001)

    if st.button("Run One-Sample t-test"):
        try:
            sample_vals = [float(x.strip()) for x in sample_input.split(",") if x.strip()]

            if len(sample_vals) == 0:
                st.warning("Please enter valid data.")
            else:
                # Perform One-Sample t-test
                t_stat, p_value = ttest_1samp(sample_vals, mean_value)

                st.markdown("### 🧮 Step-by-Step Output")
                st.write(f"**Sample Data:** {sample_vals}")
                st.write(f"**Mean Value for Comparison:** {mean_value}")
                st.write(f"**T-Statistic:** {t_stat:.4f}")
                st.write(f"**p-value:** {p_value:.4f}")

                if p_value < alpha:
                    st.success("Reject the null hypothesis: The sample mean is significantly different from the specified mean.")
                else:
                    st.info("Fail to reject the null hypothesis: The sample mean is not significantly different from the specified mean.")

        except Exception as e:
            st.error(f"Error parsing input: {e}")
