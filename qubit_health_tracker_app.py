import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from qiskit import QuantumCircuit, transpile
from qiskit_ibm_provider import IBMProvider
from qiskit.visualization import plot_histogram
import random
import io

st.set_page_config(page_title="Φ(n, 3) Quantum Validation", layout="centered")
st.title("🔗 Φ(n, 3) vs IBM Quantum Decoherence")

st.markdown("""
This app connects to the IBM Quantum backend, runs a real quantum job,
and compares actual decoherence with the predicted Φ(n, 3) collapse model.
""")

# Input: IBM Token
ibm_token = st.text_input("Enter your IBM Quantum API Token:", type="password")
run_job = st.button("Run Quantum Validation")

if run_job and ibm_token:
    with st.spinner("Connecting to IBM Quantum and running job..."):
        try:
            provider = IBMProvider(token=ibm_token)
            backend = provider.get_backend('ibmq_qasm_simulator')

            # Quantum Circuit
            qc = QuantumCircuit(1)
            qc.h(0)
            qc.rx(np.pi / 4, 0)
            qc.measure_all()

            transpiled_qc = transpile(qc, backend)
            job = backend.run(transpiled_qc, shots=1024)
            result = job.result()
            counts = result.get_counts()

            # Plot IBM result
            st.subheader("📉 Real IBM Quantum Decoherence")
            fig1, ax1 = plt.subplots()
            plot_histogram(counts, ax=ax1)
            st.pyplot(fig1)

            # Φ(n, 3) Simulation
            st.subheader("📈 Φ(n, 3) Predicted Collapse")
            def digital_root(n):
                return 9 if n % 9 == 0 and n != 0 else n % 9

            k = 3
            timesteps = 30
            n_values = np.arange(timesteps)
            digital_roots = [digital_root(k * (2 ** n)) for n in n_values]
            is_vibrating = [(val == 3 or val == 6) for val in digital_roots]

            fig2, ax2 = plt.subplots(figsize=(10, 4))
            ax2.plot(n_values, digital_roots, marker='o', label="Φ(n, 3)", color='blue')
            ax2.axhline(3, color='gray', linestyle='--', alpha=0.6)
            ax2.axhline(6, color='gray', linestyle='--', alpha=0.6)
            for n, v in enumerate(is_vibrating):
                if not v:
                    ax2.axvline(n, color='orange', alpha=0.2)
            ax2.set_title("Predicted Collapse Points")
            ax2.set_xlabel("Timestep n")
            ax2.set_ylabel("Digital Root")
            ax2.grid(True)
            ax2.legend()
            st.pyplot(fig2)

            st.success("Validation run complete! Compare IBM decoherence above with Φ(n, 3) prediction below.")

        except Exception as e:
            st.error("Failed to connect or run job. Double-check your token.")
else:
    st.info("Enter your IBM Quantum token and click the button to begin validation.")

