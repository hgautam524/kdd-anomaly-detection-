# filepath: c:\Users\Admin\kdd-anomaly-detection-\app\main.py
from flask import Flask, jsonify, request
import pandas as pd

app = Flask(__name__)

# ...existing code...

@app.route("/data")
def data():
    sample = int(request.args.get("sample", 500))
    # Load your data here (adjust path as needed)
    df = pd.read_csv("C:\\Users\\Admin\\kdd-anomaly-detection-\\data\kddcup.data_10_percent", nrows=sample, header=None)
    # Optionally set columns names
    df.columns = ["duration","protocol_type","service","flag","src_bytes","dst_bytes","land","wrong_fragment","urgent",
        "hot","num_failed_logins","logged_in","num_compromised","root_shell","su_attempted","num_root",
        "num_file_creations","num_shells","num_access_files","num_outbound_cmds","is_host_login","is_guest_login",
        "count","srv_count","serror_rate","srv_serror_rate","rerror_rate","srv_rerror_rate","same_srv_rate",
        "diff_srv_rate","srv_diff_host_rate","dst_host_count","dst_host_srv_count","dst_host_same_srv_rate",
        "dst_host_diff_srv_rate","dst_host_same_src_port_rate","dst_host_srv_diff_host_rate",
        "dst_host_serror_rate","dst_host_srv_serror_rate","dst_host_rerror_rate","dst_host_srv_rerror_rate","label"]
    return jsonify(df.sample(sample).to_dict(orient="records"))
# ...existing code...



from flask import Flask, request, jsonify
from app.preprocess import load_all_data
from app.model import preprocess_features, train_isolation_forest, train_autoencoder, infer_autoencoder
import joblib  
import os  
import pandas as pd

app = Flask(__name__)

# Model loading (for demonstration, you may want to train and persist models separately)
data = load_all_data()
X, scaler = preprocess_features(data)
iso_forest = train_isolation_forest(X)
autoencoder = train_autoencoder(X)

@app.route('/predict', methods=['POST'])
def predict():
    input_data = request.json
    df = pd.DataFrame([input_data])
    X_input, _ = preprocess_features(df)
    # Isolation Forest
    iso_pred = iso_forest.predict(X_input)[0]
    # Autoencoder
    auto_pred, mse, threshold = infer_autoencoder(autoencoder, X_input)
    return jsonify({
        "isolation_forest": int(iso_pred == -1),
        "autoencoder": int(auto_pred[0]),
        "mse": float(mse[0]),
        "threshold": float(threshold)
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)