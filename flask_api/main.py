from flask import Flask, request, jsonify
from app.preprocess import load_all_data
from app.model import preprocess_features, train_isolation_forest, train_autoencoder, infer_autoencoder
import joblib
import os

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