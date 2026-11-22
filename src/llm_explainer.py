"""
LLM-Powered Medical Explanation using Groq API
Provides detailed medical interpretations of predictions
"""

import os
from typing import Dict, List, Optional
from groq import Groq


class MedicalExplainer:
    """Generate medical explanations using Groq LLM"""

    # Feature descriptions for context
    FEATURE_DESCRIPTIONS = {
        'age': 'Patient age in years',
        'sex': 'Sex (1=Male, 0=Female)',
        'cp': 'Chest pain type (0=Typical Angina, 1=Atypical Angina, 2=Non-Anginal, 3=Asymptomatic)',
        'trestbps': 'Resting blood pressure in mm Hg',
        'chol': 'Serum cholesterol in mg/dl',
        'fbs': 'Fasting blood sugar > 120 mg/dl (1=Yes, 0=No)',
        'restecg': 'Resting ECG results (0=Normal, 1=ST-T abnormality, 2=LV hypertrophy)',
        'thalach': 'Maximum heart rate achieved',
        'exang': 'Exercise induced angina (1=Yes, 0=No)',
        'oldpeak': 'ST depression induced by exercise',
        'slope': 'Slope of peak exercise ST segment (0=Upsloping, 1=Flat, 2=Downsloping)',
        'ca': 'Number of major vessels colored by fluoroscopy (0-4)',
        'thal': 'Thalassemia (0=Normal, 1=Fixed defect, 2=Reversible defect, 3=Unknown)'
    }

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Groq client

        Args:
            api_key: Groq API key (if None, reads from GROQ_API_KEY env variable)
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Groq API key not found! Set GROQ_API_KEY environment variable or pass api_key parameter.\n"
                "Get your free API key at: https://console.groq.com/keys"
            )

        self.client = Groq(api_key=self.api_key)
        self.model = "llama-3.1-70b-versatile"  # Fast and powerful

    def format_patient_data(self, features: List[float]) -> str:
        """Format patient features into readable text"""
        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

        formatted = []
        for name, value in zip(feature_names, features):
            desc = self.FEATURE_DESCRIPTIONS.get(name, name)
            formatted.append(f"- {desc}: {value}")

        return "\n".join(formatted)

    def explain_prediction(
        self,
        features: List[float],
        prediction: int,
        probability: float,
        risk_level: str,
        model_name: str = "Machine Learning Model"
    ) -> str:
        """
        Generate detailed medical explanation for a prediction

        Args:
            features: Patient feature values
            prediction: Model prediction (0 or 1)
            probability: Probability of disease
            risk_level: Risk level classification
            model_name: Name of the ML model used

        Returns:
            Detailed medical explanation
        """
        patient_data = self.format_patient_data(features)

        prompt = f"""You are a medical AI assistant specializing in cardiovascular health. Analyze this patient's data and provide a detailed, professional medical interpretation.

**Patient Clinical Data:**
{patient_data}

**AI Prediction Results:**
- Prediction: {"Heart Disease Detected" if prediction == 1 else "No Heart Disease Detected"}
- Disease Probability: {probability:.1%}
- Risk Level: {risk_level}
- Model Used: {model_name}

**Please provide:**

1. **Clinical Summary** (2-3 sentences)
   - Overall cardiovascular health assessment
   - Key risk factors identified

2. **Risk Factor Analysis** (bullet points)
   - Identify concerning values
   - Explain how each factor contributes to heart disease risk
   - Note any protective factors

3. **Medical Recommendations** (numbered list)
   - Immediate actions if high risk
   - Lifestyle modifications
   - Suggested medical tests or consultations
   - Preventive measures

4. **Patient Education** (1-2 paragraphs)
   - What this result means in simple terms
   - Why these risk factors matter
   - Prognosis and outlook

Keep the tone professional yet compassionate. Use medical terminology but explain it clearly. Focus on actionable advice.

**IMPORTANT:** This is an AI assessment tool, NOT a medical diagnosis. Always emphasize that patients should consult healthcare professionals for proper diagnosis and treatment."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "system",
                        "content": "You are a knowledgeable cardiologist providing detailed medical explanations. Be thorough, accurate, and compassionate."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                model=self.model,
                temperature=0.3,  # Lower temperature for more consistent medical advice
                max_tokens=2000,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error generating explanation: {str(e)}\n\nPlease ensure your Groq API key is valid."

    def generate_risk_factors_analysis(self, features: List[float]) -> str:
        """Generate focused analysis of risk factors"""
        patient_data = self.format_patient_data(features)

        prompt = f"""As a cardiovascular specialist, analyze these patient metrics and identify the most significant risk factors:

{patient_data}

Provide:
1. Top 3 most concerning risk factors
2. Brief explanation of each
3. Normal/optimal ranges for comparison

Be concise and medical-focused."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a cardiologist analyzing risk factors."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.2,
                max_tokens=500,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"

    def generate_lifestyle_recommendations(self, features: List[float], risk_level: str) -> str:
        """Generate personalized lifestyle recommendations"""

        prompt = f"""Based on a patient with {risk_level} cardiovascular risk, provide 5-7 specific, actionable lifestyle recommendations.

Consider:
- Diet modifications
- Exercise guidelines
- Stress management
- Sleep hygiene
- Substance use (smoking, alcohol)
- Regular monitoring

Format as a numbered list with brief explanations."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a preventive cardiology specialist."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.4,
                max_tokens=800,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"

    def compare_with_guidelines(self, features: List[float]) -> str:
        """Compare patient metrics with clinical guidelines"""
        patient_data = self.format_patient_data(features)

        prompt = f"""Compare this patient's values against standard cardiovascular health guidelines (AHA/ACC):

{patient_data}

For each key metric, state:
- Current value
- Recommended range
- Whether it's optimal, borderline, or concerning

Be specific with numbers and guidelines."""

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a clinical guidelines expert."},
                    {"role": "user", "content": prompt}
                ],
                model=self.model,
                temperature=0.1,
                max_tokens=1000,
            )

            return chat_completion.choices[0].message.content

        except Exception as e:
            return f"Error: {str(e)}"


def test_explainer():
    """Test the medical explainer"""
    # Example patient data
    test_features = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]

    try:
        explainer = MedicalExplainer()

        print("Testing Medical Explainer with Groq API...")
        print("=" * 80)

        explanation = explainer.explain_prediction(
            features=test_features,
            prediction=1,
            probability=0.85,
            risk_level="High Risk",
            model_name="Decision Tree (Gini)"
        )

        print(explanation)
        print("\n" + "=" * 80)
        print("Test completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set your Groq API key:")
        print("export GROQ_API_KEY='your-api-key-here'")
        print("\nGet your free API key at: https://console.groq.com/keys")


if __name__ == "__main__":
    test_explainer()
