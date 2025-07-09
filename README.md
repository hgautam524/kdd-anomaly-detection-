## 🚨 Anomaly Detection in Network Traffic

This project is a complete end-to-end pipeline for detecting anomalies in network traffic using the **KDD Cup 1999 dataset**. It combines **unsupervised machine learning** techniques like **Isolation Forest** and **Autoencoders**, and offers:

- ✅ A Flask API for inference
- ✅ A Streamlit UI for interaction and visualization
- ✅ A Jupyter notebook with detailed analysis
- ✅ Docker support for one-click deployment

---

## 📦 Features

- 🔍 Detects anomalies using Isolation Forest & Autoencoder
- 📊 Visualize traffic patterns, labels, and outliers
- 💾 Upload custom datasets through UI
- 📈 View real-time results in an interactive dashboard
- 🧠 Jupyter notebook analysis: `anomaly-detection-Visualisation.ipynb`
- 🐳 Dockerized for cross-platform execution

---

## 📁 Project Structure

kdd-anomaly-detection/
│
├── app/
│   ├── __init__.py
│   ├── model.py           # ML logic (training, prediction)
│   ├── preprocess.py      # Data loading and preprocessing
│   ├── config.py          # Configurations
│   └── utils.py
│
├── flask_api/
│   ├── __init__.py
│   └── main.py            # Flask app exposing prediction API
│
├── streamlit_ui/
│   └── app.py             # Streamlit frontend
│
├── data/                  # Place for KDD Cup files
│
│---anomaly-detection-Visualisation.ipynb      # Jupyter Visualisation Analysis File
├── requirements.txt
├── Dockerfile
├── README.md
└── .gitignore



## Usage

### 1. Download Data

Place all KDD Cup files (from [Kaggle](https://www.kaggle.com/datasets/galaxyh/kdd-cup-1999-data)) into the `data/` directory.

### 2. Build and Run

**Locally:**

```sh
pip install -r requirements.txt
python flask_api/main.py
# In another terminal
streamlit run streamlit_ui/app.py
```

**With Docker:**

```sh
docker build -t kdd-anomaly-detection .
docker run -p 5000:5000 -p 8501:8501 -v $(pwd)/data:/app/data kdd-anomaly-detection
```

### 3. Access

- Streamlit UI: [http://localhost:8501](http://localhost:8501)
- API: [http://localhost:5000/predict](http://localhost:5000/predict)

## API Example

```json
POST /predict
{
  "duration": 0, "protocol_type": 1, ...
}
```

## Notes

- The first run will be slow as models are trained on startup.
- You can persist trained models for faster reload (see `joblib` in `app/model.py`).
