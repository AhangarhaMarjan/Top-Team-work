import pickle
import numpy as np

# Load the trained model and columns
with open('lung_cancer_model.pkl', 'rb') as f:
    model = pickle.load(f)

with open('columns.pkl', 'rb') as f:
    columns = pickle.load(f)

def predict_lung_cancer(features):
    features = np.array(features).reshape(1, -1)
    prediction = model.predict(features)
    return prediction[0]
