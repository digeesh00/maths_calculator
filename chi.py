import streamlit as st
import numpy as np
from scipy.stats import chi2

st.title("Chi-Square Goodness of Fit Calculator")

st.markdown("""
This calculator performs the **Chi-Square Goodness of Fit Test**.
Enter the **observed** and **expected** (estimated) frequencies to check if the observed distribution differs significantly from the expected.
""")

observed_input = st.text_area("Enter Observed Frequencies (comma-separated):", placeholder="e.g., 20, 30, 25, 25")
expected_input = st.text_area("Enter Expected Frequencies (comma-separated):", placeholder="e.g., 25, 25, 25, 25")

alpha = st.number_input("Significance Level (α):", min_value=0.001, max_value=0.10, value=0.05, step=0.001)

if st.button("Calculate Chi-Square"):
    try:
        observed = [float(x.strip()) for x in observed_input.split(",") if x.strip()]
        expected = [float(x.strip()) for x in expected_input.split(",") if x.strip()]

        if len(observed) != len(expected):
            st.error("Observed and expected frequencies must have the same number of values.")
        elif any(e == 0 for e in expected):
            st.error("Expected frequencies cannot be zero.")
        else:
            observed = np.array(observed)
            expected = np.array(expected)

            chi_stat = np.sum((observed - expected)**2 / expected)
            df = len(observed) - 1
            p_value = 1 - chi2.cdf(chi_stat, df)
            critical_val = chi2.ppf(1 - alpha, df)

            st.markdown("### 🧮 Chi-Square Test Results")
            st.write(f"**Chi-Square Statistic:** {chi_stat:.4f}")
            st.write(f"**Degrees of Freedom:** {df}")
            st.write(f"**Chi-Square Critical Value (α={alpha}):** {critical_val:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")

            if chi_stat > critical_val:
                st.success("Reject the null hypothesis: Observed data significantly differs from expected.")
            else:
                st.info("Fail to reject the null hypothesis: No significant difference between observed and expected.")
    except Exception as e:
        st.error(f"Error in processing input: {e}")
