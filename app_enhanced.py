"""
Heart Disease Prediction Web Application with AI Explanations & PDF Reports
Enhanced version with Groq LLM integration and PDF report generation
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys
import os

# Add src directory to path
sys.path.append(str(Path(__file__).parent / "src"))

try:
    from src.predict import HeartDiseasePredictor, load_all_models
    from src.llm_explainer import MedicalExplainer
    from src.report_generator import MedicalReportGenerator
except ImportError:
    from predict import HeartDiseasePredictor, load_all_models
    from llm_explainer import MedicalExplainer
    from report_generator import MedicalReportGenerator


# Page configuration
st.set_page_config(
    page_title="Heart Disease Prediction AI",
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
    .stDownloadButton>button {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
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
    st.markdown("<h1 style='text-align: center;'>❤️ AI-Powered Heart Disease Prediction System</h1>",
                unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #666;'>Advanced ML with LLM-Enhanced Medical Explanations & PDF Reports</p>",
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
        st.title("⚙️ Configuration")

        # Model selection
        model_name = st.selectbox(
            "🤖 Select ML Model",
            options=list(models.keys()),
            format_func=lambda x: x.replace('_', ' ').title()
        )

        st.markdown("---")

        # Groq API Key input
        st.markdown("### 🧠 AI Explanations (Optional)")
        st.info("Get detailed medical explanations powered by Groq's free LLM API")

        groq_api_key = st.text_input(
            "Groq API Key",
            type="password",
            help="Get your free API key at: https://console.groq.com/keys",
            placeholder="gsk_..."
        )

        if groq_api_key:
            os.environ["GROQ_API_KEY"] = groq_api_key
            st.success("✓ AI explanations enabled!")
            st.caption("Using Llama 3.1 70B model")
        else:
            st.caption("Enter API key to enable AI medical explanations")

        st.markdown("---")

        # PDF Report options
        st.markdown("### 📄 PDF Report Options")
        generate_pdf = st.checkbox("Generate PDF Report", value=False)

        if generate_pdf:
            patient_name = st.text_input("Patient Name", "John Doe")
            patient_id = st.text_input("Patient ID", "P123456")
            doctor_name = st.text_input("Doctor Name (Optional)", "")
            hospital_name = st.text_input("Hospital Name (Optional)", "")
        else:
            patient_name = patient_id = doctor_name = hospital_name = None

        st.markdown("---")
        st.markdown("### 📚 About")
        st.info("""
        This enhanced application combines:
        - **Machine Learning** for predictions
        - **Groq LLM** for medical explanations
        - **PDF Reports** for documentation

        **Models Available:**
        - Decision Tree (Gini & Entropy)
        - Logistic Regression
        - Random Forest
        """)

        st.markdown("---")
        st.markdown("### ⚠️ Disclaimer")
        st.warning("This tool is for educational purposes only. Not a replacement for professional medical advice.")

    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🔍 Prediction", "📊 Benchmarks", "📈 Data Explorer", "ℹ️ Information"])

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
        if st.button("🔮 Analyze & Predict Heart Disease Risk", use_container_width=True):
            # Prepare features
            features = [age, sex, cp, trestbps, chol, fbs, restecg,
                       thalach, exang, oldpeak, slope, ca, thal]

            # Get predictor
            predictor = models[model_name]

            # Make prediction
            with st.spinner("Analyzing patient data..."):
                result = predictor.explain_prediction(features)

            # Store in session state for PDF generation
            st.session_state['last_prediction'] = {
                'features': features,
                'result': result,
                'model_name': model_name
            }

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

            # AI-powered medical explanation
            if groq_api_key:
                st.markdown("---")
                st.markdown("### 🧠 AI-Powered Medical Analysis")

                with st.spinner("Generating detailed medical explanation with AI..."):
                    try:
                        explainer = MedicalExplainer(api_key=groq_api_key)
                        llm_explanation = explainer.explain_prediction(
                            features=features,
                            prediction=result['prediction_value'],
                            probability=result['disease_probability'],
                            risk_level=result['risk_level'],
                            model_name=model_name
                        )

                        st.session_state['llm_explanation'] = llm_explanation

                        # Display explanation in an expander
                        with st.expander("📖 View Detailed Medical Analysis", expanded=True):
                            st.markdown(llm_explanation)

                    except Exception as e:
                        st.error(f"Error generating AI explanation: {e}")
                        st.info("Please check your Groq API key and try again.")
                        st.session_state['llm_explanation'] = None
            else:
                st.info("💡 Enable AI explanations by entering your Groq API key in the sidebar")
                st.session_state['llm_explanation'] = None

            # Basic Recommendations
            st.markdown("---")
            st.markdown("### 💡 General Recommendations")
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

            # PDF Report Generation
            if generate_pdf and patient_name and patient_id:
                st.markdown("---")
                st.markdown("### 📄 PDF Report")

                with st.spinner("Generating professional PDF report..."):
                    try:
                        generator = MedicalReportGenerator(output_dir="reports")

                        patient_info = {
                            'name': patient_name,
                            'id': patient_id,
                            'dob': 'N/A',
                            'age': age,
                            'sex': 'Male' if sex == 1 else 'Female'
                        }

                        llm_text = st.session_state.get('llm_explanation', None)

                        pdf_path = generator.generate_report(
                            patient_info=patient_info,
                            features=features,
                            prediction_result=result,
                            llm_explanation=llm_text,
                            model_name=model_name,
                            doctor_name=doctor_name if doctor_name else None,
                            hospital_name=hospital_name if hospital_name else None
                        )

                        # Read PDF file
                        with open(pdf_path, "rb") as pdf_file:
                            pdf_bytes = pdf_file.read()

                        st.success(f"✓ Report generated successfully!")

                        # Download button
                        st.download_button(
                            label="📥 Download PDF Report",
                            data=pdf_bytes,
                            file_name=f"heart_disease_report_{patient_id}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )

                    except Exception as e:
                        st.error(f"Error generating PDF report: {e}")

    with tab2:
        st.header("📊 Model Benchmarks & Comparison")

        st.info("""
        **Comprehensive Model Benchmarking**

        Run detailed comparison of all ML models on medical diagnostic metrics.
        This includes sensitivity, specificity, ROC-AUC, and more.
        """)

        if st.button("🚀 Run Complete Benchmark"):
            st.warning("This will take 2-5 minutes to complete...")

            with st.spinner("Running comprehensive benchmark..."):
                try:
                    from src.benchmark import MedicalModelBenchmark

                    # Run benchmark
                    benchmark = MedicalModelBenchmark(
                        data_path="data/heart.csv",
                        test_size=0.2,
                        random_state=42
                    )

                    benchmark.run_all_benchmarks()
                    benchmark.generate_comparison_report()

                    st.success("✓ Benchmark complete!")
                    st.balloons()

                    st.markdown("### 📈 Check Results")
                    st.info("Results saved in `benchmark_results/` folder")
                    st.markdown("- Metrics CSV file")
                    st.markdown("- Visualization PNGs")
                    st.markdown("- JSON report")

                except Exception as e:
                    st.error(f"Error running benchmark: {e}")

        st.markdown("---")
        st.markdown("### 📚 What's Included in Benchmark?")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""
            **Models Compared:**
            - Decision Tree (Gini)
            - Decision Tree (Entropy)
            - Random Forest
            - Gradient Boosting
            - Logistic Regression
            - SVM (RBF)
            - Naive Bayes
            """)

        with col2:
            st.markdown("""
            **Metrics Evaluated:**
            - Accuracy & Balanced Accuracy
            - Sensitivity (Recall/TPR)
            - Specificity (TNR)
            - Precision (PPV) & NPV
            - F1-Score & ROC-AUC
            - Matthews Correlation
            - Cohen's Kappa
            - Training & Prediction Time
            """)

    with tab3:
        st.header("📈 Dataset Explorer")

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

    with tab4:
        st.header("ℹ️ System Information")

        st.markdown("""
        ### 🎯 About This System

        This enhanced heart disease prediction system combines:

        1. **Machine Learning Models**: Multiple algorithms trained on cardiovascular data
        2. **Groq LLM Integration**: Free, fast AI-powered medical explanations using Llama 3.1 70B
        3. **PDF Report Generation**: Professional medical reports with detailed analysis
        4. **Comprehensive Benchmarking**: Detailed model comparison with medical metrics

        ### 🔑 Getting Your Free Groq API Key

        1. Visit: https://console.groq.com/keys
        2. Sign up for a free account
        3. Create an API key
        4. Paste it in the sidebar

        **Why Groq?**
        - 100% Free to use
        - Extremely fast inference
        - Powerful Llama 3.1 70B model
        - No credit card required

        ### 📊 Model Benchmarking

        The benchmarking system evaluates models on:
        - **Medical Diagnostic Metrics**: Sensitivity, Specificity, PPV, NPV
        - **Performance Metrics**: Accuracy, F1-Score, ROC-AUC
        - **Efficiency Metrics**: Training time, prediction speed
        - **Statistical Metrics**: MCC, Cohen's Kappa, Youden's Index

        ### 📄 PDF Reports Include:
        - Patient information
        - Clinical parameters
        - Prediction results with risk levels
        - AI-generated medical analysis
        - Visualizations
        - Professional formatting
        - Disclaimer and recommendations
        """)

        st.markdown("---")

        # Feature Information
        st.markdown("### 📋 Clinical Features")

        feature_info = {
            "**Age**": "Patient's age in years",
            "**Sex**": "1 = Male, 0 = Female",
            "**Chest Pain Type (CP)**": "0: Typical Angina, 1: Atypical Angina, 2: Non-Anginal, 3: Asymptomatic",
            "**Resting Blood Pressure**": "Blood pressure in mm Hg",
            "**Cholesterol**": "Serum cholesterol in mg/dl",
            "**Fasting Blood Sugar**": "1 if > 120 mg/dl, 0 otherwise",
            "**Resting ECG**": "0: Normal, 1: ST-T abnormality, 2: LV hypertrophy",
            "**Max Heart Rate**": "Maximum heart rate achieved",
            "**Exercise Angina**": "1 = Yes, 0 = No",
            "**ST Depression**": "Depression induced by exercise",
            "**Slope**": "Slope of peak exercise ST segment",
            "**CA**": "Number of major vessels (0-4)",
            "**Thalassemia**": "0: Normal, 1: Fixed defect, 2: Reversible defect"
        }

        for feature, description in feature_info.items():
            with st.expander(feature):
                st.markdown(description)


if __name__ == "__main__":
    main()
