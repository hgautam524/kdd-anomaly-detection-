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


![image](https://github.com/user-attachments/assets/6a699700-1802-40d4-b88e-c5a6449e8fe0)


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

## Streamlit ( Login Credentials )
- Use default Login Credentials
--- USER AUTH (simple demo, not secure) ---
USERS = {"admin": "admin123", "user": "user123"}

![image](https://github.com/user-attachments/assets/a95f470e-8c26-4680-b192-69fcd68bbe21)



## API Example

```json
POST /predict
{
  "duration": 0, "protocol_type": 1, ...
}
```

## Inside anomaly-detection-Visualisation.ipynb 

![image](https://github.com/user-attachments/assets/f14b7648-75ae-4434-a059-f667fd7bf42d)

![image](https://github.com/user-attachments/assets/6353f285-6c37-49dd-a82a-8990bd8bf244)

![image](https://github.com/user-attachments/assets/877198f2-5a86-4379-a969-f80ce2641d88)

![image](https://github.com/user-attachments/assets/6270650a-20a9-4a89-8a62-5472ecb45efc)



## Notes

- The first run will be slow as models are trained on startup.
- You can persist trained models for faster reload (see `joblib` in `app/model.py`).
