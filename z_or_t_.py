import streamlit as st
from scipy.stats import norm, t
import math

st.title("Z-Test / T-Test Calculator (Auto Classifier)")

st.markdown("""
This tool automatically selects:
- **Z-Test** when sample size **n ≥ 30**
- **T-Test** when sample size **n < 30**

Performs a two-tailed test to compare the sample mean against a known population mean.
""")

# Inputs
n = st.number_input("Sample size (n):", min_value=1)
sample_mean = st.number_input("Sample mean (x̄):")
pop_mean = st.number_input("Population mean (μ):")
std_dev = st.number_input("Standard deviation (σ or s):", min_value=0.0001)
alpha = st.number_input("Significance level (α):", min_value=0.001, max_value=0.10, value=0.05, step=0.001)

if st.button("Run Test"):
    se = std_dev / math.sqrt(n)  # standard error
    test_stat = (sample_mean - pop_mean) / se

    if n >= 30:
        # Z-test
        p_value = 2 * (1 - norm.cdf(abs(test_stat)))
        critical = norm.ppf(1 - alpha / 2)

        st.markdown("### ✅ Z-Test Results (Large Sample)")
        st.write(f"**Z Statistic:** {test_stat:.4f}")
        st.write(f"**p-value:** {p_value:.4f}")
        st.write(f"**Z Critical Value (α = {alpha}):** ±{critical:.4f}")

    else:
        # T-test
        df = n - 1
        p_value = 2 * (1 - t.cdf(abs(test_stat), df))
        critical = t.ppf(1 - alpha / 2, df)

        st.markdown("### ✅ T-Test Results (Small Sample)")
        st.write(f"**T Statistic:** {test_stat:.4f}")
        st.write(f"**Degrees of Freedom:** {df}")
        st.write(f"**p-value:** {p_value:.4f}")
        st.write(f"**T Critical Value (α = {alpha}):** ±{critical:.4f}")

    # Decision
    if abs(test_stat) > critical:
        st.success("Reject the null hypothesis: Significant difference exists.")
    else:
        st.info("Fail to reject the null hypothesis: No significant difference found.")
