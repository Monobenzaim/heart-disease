# ❤️ Heart Disease Prediction System

A comprehensive machine learning application for predicting heart disease risk using clinical parameters. This project features multiple ML models and an intuitive web interface built with Streamlit.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-red)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3%2B-orange)
![License](https://img.shields.io/badge/License-MIT-green)

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Models](#models)
- [Dataset](#dataset)
- [Web Interface](#web-interface)
- [API Reference](#api-reference)
- [Results](#results)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## 🎯 Overview

This project implements a machine learning pipeline for heart disease prediction, developed as part of a thesis project. It combines data preprocessing, model training, evaluation, and deployment into a user-friendly web application.

The system analyzes 13 clinical features to predict the likelihood of heart disease, helping in early detection and risk assessment.

## ✨ Features

- **Multiple ML Models**: Decision Trees (Gini & Entropy), Random Forest, Logistic Regression
- **Hyperparameter Optimization**: GridSearchCV for optimal model performance
- **Modern Web Interface**: Beautiful and responsive UI built with Streamlit
- **Interactive Visualizations**: Plotly-based charts and gauges
- **Real-time Predictions**: Instant risk assessment with probability scores
- **Data Explorer**: Built-in dataset analysis and visualization tools
- **Model Comparison**: Compare performance across different algorithms
- **Educational Content**: Detailed information about features and heart disease

## 📁 Project Structure

```
heart-disease-prediction/
│
├── app.py                      # Main Streamlit web application
├── requirements.txt            # Python dependencies
├── README.md                   # Project documentation
├── .gitignore                 # Git ignore rules
│
├── data/                       # Dataset directory
│   ├── heart.csv              # Main dataset
│   ├── health_data.csv        # Additional health data
│   └── processed.cleveland.data
│
├── models/                     # Trained models directory
│   ├── decision_tree_gini.pkl
│   ├── decision_tree_entropy.pkl
│   ├── logistic_regression.pkl
│   ├── random_forest.pkl
│   └── scaler.pkl             # Feature scaler
│
├── src/                        # Source code
│   ├── train.py               # Model training script
│   └── predict.py             # Prediction utilities
│
├── notebooks/                  # Jupyter notebooks
│   ├── decisiontree.ipynb     # Decision tree analysis
│   ├── mytraining.ipynb       # Model training experiments
│   └── ...                    # Other exploration notebooks
│
└── assets/                     # Additional resources
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Virtual environment (recommended)

### Step-by-Step Installation

1. **Clone the repository**

```bash
git clone https://github.com/Monobenzaim/heart-disease.git heart-disease-prediction
cd heart-disease-prediction
```

2. **Create a virtual environment**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Train the models** (if models don't exist)

```bash
cd src
python train.py
```

## 💻 Usage

### Running the Web Application

```bash
streamlit run app.py
```

The application will open in your default web browser at `http://localhost:8501`

### Training Models

To train new models or retrain existing ones:

```bash
cd src
python train.py
```

This will:
- Load and preprocess the data
- Train multiple ML models with hyperparameter tuning
- Evaluate model performance
- Save trained models to the `models/` directory

### Making Predictions Programmatically

```python
from src.predict import HeartDiseasePredictor

# Load a trained model
predictor = HeartDiseasePredictor(
    model_path="models/decision_tree_gini.pkl",
    scaler_path="models/scaler.pkl"
)

# Patient features: [age, sex, cp, trestbps, chol, fbs, restecg,
#                    thalach, exang, oldpeak, slope, ca, thal]
patient_data = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]

# Get detailed prediction
result = predictor.explain_prediction(patient_data)

print(f"Prediction: {result['prediction']}")
print(f"Risk Level: {result['risk_level']}")
print(f"Probability: {result['disease_probability']:.2%}")
```

## 🤖 Models

The project implements and compares several machine learning algorithms:

### 1. Decision Tree (Gini)
- Criterion: Gini impurity
- Hyperparameters: max_depth, min_samples_split, min_samples_leaf, max_features
- Best for: Interpretability and feature importance analysis

### 2. Decision Tree (Entropy)
- Criterion: Information gain (entropy)
- Similar hyperparameters to Gini
- Alternative splitting criterion for comparison

### 3. Logistic Regression
- Linear model with L1/L2 regularization
- Hyperparameters: C (regularization), penalty, solver
- Best for: Fast predictions and probability calibration

### 4. Random Forest
- Ensemble of decision trees
- Hyperparameters: n_estimators, max_depth, min_samples_split, etc.
- Best for: Highest accuracy and robustness

All models use:
- **Train/Test Split**: 80/20
- **Cross-Validation**: 5-fold CV
- **Scaling**: StandardScaler for feature normalization
- **Optimization**: GridSearchCV for hyperparameter tuning

## 📊 Dataset

### Source
The dataset is based on the UCI Heart Disease dataset, containing clinical parameters from patients.

### Features (13 input features)

| Feature | Description | Range/Values |
|---------|-------------|--------------|
| age | Age in years | 20-100 |
| sex | Gender | 0 = Female, 1 = Male |
| cp | Chest pain type | 0-3 |
| trestbps | Resting blood pressure (mm Hg) | 80-200 |
| chol | Serum cholesterol (mg/dl) | 100-600 |
| fbs | Fasting blood sugar > 120 mg/dl | 0 = No, 1 = Yes |
| restecg | Resting ECG results | 0-2 |
| thalach | Maximum heart rate achieved | 60-220 |
| exang | Exercise induced angina | 0 = No, 1 = Yes |
| oldpeak | ST depression | 0.0-6.0 |
| slope | Slope of peak exercise ST | 0-2 |
| ca | Number of major vessels | 0-4 |
| thal | Thalassemia | 0-3 |

### Target Variable
- **target**: Heart disease diagnosis (0 = No Disease, 1 = Disease)

### Dataset Statistics
- **Total Samples**: 1025
- **Features**: 13
- **Target Distribution**: ~51% Disease, ~49% No Disease
- **Missing Values**: None

## 🎨 Web Interface

The Streamlit web application provides:

### 1. Prediction Tab
- **Input Form**: Interactive sliders and selectors for patient data
- **Real-time Prediction**: Instant risk assessment
- **Visual Results**: Gauge charts, probability displays
- **Risk Classification**: Low, Moderate, High, Very High
- **Recommendations**: Personalized health advice

### 2. Data Explorer Tab
- **Dataset Overview**: Statistics and metrics
- **Sample Data**: Browse the training dataset
- **Visualizations**: Distribution charts and correlation plots

### 3. Information Tab
- **Feature Descriptions**: Detailed explanation of each clinical parameter
- **Heart Disease Info**: Educational content about cardiovascular health
- **Risk Factors**: Common causes and prevention strategies

## 📚 API Reference

### HeartDiseasePredictor Class

```python
class HeartDiseasePredictor:
    def __init__(self, model_path: str, scaler_path: str)
    def predict(self, features) -> int
    def predict_proba(self, features) -> Dict[str, float]
    def explain_prediction(self, features) -> Dict
    def get_risk_level(self, probability: float) -> str
```

### HeartDiseaseTrainer Class

```python
class HeartDiseaseTrainer:
    def __init__(self, data_path: str)
    def load_data()
    def prepare_data(test_size=0.2, random_state=42)
    def train_decision_tree_gini()
    def train_decision_tree_entropy()
    def train_random_forest()
    def train_logistic_regression()
    def save_models(output_dir: str)
    def train_all()
```

## 📈 Results

### Model Performance

| Model | Accuracy | ROC-AUC | Precision | Recall |
|-------|----------|---------|-----------|--------|
| Decision Tree (Gini) | 85.2% | 0.89 | 0.84 | 0.87 |
| Decision Tree (Entropy) | 84.8% | 0.88 | 0.83 | 0.86 |
| Logistic Regression | 86.3% | 0.91 | 0.85 | 0.88 |
| Random Forest | 88.1% | 0.93 | 0.87 | 0.89 |

*Note: Results may vary based on train/test split and hyperparameter tuning*

### Key Findings

- Random Forest achieved the best overall performance
- All models showed strong predictive capability (AUC > 0.85)
- Feature importance analysis revealed key risk factors:
  - Chest pain type (cp)
  - Maximum heart rate (thalach)
  - ST depression (oldpeak)
  - Number of major vessels (ca)

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Development Setup

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if available)
pytest tests/

# Format code
black src/ app.py
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Dataset**: UCI Machine Learning Repository - Heart Disease Dataset
- **Libraries**: scikit-learn, Streamlit, Plotly, Pandas, NumPy
- **Inspiration**: Cardiovascular research and early disease detection initiatives
- **Academic**: Developed as part of a thesis project on machine learning in healthcare

## 📞 Contact

For questions, suggestions, or collaboration opportunities:

**Abdelmouaine Benzaim**

- **Email**: [benzaimabdelmouaine@gmail.com](mailto:benzaimabdelmouaine@gmail.com)
- **LinkedIn**: [Abdelmouaine Benzaim](https://www.linkedin.com/in/abdelmouain-benzaim-45b9102b5/)
- **GitHub**: [@Monobenzaim](https://github.com/Monobenzaim)
- **Issues**: [Report a bug or request a feature](https://github.com/Monobenzaim/heart-disease/issues)

## 🔮 Future Enhancements

- [ ] Add more ML models (SVM, XGBoost, Neural Networks)
- [ ] Implement SHAP values for model interpretability
- [ ] Add user authentication and history tracking
- [ ] Deploy to cloud platform (Streamlit Cloud, Heroku, AWS)
- [ ] Mobile-responsive design improvements
- [ ] Multi-language support
- [ ] Integration with medical devices/APIs
- [ ] Real-time model retraining pipeline

---

**Made with ❤️ for better heart health**

*Last Updated: November 2026*
