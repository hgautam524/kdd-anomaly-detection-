import streamlit as st
import requests
import pandas as pd
import numpy as np
import altair as alt

# --- CONFIGURATION ---
API_URL = "http://localhost:5000"  # Change if your backend runs elsewhere

# --- SESSION STATE FOR LOGIN ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# --- USER AUTH (simple demo, not secure) ---
USERS = {"admin": "admin123", "user": "user123"}

def login_page():
    st.title("🔒 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Logged in!")
            st.rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# --- SIDEBAR NAVIGATION ---
def sidebar():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio(
        "Go to",
        ("Home", "Predict", "Data Visualization", "About"),
        key="nav"
    )
    st.sidebar.markdown("---")
    st.sidebar.write(f"Logged in as: `{st.session_state.username}`")
    st.sidebar.button("Logout", on_click=logout)
    return page

# --- HOME PAGE ---
def home():
    st.title("🏠 Anomaly Detection Dashboard")
    st.markdown("""
    Welcome to the Anomaly Detection App!  
    - Use the **Predict** page to detect anomalies in network traffic.
    - Use **Data Visualization** to explore the dataset.
    - Navigate using the sidebar.
    """)

# --- PREDICTION PAGE ---
def predict():
    st.title("🔎 Predict Anomaly")
    st.write("Enter feature values for prediction:")

    # Categorical options
    protocol_types = ["tcp", "udp", "icmp"]
    services = ["http", "smtp", "ftp", "domain_u", "eco_i", "other"]
    flags = ["SF", "S0", "REJ", "RSTR", "SH", "S1", "S2", "S3", "OTH"]

    features = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
        "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
        "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login",
        "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
        "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate"
    ]

    with st.form("predict_form"):
        input_data = {}
        for col in features:
            if col == "protocol_type":
                input_data[col] = st.selectbox(col, protocol_types)
            elif col == "service":
                input_data[col] = st.selectbox(col, services)
            elif col == "flag":
                input_data[col] = st.selectbox(col, flags)
            else:
                input_data[col] = st.text_input(col, "0")
        submitted = st.form_submit_button("Detect Anomaly")
        if submitted:
            for k in input_data:
                if k not in ["protocol_type", "service", "flag"]:
                    try:
                        input_data[k] = float(input_data[k])
                    except ValueError:
                        pass
            try:
                response = requests.post(f"{API_URL}/predict", json=input_data)
                if response.ok:
                    result = response.json()
                    st.success("Prediction Results:")
                    st.write("Isolation Forest: ", "🚨 Anomaly" if result["isolation_forest"] else "✅ Normal")
                    st.write("Autoencoder: ", "🚨 Anomaly" if result["autoencoder"] else "✅ Normal")
                    st.write("Reconstruction Error (Autoencoder): ", result["mse"])
                else:
                    st.error("Prediction failed: " + response.text)
            except Exception as e:
                st.error(f"Error connecting to backend: {e}")

# --- DATA VISUALIZATION PAGE ---
import os

def data_visualization():
    st.title("📊 Data Visualization")

    # --- File Uploader ---
    st.subheader("Upload KDD Dataset")
    uploaded_file = st.file_uploader("Choose a CSV file", type=["csv"])
    
    # Column names from KDD Cup 1999 dataset
    column_names = [
        "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes", "land", "wrong_fragment", "urgent",
        "hot", "num_failed_logins", "logged_in", "num_compromised", "root_shell", "su_attempted", "num_root",
        "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds", "is_host_login", "is_guest_login",
        "count", "srv_count", "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate", "same_srv_rate",
        "diff_srv_rate", "srv_diff_host_rate", "dst_host_count", "dst_host_srv_count", "dst_host_same_srv_rate",
        "dst_host_diff_srv_rate", "dst_host_same_src_port_rate", "dst_host_srv_diff_host_rate",
        "dst_host_serror_rate", "dst_host_srv_serror_rate", "dst_host_rerror_rate", "dst_host_srv_rerror_rate",
        "label"
    ]

    try:
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file, names=column_names, nrows=5000)
        else:
            # Use default local path if no upload
            data_path = r"C:\Users\Admin\kdd-anomaly-detection-\data\kddcup.data_10_percent"
            df = pd.read_csv(data_path, names=column_names, nrows=5000)
            st.info(f"Using default data file at: `{data_path}`")

    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        return

    # --- Label Filter ---
    st.subheader("Filter by Label")
    label_options = ["All"] + sorted(df["label"].unique())
    selected_label = st.selectbox("Select label to filter", label_options)

    if selected_label != "All":
        df = df[df["label"] == selected_label]

    st.write("### Data Sample")
    st.dataframe(df.head(20))

    st.write("### Chart Options")
    chart_type = st.selectbox("Chart Type", ["Histogram", "Boxplot", "Scatter"])
    columns = df.columns.tolist()

    if chart_type == "Histogram":
        col = st.selectbox("Feature", columns, key="hist_col")
        hist = alt.Chart(df).mark_bar().encode(
            alt.X(col, bin=alt.Bin(maxbins=30), title=col),
            y='count()'
        ).properties(width=500, height=300)
        st.altair_chart(hist, use_container_width=True)

    elif chart_type == "Boxplot":
        col = st.selectbox("Feature", columns, key="box_col")
        box = alt.Chart(df).mark_boxplot().encode(
            y=alt.Y(col, title=col)
        ).properties(width=400, height=300)
        st.altair_chart(box, use_container_width=True)

    elif chart_type == "Scatter":
        x = st.selectbox("X-axis", columns, index=0, key="scatter_x")
        y = st.selectbox("Y-axis", columns, index=1, key="scatter_y")
        scatter = alt.Chart(df).mark_circle(size=60, opacity=0.6).encode(
            x=alt.X(x, title=x),
            y=alt.Y(y, title=y),
            color=alt.Color("label:N") if "label" in df.columns else alt.value("steelblue"),
            tooltip=[x, y, "label"] if "label" in df.columns else [x, y]
        ).properties(width=500, height=300)
        st.altair_chart(scatter, use_container_width=True)

    st.write("### Label Distribution")
    if "label" in df.columns:
        label_count = df["label"].value_counts().reset_index()
        label_count.columns = ["label", "count"]
        label_bar = alt.Chart(label_count).mark_bar().encode(
            x=alt.X("label:N", title="Label"),
            y=alt.Y("count:Q", title="Count")
        ).properties(width=400, height=300)
        st.altair_chart(label_bar, use_container_width=True)

# --- ABOUT PAGE ---
def about():
    st.title("ℹ️ About")
    st.markdown("""
    **Anomaly Detection in Network Traffic**  
    - This app provides a user-friendly interface for detecting anomalies in network traffic data using machine learning models.
    - Detects anomalies in network traffic using Isolation Forest and Autoencoder models  
    - Visualize and explore the KDD dataset  
    - Demo login: `admin` / `admin123` or `user` / `user123`
    """)

# --- MAIN APP LOGIC ---
def main():
    if not st.session_state.logged_in:
        login_page()
        return

    page = sidebar()
    if page == "Home":
        home()
    elif page == "Predict":
        predict()
    elif page == "Data Visualization":
        data_visualization()
    elif page == "About":
        about()

if __name__ == "__main__":
    main()
