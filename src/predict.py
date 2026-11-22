"""
Heart Disease Prediction Utilities
Provides functions for making predictions using trained models.
"""

import joblib
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Union


class HeartDiseasePredictor:
    """Make predictions for heart disease using trained models"""

    # Feature names in order
    FEATURE_NAMES = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]

    # Feature descriptions
    FEATURE_INFO = {
        'age': 'Age in years',
        'sex': 'Sex (1 = male; 0 = female)',
        'cp': 'Chest pain type (0-3)',
        'trestbps': 'Resting blood pressure (mm Hg)',
        'chol': 'Serum cholesterol (mg/dl)',
        'fbs': 'Fasting blood sugar > 120 mg/dl (1 = true; 0 = false)',
        'restecg': 'Resting electrocardiographic results (0-2)',
        'thalach': 'Maximum heart rate achieved',
        'exang': 'Exercise induced angina (1 = yes; 0 = no)',
        'oldpeak': 'ST depression induced by exercise relative to rest',
        'slope': 'Slope of the peak exercise ST segment (0-2)',
        'ca': 'Number of major vessels colored by fluoroscopy (0-4)',
        'thal': 'Thalassemia (0 = normal; 1 = fixed defect; 2 = reversible defect; 3 = unknown)'
    }

    def __init__(self, model_path: str, scaler_path: str):
        """
        Initialize predictor with model and scaler paths

        Args:
            model_path: Path to the trained model pickle file
            scaler_path: Path to the fitted scaler pickle file
        """
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)

    def predict(self, features: Union[List, np.ndarray, pd.DataFrame]) -> int:
        """
        Predict heart disease for given features

        Args:
            features: Input features (can be list, array, or DataFrame)

        Returns:
            Prediction (0 = No Disease, 1 = Disease)
        """
        # Convert to numpy array if needed
        if isinstance(features, list):
            features = np.array(features).reshape(1, -1)
        elif isinstance(features, pd.DataFrame):
            features = features.values

        # Ensure correct shape
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Scale features
        features_scaled = self.scaler.transform(features)

        # Make prediction
        prediction = self.model.predict(features_scaled)[0]

        return int(prediction)

    def predict_proba(self, features: Union[List, np.ndarray, pd.DataFrame]) -> Dict[str, float]:
        """
        Get prediction probabilities

        Args:
            features: Input features

        Returns:
            Dictionary with probabilities for each class
        """
        # Convert to numpy array if needed
        if isinstance(features, list):
            features = np.array(features).reshape(1, -1)
        elif isinstance(features, pd.DataFrame):
            features = features.values

        # Ensure correct shape
        if features.ndim == 1:
            features = features.reshape(1, -1)

        # Scale features
        features_scaled = self.scaler.transform(features)

        # Get probabilities
        if hasattr(self.model, 'predict_proba'):
            proba = self.model.predict_proba(features_scaled)[0]
            return {
                'no_disease': float(proba[0]),
                'disease': float(proba[1])
            }
        else:
            # For models without predict_proba, return binary result
            prediction = self.model.predict(features_scaled)[0]
            if prediction == 0:
                return {'no_disease': 1.0, 'disease': 0.0}
            else:
                return {'no_disease': 0.0, 'disease': 1.0}

    def get_risk_level(self, probability: float) -> str:
        """
        Determine risk level based on disease probability

        Args:
            probability: Probability of disease (0-1)

        Returns:
            Risk level string
        """
        if probability < 0.3:
            return "Low Risk"
        elif probability < 0.6:
            return "Moderate Risk"
        elif probability < 0.8:
            return "High Risk"
        else:
            return "Very High Risk"

    def explain_prediction(self, features: Union[List, np.ndarray, pd.DataFrame]) -> Dict:
        """
        Get detailed explanation of prediction

        Args:
            features: Input features

        Returns:
            Dictionary with prediction details
        """
        prediction = self.predict(features)
        probabilities = self.predict_proba(features)

        disease_prob = probabilities['disease']
        risk_level = self.get_risk_level(disease_prob)

        return {
            'prediction': 'Disease Detected' if prediction == 1 else 'No Disease',
            'prediction_value': prediction,
            'probabilities': probabilities,
            'disease_probability': disease_prob,
            'risk_level': risk_level,
            'confidence': max(probabilities.values())
        }

    @staticmethod
    def create_feature_dict(age: int, sex: int, cp: int, trestbps: int,
                          chol: int, fbs: int, restecg: int, thalach: int,
                          exang: int, oldpeak: float, slope: int,
                          ca: int, thal: int) -> List:
        """
        Create feature list from individual parameters

        Args:
            All 13 heart disease features

        Returns:
            List of features in correct order
        """
        return [age, sex, cp, trestbps, chol, fbs, restecg, thalach,
                exang, oldpeak, slope, ca, thal]


def load_all_models(models_dir: str = "../models") -> Dict[str, HeartDiseasePredictor]:
    """
    Load all available trained models

    Args:
        models_dir: Directory containing model files

    Returns:
        Dictionary of model name to predictor instance
    """
    models_path = Path(models_dir)
    scaler_path = models_path / "scaler.pkl"

    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")

    predictors = {}

    # Load all model files
    for model_file in models_path.glob("*.pkl"):
        if model_file.name != "scaler.pkl":
            model_name = model_file.stem
            try:
                predictor = HeartDiseasePredictor(str(model_file), str(scaler_path))
                predictors[model_name] = predictor
                print(f"Loaded model: {model_name}")
            except Exception as e:
                print(f"Error loading {model_name}: {e}")

    return predictors


if __name__ == "__main__":
    # Example usage
    print("Heart Disease Predictor - Example Usage\n")

    # Try to load a model
    try:
        predictor = HeartDiseasePredictor(
            "../models/decision_tree_gini.pkl",
            "../models/scaler.pkl"
        )

        # Example patient data
        patient_features = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]

        # Make prediction
        result = predictor.explain_prediction(patient_features)

        print("Prediction Results:")
        print(f"  Prediction: {result['prediction']}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Disease Probability: {result['disease_probability']:.2%}")
        print(f"  Confidence: {result['confidence']:.2%}")

    except FileNotFoundError:
        print("Models not found. Please train models first using train.py")
