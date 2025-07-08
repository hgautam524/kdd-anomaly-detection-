import streamlit as st
import requests
import pandas as pd

st.title("KDD Cup Anomaly Detection")

with st.form("predict_form"):
    st.write("Enter feature values for prediction:")
    input_data = {}
    # You may want to dynamically create fields for all KDD features except 'label'
    for col in [
        "duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent",
        "hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
        "num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
        "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
        "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
        "dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
        "dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate"
    ]:
        input_data[col] = st.text_input(col, "0")
    submitted = st.form_submit_button("Detect Anomaly")
    if submitted:
        # Convert inputs to correct types if needed (int/float)
        for k in input_data:
            try:
                input_data[k] = float(input_data[k])
            except ValueError:
                pass
        response = requests.post("http://localhost:5000/predict", json=input_data)
        if response.ok:
            result = response.json()
            st.write("Isolation Forest: ", "Anomaly" if result["isolation_forest"] else "Normal")
            st.write("Autoencoder: ", "Anomaly" if result["autoencoder"] else "Normal")
            st.write("Reconstruction Error (Autoencoder): ", result["mse"])
        else:
            st.write("Prediction failed:", response.text)