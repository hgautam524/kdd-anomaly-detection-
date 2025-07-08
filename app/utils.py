import os
import joblib
import logging

def setup_logger(name=__name__, log_file='app.log', level=logging.INFO):
    """Set up a logger for the app."""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)        
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        logger.addHandler(handler)
    return logger

def save_model(model, filename):
    """Save a model to disk using joblib."""
    joblib.dump(model, filename)

def load_model(filename):
    """Load a model from disk using joblib."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Model file {filename} not found.")
    return joblib.load(filename)

def save_scaler(scaler, filename):
    """Save a scaler/encoder to disk using joblib."""
    joblib.dump(scaler, filename)

def load_scaler(filename):
    """Load a scaler/encoder from disk using joblib."""
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Scaler file {filename} not found.")
    return joblib.load(filename)

def encode_categorical(df, columns, encoders=None):
    """Encode categorical columns using provided or new LabelEncoders."""
    from sklearn.preprocessing import LabelEncoder
    if encoders is None:
        encoders = {}
    for col in columns:
        le = encoders.get(col, LabelEncoder())
        df[col] = le.fit_transform(df[col].astype(str))
        encoders[col] = le
    return df, encoders