
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import h5py
import os

st.set_page_config(page_title="Φ(n, 3) vs QDataSet", layout="centered")
st.title("📊 Φ(n, 3) Collapse Pattern vs Real Quantum Decoherence (QDataSet)")

st.markdown("""
This app compares your Φ(n, 3) digital root model to actual qubit evolution data
from the [QDataSet project](https://github.com/qdataset/qdataset).
""")

# Upload the .h5 file from QDataSet
uploaded_file = st.file_uploader("📂 Upload a QDataSet .h5 file", type="h5")

if uploaded_file:
    with st.spinner("🔍 Processing the dataset..."):
        # Load the file into memory
        with h5py.File(uploaded_file, "r") as f:
            keys = list(f.keys())
            st.success(f"Loaded dataset with {len(keys)} keys.")
            # Assume "states" key exists and use as main trace
            if "states" in keys:
                data = np.array(f["states"])
                num_timesteps = data.shape[0]
                st.write(f"Timesteps: {num_timesteps}")

                # Generate collapse pattern: norm of amplitudes
                probabilities = np.abs(data[:, 0])**2

                # Plot actual decoherence from dataset
                fig1, ax1 = plt.subplots()
                ax1.plot(probabilities, label="|0⟩ Probability")
                ax1.set_title("🧪 Real Decoherence Pattern from QDataSet")
                ax1.set_xlabel("Timestep")
                ax1.set_ylabel("Probability of |0⟩")
                ax1.grid(True)
                ax1.legend()
                st.pyplot(fig1)

                # Φ(n, 3) model
                st.subheader("📐 Φ(n, 3) Predicted Collapse Points")

                def digital_root(n):
                    return 9 if n % 9 == 0 and n != 0 else n % 9

                k = 3
                n_values = np.arange(num_timesteps)
                digital_roots = [digital_root(k * (2 ** n)) for n in n_values]
                is_vibrating = [(val == 3 or val == 6) for val in digital_roots]

                fig2, ax2 = plt.subplots(figsize=(10, 4))
                ax2.plot(n_values, digital_roots, marker='o', label="Φ(n, 3)", color='blue')
                ax2.axhline(3, color='gray', linestyle='--', alpha=0.6)
                ax2.axhline(6, color='gray', linestyle='--', alpha=0.6)
                for n, v in enumerate(is_vibrating):
                    if not v:
                        ax2.axvline(n, color='orange', alpha=0.2)
                ax2.set_title("Φ(n, 3) Predicted Collapse Pattern")
                ax2.set_xlabel("Timestep")
                ax2.set_ylabel("Digital Root")
                ax2.grid(True)
                ax2.legend()
                st.pyplot(fig2)

                st.success("✅ Done! Compare actual vs predicted decoherence.")
            else:
                st.error("No 'states' key found in uploaded file. Please try a different QDataSet file.")
else:
    st.info("Upload a `.h5` file from QDataSet to begin.")
