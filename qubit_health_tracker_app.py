
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import random

# Set page config
st.set_page_config(page_title="Qubit Health Tracker", layout="centered")
st.title("Φ(n, 3) Qubit Health Prediction App")

st.markdown("""
This app simulates quantum decoherence using your custom Φ(n, 3) digital root pattern.
It tracks qubit vibration states and outputs health scores.
""")

# User inputs
num_qubits = st.slider("Select number of qubits:", 1, 10, 5)
timesteps = st.slider("Select number of timesteps:", 10, 200, 100)
decohere_chance = st.slider("Decoherence chance per step (0.0 - 1.0):", 0.0, 0.2, 0.03)

# Digital root function
def digital_root(n):
    return 9 if n % 9 == 0 and n != 0 else n % 9

# Simulation
qubit_data = []
health_score = []
k = 3

for q in range(num_qubits):
    form_count = 0
    current_k = k
    sequence = []

    for t in range(timesteps):
        if random.random() < decohere_chance:
            current_k = random.choice([2, 4, 5, 7])
        val = digital_root(current_k * (2 ** t))
        is_form = val in [3, 6]
        form_count += is_form
        sequence.append({
            'Qubit': f'Qubit {q+1}',
            'Timestep': t,
            'DigitalRoot': val,
            'FormState': is_form,
            'State': 'Quantum' if current_k == 3 else 'Classical'
        })

    qubit_data.extend(sequence)
    health_score.append({
        'Qubit': f'Qubit {q+1}',
        'Health Score (%)': round((form_count / timesteps) * 100, 2)
    })

# DataFrames
df_health = pd.DataFrame(health_score)
df_vibration = pd.DataFrame(qubit_data)

# Plot
tab1, tab2 = st.tabs(["Digital Root Graph", "Health Scores"])

with tab1:
    st.subheader("Φ(n, 3) Digital Root Pattern")
    fig, ax = plt.subplots(figsize=(10, 5))
    for q in df_vibration['Qubit'].unique():
        subset = df_vibration[df_vibration['Qubit'] == q]
        ax.plot(subset['Timestep'], subset['DigitalRoot'], label=q)
        decohere_points = subset[subset['State'] == 'Classical']['Timestep']
        for d in decohere_points:
            ax.axvline(x=d, color='red', alpha=0.1)
    ax.axhline(3, color='gray', linestyle='--', alpha=0.5)
    ax.axhline(6, color='gray', linestyle='--', alpha=0.5)
    ax.set_xlabel("Timestep")
    ax.set_ylabel("Digital Root")
    ax.set_title("Simulated Qubit Decoherence using Φ(n, 3)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

with tab2:
    st.subheader("Qubit Health Score Table")
    st.dataframe(df_health, use_container_width=True)

# Export button
csv = df_health.to_csv(index=False).encode('utf-8')
st.download_button("Download Health Scores as CSV", csv, "health_scores.csv", "text/csv")
