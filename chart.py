import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("📊 Statistical Control Chart Dashboard")

chart_type = st.selectbox(
    "Select Chart Type",
    ("X̄-R Chart", "X̄-S Chart", "C Chart", "P/NP Chart")
)

alpha_constants = {
    2: (1.88, 1.88),
    3: (1.023, 0.729),
    4: (0.729, 0.577),
    5: (0.577, 0.483),
    6: (0.483, 0.419),
    7: (0.419, 0.373),
    8: (0.373, 0.337),
    9: (0.337, 0.308),
    10: (0.308, 0.285)
}

st.markdown("### 📥 Input Sample Data")
data_input = st.text_area("Enter your data as rows (comma-separated values per subgroup/sample):", 
                          placeholder="e.g.\n5,6,7\n6,5,7\n7,8,6")

alpha = st.number_input("Significance Level (used for 3σ limits)", value=0.0027)

def plot_chart(y_values, ucl, lcl, cl, title):
    fig, ax = plt.subplots()
    ax.plot(y_values, marker='o', linestyle='-', label="Value")
    ax.axhline(cl, color='green', linestyle='--', label="CL")
    ax.axhline(ucl, color='red', linestyle='--', label="UCL")
    ax.axhline(lcl, color='red', linestyle='--', label="LCL")
    ax.set_title(title)
    ax.set_xlabel("Sample")
    ax.set_ylabel("Measured Value")
    ax.legend()
    st.pyplot(fig)

if st.button("Generate Chart"):
    try:
        rows = data_input.strip().split('\n')
        data = [list(map(float, row.strip().split(','))) for row in rows]
        df = pd.DataFrame(data)
        subgroup_size = df.shape[1]
        num_subgroups = df.shape[0]

        if chart_type == "X̄-R Chart":
            st.header("📈 X̄-R Control Chart")
            x_bar = df.mean(axis=1)
            r_bar = df.max(axis=1) - df.min(axis=1)
            X̄̄ = x_bar.mean()
            R̄ = r_bar.mean()
            A2 = alpha_constants.get(subgroup_size, (0, 0))[0]
            UCL = X̄̄ + A2 * R̄
            LCL = X̄̄ - A2 * R̄

            st.write(f"CL (X̄̄): {X̄̄:.2f}")
            st.write(f"UCL: {UCL:.2f}")
            st.write(f"LCL: {LCL:.2f}")
            plot_chart(x_bar, UCL, LCL, X̄̄, "X̄ Chart")

            # R chart
            D4 = 3.267  # max for n=2
            D3 = 0
            R_UCL = D4 * R̄
            R_LCL = D3 * R̄
            plot_chart(r_bar, R_UCL, R_LCL, R̄, "R Chart")

        elif chart_type == "X̄-S Chart":
            st.header("📈 X̄-S Control Chart")
            x_bar = df.mean(axis=1)
            s = df.std(axis=1, ddof=1)
            X̄̄ = x_bar.mean()
            S̄ = s.mean()
            A3 = 1.023  # for n=3
            UCL = X̄̄ + A3 * S̄
            LCL = X̄̄ - A3 * S̄

            st.write(f"CL (X̄̄): {X̄̄:.2f}")
            st.write(f"UCL: {UCL:.2f}")
            st.write(f"LCL: {LCL:.2f}")
            plot_chart(x_bar, UCL, LCL, X̄̄, "X̄ Chart")

            B3 = 0  # for n=3
            B4 = 2.568
            S_UCL = B4 * S̄
            S_LCL = B3 * S̄
            plot_chart(s, S_UCL, S_LCL, S̄, "S Chart")

        elif chart_type == "C Chart":
            st.header("📈 C Chart")
            counts = [sum(map(float, row.strip().split(','))) for row in rows]
            C̄ = np.mean(counts)
            UCL = C̄ + 3 * np.sqrt(C̄)
            LCL = C̄ - 3 * np.sqrt(C̄)

            st.write(f"CL (C̄): {C̄:.2f}")
            st.write(f"UCL: {UCL:.2f}")
            st.write(f"LCL: {max(LCL, 0):.2f}")
            plot_chart(counts, UCL, max(LCL, 0), C̄, "C Chart")

        elif chart_type == "P/NP Chart":
            st.header("📈 P / NP Chart")
            defectives = []
            n_values = []
            for row in rows:
                parts = list(map(float, row.strip().split(',')))
                defectives.append(parts[0])
                n_values.append(parts[1])
            p_vals = np.array(defectives) / np.array(n_values)
            p̄ = np.mean(p_vals)
            n̄ = np.mean(n_values)
            UCL = p̄ + 3 * np.sqrt(p̄ * (1 - p̄) / n̄)
            LCL = p̄ - 3 * np.sqrt(p̄ * (1 - p̄) / n̄)

            st.write(f"CL (p̄): {p̄:.4f}")
            st.write(f"UCL: {UCL:.4f}")
            st.write(f"LCL: {max(LCL, 0):.4f}")
            plot_chart(p_vals, UCL, max(LCL, 0), p̄, "P Chart")

    except Exception as e:
        st.error(f"Error: {e}")
