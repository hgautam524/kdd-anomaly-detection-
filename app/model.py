import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from keras.models import Model
from keras.layers import Input, Dense
from keras import regularizers

def preprocess_features(df):
    # Encode categorical features
    for col in ["protocol_type", "service", "flag"]:
        if col in df.columns:
            le = LabelEncoder()
            df[col] = le.fit_transform(df[col].astype(str))
    # Drop label if present
    X = df.drop(columns=["label"], errors="ignore")
    scaler = MinMaxScaler()
    X_scaled = scaler.fit_transform(X)
    return X_scaled, scaler

def train_isolation_forest(X):
    clf = IsolationForest(contamination=0.01, random_state=42)
    clf.fit(X)
    return clf

def train_autoencoder(X):
    input_dim = X.shape[1]
    input_layer = Input(shape=(input_dim,))
    encoded = Dense(32, activation="relu", activity_regularizer=regularizers.l1(1e-5))(input_layer)
    encoded = Dense(16, activation="relu")(encoded)
    decoded = Dense(32, activation="relu")(encoded)
    decoded = Dense(input_dim, activation="sigmoid")(decoded)
    autoencoder = Model(inputs=input_layer, outputs=decoded)
    autoencoder.compile(optimizer="adam", loss="mse")
    autoencoder.fit(X, X, epochs=5, batch_size=256, shuffle=True, validation_split=0.1, verbose=1)
    return autoencoder

def infer_autoencoder(autoencoder, X, threshold=None):
    reconstructions = autoencoder.predict(X)
    mse = np.mean(np.power(X - reconstructions, 2), axis=1)
    if threshold is None:
        threshold = np.percentile(mse, 99)
    return (mse > threshold).astype(int), mse, threshold