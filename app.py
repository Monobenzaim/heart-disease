"""
Heart Disease Prediction Web Application
A modern and aesthetic web interface built with Streamlit
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.predict import HeartDiseasePredictor, load_all_models
except ImportError:
    from predict import HeartDiseasePredictor, load_all_models


# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better aesthetics
st.markdown("""
<style>
    .main {
        padding: 0rem 1rem;
    }
    .stAlert {
        border-radius: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
    }
    .info-box {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #667eea;
        margin: 10px 0;
    }
    h1 {
        color: #667eea;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 10px;
        border-radius: 8px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_models():
    """Load all available models (cached)"""
    try:
        return load_all_models("models")
    except Exception as e:
        st.error(f"Error loading models: {e}")
        return {}


def create_gauge_chart(probability: float, title: str):
    """Create a gauge chart for probability visualization"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=probability * 100,
        title={'text': title, 'font': {'size': 20}},
        delta={'reference': 50},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [0, 30], 'color': "#90EE90"},
                {'range': [30, 60], 'color': "#FFD700"},
                {'range': [60, 80], 'color': "#FFA500"},
                {'range': [80, 100], 'color': "#FF6347"}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 90
            }
        }
    ))

    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_feature_importance_chart(features_dict: dict):
    """Create a horizontal bar chart for feature values"""
    df = pd.DataFrame(list(features_dict.items()), columns=['Feature', 'Value'])

    fig = px.bar(df, x='Value', y='Feature', orientation='h',
                 title='Input Feature Values',
                 color='Value',
                 color_continuous_scale='Viridis')

    fig.update_layout(height=400, showlegend=False)
    return fig


def main():
    """Main application"""

    # Header
    st.markdown("<h1 style='text-align: center;'>❤️ Heart Disease Prediction System</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Advanced ML-powered cardiovascular risk assessment</p>",
                unsafe_allow_html=True)

    st.markdown("---")

    # Load models
    models = load_models()

    if not models:
        st.error("⚠️ No models found! Please train models first by running: `python src/train.py`")
        st.info("📝 After training, the models will be saved in the `models/` directory.")
        return

    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/color/96/000000/heart-health.png", width=100)
        st.title("Configuration")

        # Model selection
        model_name = st.selectbox(
            "Select Model",
            options=list(models.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        st.markdown("---")
        st.markdown("### About")
        st.info("""
        This application uses machine learning to predict the likelihood of heart disease based on clinical parameters.

        **Models Available:**
        - Decision Tree (Gini)
        - Decision Tree (Entropy)
        - Logistic Regression
        - Random Forest
        """)

        st.markdown("---")
        st.markdown("### Disclaimer")
        st.warning("⚠️ This tool is for educational purposes only and should not replace professional medical advice.")

    # Main content
    tab1, tab2, tab3 = st.tabs(["🔍 Prediction", "📊 Data Explorer", "ℹ️ Information"])

    with tab1:
        st.header("Patient Information")

        # Create two columns for input fields
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Personal Information")
            age = st.slider("Age", 20, 100, 50, help="Patient's age in years")
            sex = st.radio("Sex", options=[1, 0], format_func=lambda x: "Male" if x == 1 else "Female")

            st.subheader("Blood Pressure & Cholesterol")
            trestbps = st.slider("Resting Blood Pressure", 80, 200, 120,
                               help="Resting blood pressure in mm Hg")
            chol = st.slider("Serum Cholesterol", 100, 600, 200,
                           help="Serum cholesterol in mg/dl")
            fbs = st.radio("Fasting Blood Sugar > 120 mg/dl",
                         options=[1, 0],
                         format_func=lambda x: "Yes" if x == 1 else "No")

        with col2:
            st.subheader("Clinical Indicators")
            cp = st.selectbox("Chest Pain Type", options=[0, 1, 2, 3],
                            format_func=lambda x: ["Typical Angina", "Atypical Angina",
                                                  "Non-Anginal Pain", "Asymptomatic"][x])
            restecg = st.selectbox("Resting ECG", options=[0, 1, 2],
                                 format_func=lambda x: ["Normal", "ST-T Wave Abnormality",
                                                       "Left Ventricular Hypertrophy"][x])

            st.subheader("Exercise Test Results")
            thalach = st.slider("Maximum Heart Rate", 60, 220, 150,
                              help="Maximum heart rate achieved")
            exang = st.radio("Exercise Induced Angina",
                           options=[1, 0],
                           format_func=lambda x: "Yes" if x == 1 else "No")
            oldpeak = st.slider("ST Depression", 0.0, 6.0, 1.0, 0.1,
                              help="ST depression induced by exercise relative to rest")

        col3, col4 = st.columns(2)
        with col3:
            slope = st.selectbox("Slope of Peak Exercise ST", options=[0, 1, 2],
                               format_func=lambda x: ["Upsloping", "Flat", "Downsloping"][x])
        with col4:
            ca = st.slider("Number of Major Vessels", 0, 4, 0,
                         help="Number of major vessels colored by fluoroscopy")

        thal = st.selectbox("Thalassemia", options=[0, 1, 2, 3],
                          format_func=lambda x: ["Normal", "Fixed Defect",
                                                "Reversible Defect", "Unknown"][x])

        st.markdown("---")

        # Predict button
        if st.button("🔮 Predict Heart Disease Risk", use_container_width=True):
            # Prepare features
            features = [age, sex, cp, trestbps, chol, fbs, restecg,
                       thalach, exang, oldpeak, slope, ca, thal]

            # Get predictor
            predictor = models[model_name]

            # Make prediction
            with st.spinner("Analyzing patient data..."):
                result = predictor.explain_prediction(features)

            # Display results
            st.markdown("## 📋 Prediction Results")

            # Create three columns for metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                prediction_color = "🔴" if result['prediction_value'] == 1 else "🟢"
                st.markdown(f"### {prediction_color} {result['prediction']}")

            with col2:
                st.metric("Risk Level", result['risk_level'])

            with col3:
                st.metric("Confidence", f"{result['confidence']:.1%}")

            # Gauge chart
            st.plotly_chart(
                create_gauge_chart(result['disease_probability'], "Disease Probability"),
                use_container_width=True
            )

            # Probabilities
            col1, col2 = st.columns(2)
            with col1:
                st.success(f"**No Disease:** {result['probabilities']['no_disease']:.2%}")
            with col2:
                st.error(f"**Disease:** {result['probabilities']['disease']:.2%}")

            # Feature visualization
            st.markdown("### 📊 Input Features Overview")
            features_dict = {
                'Age': age, 'Sex': sex, 'CP': cp, 'BP': trestbps,
                'Cholesterol': chol, 'FBS': fbs, 'RestECG': restecg,
                'MaxHR': thalach, 'ExAngina': exang, 'Oldpeak': oldpeak,
                'Slope': slope, 'CA': ca, 'Thal': thal
            }
            st.plotly_chart(create_feature_importance_chart(features_dict),
                          use_container_width=True)

            # Recommendations
            st.markdown("### 💡 Recommendations")
            if result['prediction_value'] == 1:
                st.error("""
                **High Risk Detected!**
                - Consult with a cardiologist immediately
                - Schedule comprehensive cardiac evaluation
                - Maintain detailed health records
                - Follow prescribed medication regimen
                - Adopt heart-healthy lifestyle changes
                """)
            else:
                st.success("""
                **Low Risk Detected!**
                - Maintain regular health check-ups
                - Continue healthy lifestyle habits
                - Monitor blood pressure and cholesterol
                - Stay physically active
                - Eat a balanced, heart-healthy diet
                """)

    with tab2:
        st.header("📊 Dataset Explorer")

        try:
            df = pd.read_csv("data/heart.csv")

            st.subheader("Dataset Overview")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Total Samples", len(df))
            col2.metric("Features", len(df.columns) - 1)
            col3.metric("Disease Cases", df['target'].sum())
            col4.metric("Healthy Cases", (df['target'] == 0).sum())

            st.markdown("---")

            # Display dataframe
            st.subheader("Sample Data")
            st.dataframe(df.head(10), use_container_width=True)

            # Statistics
            st.subheader("Statistical Summary")
            st.dataframe(df.describe(), use_container_width=True)

            # Distribution plots
            st.subheader("Target Distribution")
            fig = px.pie(df, names='target',
                        title='Heart Disease Distribution',
                        color_discrete_sequence=['#90EE90', '#FF6347'])
            st.plotly_chart(fig, use_container_width=True)

        except FileNotFoundError:
            st.warning("Dataset not found in data/heart.csv")

    with tab3:
        st.header("ℹ️ Feature Information")

        st.markdown("""
        ### Clinical Features Explained

        Below is a detailed description of each feature used in the prediction model:
        """)

        feature_info = {
            "**Age**": "Patient's age in years",
            "**Sex**": "1 = Male, 0 = Female",
            "**Chest Pain Type (CP)**": """
            - 0: Typical Angina
            - 1: Atypical Angina
            - 2: Non-Anginal Pain
            - 3: Asymptomatic
            """,
            "**Resting Blood Pressure (trestbps)**": "Blood pressure in mm Hg on admission",
            "**Serum Cholesterol (chol)**": "Cholesterol level in mg/dl",
            "**Fasting Blood Sugar (fbs)**": "1 if > 120 mg/dl, 0 otherwise",
            "**Resting ECG (restecg)**": """
            - 0: Normal
            - 1: ST-T wave abnormality
            - 2: Left ventricular hypertrophy
            """,
            "**Maximum Heart Rate (thalach)**": "Maximum heart rate achieved during exercise",
            "**Exercise Induced Angina (exang)**": "1 = Yes, 0 = No",
            "**ST Depression (oldpeak)**": "Depression induced by exercise relative to rest",
            "**Slope**": """
            - 0: Upsloping
            - 1: Flat
            - 2: Downsloping
            """,
            "**CA**": "Number of major vessels (0-4) colored by fluoroscopy",
            "**Thalassemia (thal)**": """
            - 0: Normal
            - 1: Fixed defect
            - 2: Reversible defect
            - 3: Unknown
            """
        }

        for feature, description in feature_info.items():
            with st.expander(feature):
                st.markdown(description)

        st.markdown("---")
        st.markdown("### 🏥 About Heart Disease")
        st.info("""
        Heart disease describes a range of conditions that affect your heart. Diseases under
        the heart disease umbrella include blood vessel diseases, heart rhythm problems,
        and heart defects you're born with, among others.

        **Risk Factors Include:**
        - High blood pressure
        - High cholesterol
        - Smoking
        - Obesity
        - Poor diet
        - Physical inactivity
        - Excessive alcohol use

        **Prevention:**
        - Regular exercise
        - Healthy diet
        - Stress management
        - Regular health screenings
        """)


if __name__ == "__main__":
    main()
