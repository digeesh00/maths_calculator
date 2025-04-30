import streamlit as st
from scipy.stats import f_oneway
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

st.title("One-Way ANOVA Calculator")

st.markdown("""
This app performs **One-Way ANOVA (Analysis of Variance)** to test if there are significant differences among group means.
""")

group_data = {}
group_count = st.number_input("Number of groups:", min_value=2, max_value=10, step=1)

for i in range(1, group_count + 1):
    data_str = st.text_input(f"Group {i} values (comma-separated):", key=f"group_{i}")
    try:
        data = [float(x.strip()) for x in data_str.split(",") if x.strip()]
        group_data[f"Group {i}"] = data
    except:
        st.warning(f"Invalid input in Group {i}.")

alpha = st.number_input("Significance level α:", min_value=0.001, max_value=0.10, value=0.05, step=0.001)

if st.button("Run ANOVA"):
    if len(group_data) >= 2 and all(len(v) > 1 for v in group_data.values()):
        try:
            f_stat, p_value = f_oneway(*group_data.values())

            st.markdown("### 🧮 ANOVA Results")
            st.write(f"**F Statistic:** {f_stat:.4f}")
            st.write(f"**p-value:** {p_value:.4f}")
            st.write(f"**Significance Level (α):** {alpha}")

            if p_value < alpha:
                st.success("Reject the null hypothesis: At least one group mean is significantly different.")
            else:
                st.info("Fail to reject the null hypothesis: No significant difference among group means.")

            # Optional boxplot visualization
            st.markdown("### 📊 Group Distributions")
            all_data = []
            for grp, values in group_data.items():
                for val in values:
                    all_data.append((grp, val))

            df_plot = pd.DataFrame(all_data, columns=["Group", "Value"])
            plt.figure(figsize=(8, 4))
            sns.boxplot(x="Group", y="Value", data=df_plot, palette="Set2")
            st.pyplot(plt.gcf())
        except Exception as e:
            st.error(f"Error running ANOVA: {e}")
    else:
        st.error("Each group must have at least 2 values.")
