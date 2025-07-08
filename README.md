# KDD Cup 1999 Anomaly Detection

An end-to-end anomaly detection project using the KDD Cup 1999 dataset, leveraging both Isolation Forest and Autoencoder models. Features:

- Loads and aggregates all provided KDD Cup data files.
- Offers a Flask API for backend ML inference.
- Streamlit UI for user-friendly interaction.
- Ready for Docker deployment.

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