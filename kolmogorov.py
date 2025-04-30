import streamlit as st
from scipy.stats import kstest, norm, uniform, expon
import numpy as np
import pandas as pd

st.title("Kolmogorov–Smirnov Test (1-Sample)")
st.write("This app performs a 1-sample K-S test comparing your sample data to a theoretical distribution.")

# Input data
sample_input = st.text_area("Enter sample data (comma-separated)", "2.1, 2.5, 3.0, 3.2, 4.0, 4.1, 4.3, 5.0, 5.1")

# Choose distribution
dist_name = st.selectbox("Select theoretical distribution", ["Normal", "Uniform", "Exponential"])

# Run test
if st.button("Run K-S Test"):
    try:
        sample = np.array(list(map(float, sample_input.strip().split(","))))
        sample = np.sort(sample)

        # Select distribution
        if dist_name == "Normal":
            loc, scale = np.mean(sample), np.std(sample, ddof=1)
            dist = norm(loc=loc, scale=scale)
            dist_func = "norm"
            params = (loc, scale)
        elif dist_name == "Uniform":
            loc, scale = np.min(sample), np.max(sample) - np.min(sample)
            dist = uniform(loc=loc, scale=scale)
            dist_func = "uniform"
            params = (loc, scale)
        elif dist_name == "Exponential":
            loc, scale = 0, np.mean(sample)
            dist = expon(loc=loc, scale=scale)
            dist_func = "expon"
            params = (loc, scale)

        # Calculate ECDF
        ecdf_y = np.arange(1, len(sample)+1) / len(sample)
        cdf_y = dist.cdf(sample)
        d_stat = np.max(np.abs(ecdf_y - cdf_y))

        df = pd.DataFrame({
            "Sample": sample,
            "ECDF": ecdf_y,
            "Theoretical CDF": cdf_y,
            "|ECDF - CDF|": np.abs(ecdf_y - cdf_y)
        })

        st.markdown("### 📊 Step-by-Step Calculation")
        st.dataframe(df)

        st.markdown("### 🧮 D-statistic")
        st.write(f"**D = {d_stat:.4f}**")

        # Run K-S test
        ks_stat, p_value = kstest(sample, dist_func, args=params)

        st.markdown("### 🧪 Kolmogorov–Smirnov Test Result")
        st.write(f"**Test Statistic (D):** {ks_stat:.4f}")
        st.write(f"**P-value:** {p_value:.4f}")

        alpha = 0.05
        if p_value < alpha:
            st.error("Reject the null hypothesis: Data does not follow the specified distribution.")
        else:
            st.success("Fail to reject the null hypothesis: Data may follow the specified distribution.")

    except Exception as e:
        st.error(f"Error: {str(e)}")
