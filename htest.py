import streamlit as st
import pandas as pd
import numpy as np
from scipy.stats import kruskal, rankdata, chi2
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Kruskal-Wallis H Test (Rank Sum Test) - Educational Calculator")

st.markdown("""
This app follows the procedure outlined in your academic reference for **Kruskal-Wallis H-Test**:
- Non-parametric test for comparing multiple independent groups.
- Uses **ranks** instead of raw data.
""")

group_data = {}
group_count = st.number_input("How many groups?", min_value=2, max_value=10, step=1)

for i in range(1, group_count + 1):
    data_str = st.text_input(f"Enter values for Group {i} (comma-separated):", key=f"group_{i}")
    try:
        data = [float(x.strip()) for x in data_str.split(",") if x.strip()]
        group_data[f"Group {i}"] = data
    except:
        st.warning(f"Invalid input in Group {i}.")

alpha = st.number_input("Enter significance level α (e.g., 0.05):", value=0.05, step=0.01)

if st.button("Run H-Test"):
    if len(group_data) >= 2 and all(len(v) > 0 for v in group_data.values()):
        # Combine all data with group labels
        all_values = []
        group_labels = []
        for group_name, values in group_data.items():
            all_values.extend(values)
            group_labels.extend([group_name] * len(values))
        
        df = pd.DataFrame({"Group": group_labels, "Value": all_values})
        df["Rank"] = rankdata(df["Value"])

        # Calculate group-level rank sums and H statistic
        rank_sums = df.groupby("Group")["Rank"].sum()
        ni = df["Group"].value_counts()
        N = len(df)
        H = (12 / (N * (N + 1))) * sum((rank_sums**2) / ni) - 3 * (N + 1)
        df_degree = group_count - 1
        chi_critical = chi2.ppf(1 - alpha, df_degree)

        # Perform scipy Kruskal for verification
        h_scipy, p_value = kruskal(*group_data.values())

        st.markdown("### 🧮 Step-by-Step Results")
        st.write("**Data Table with Ranks:**")
        st.dataframe(df)

        st.write("**Sum of Ranks for each Group:**")
        st.dataframe(rank_sums)

        st.write(f"**Calculated H:** {H:.4f}")
        st.write(f"**Chi-Square Critical Value (df={df_degree}, α={alpha}):** {chi_critical:.4f}")
        st.write(f"**p-value (Scipy check):** {p_value:.4f}")

        if H > chi_critical:
            st.success("Result: Reject the Null Hypothesis — Significant differences between groups exist.")
        else:
            st.info("Result: Fail to Reject the Null Hypothesis — No significant difference found.")

        # Boxplot
        st.markdown("### 📊 Group Value Distribution")
        plt.figure(figsize=(8, 4))
        sns.boxplot(x="Group", y="Value", data=df, palette="Set2")
        st.pyplot(plt.gcf())
    else:
        st.error("Please input valid data for all groups.")
