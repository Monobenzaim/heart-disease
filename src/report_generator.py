"""
PDF Report Generator for Heart Disease Predictions
Creates professional medical reports with AI explanations
"""

from datetime import datetime
from typing import Dict, List, Optional
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, Image, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfgen import canvas
import matplotlib.pyplot as plt
import io
from pathlib import Path


class MedicalReportGenerator:
    """Generate professional PDF medical reports"""

    # Feature names mapping
    FEATURE_NAMES = {
        'age': 'Age (years)',
        'sex': 'Sex',
        'cp': 'Chest Pain Type',
        'trestbps': 'Resting Blood Pressure (mm Hg)',
        'chol': 'Cholesterol (mg/dl)',
        'fbs': 'Fasting Blood Sugar > 120 mg/dl',
        'restecg': 'Resting ECG',
        'thalach': 'Maximum Heart Rate',
        'exang': 'Exercise Induced Angina',
        'oldpeak': 'ST Depression',
        'slope': 'Slope of Peak Exercise ST',
        'ca': 'Major Vessels (0-4)',
        'thal': 'Thalassemia'
    }

    def __init__(self, output_dir: str = "reports"):
        """Initialize report generator"""
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def _create_gauge_chart(self, probability: float) -> io.BytesIO:
        """Create a gauge chart for probability"""
        fig, ax = plt.subplots(figsize=(6, 3))

        # Create the gauge
        colors_list = ['#90EE90', '#FFD700', '#FFA500', '#FF6347']
        ranges = [0.3, 0.6, 0.8, 1.0]

        # Draw colored segments
        theta = 180 * probability
        for i, (r, c) in enumerate(zip(ranges, colors_list)):
            start = ranges[i-1] * 180 if i > 0 else 0
            end = r * 180
            wedge = plt.matplotlib.patches.Wedge(
                (0.5, 0), 0.4, start, end,
                facecolor=c, edgecolor='white', linewidth=2
            )
            ax.add_patch(wedge)

        # Draw needle
        needle_angle = theta * 3.14159 / 180
        ax.plot([0.5, 0.5 + 0.35 * np.cos(needle_angle)],
                [0, 0.35 * np.sin(needle_angle)],
                'k-', linewidth=3)

        # Text
        ax.text(0.5, -0.15, f'{probability:.1%}', ha='center', fontsize=16, fontweight='bold')

        ax.set_xlim(0, 1)
        ax.set_ylim(-0.2, 0.5)
        ax.axis('off')

        plt.tight_layout()

        # Save to bytes
        buf = io.BytesIO()
        plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
        buf.seek(0)
        plt.close()

        return buf

    def _get_risk_color(self, risk_level: str) -> colors.Color:
        """Get color based on risk level"""
        risk_colors = {
            "Low Risk": colors.green,
            "Moderate Risk": colors.orange,
            "High Risk": colors.orangered,
            "Very High Risk": colors.red
        }
        return risk_colors.get(risk_level, colors.grey)

    def generate_report(
        self,
        patient_info: Dict,
        features: List[float],
        prediction_result: Dict,
        llm_explanation: Optional[str] = None,
        model_name: str = "Decision Tree",
        doctor_name: Optional[str] = None,
        hospital_name: Optional[str] = None
    ) -> str:
        """
        Generate comprehensive PDF report

        Args:
            patient_info: Dict with patient details (name, age, id, etc.)
            features: List of 13 clinical features
            prediction_result: Dict from predict.explain_prediction()
            llm_explanation: AI-generated medical explanation
            model_name: Name of ML model used
            doctor_name: Ordering physician name
            hospital_name: Medical facility name

        Returns:
            Path to generated PDF file
        """
        # Generate filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        patient_id = patient_info.get('id', 'UNKNOWN')
        filename = f"heart_disease_report_{patient_id}_{timestamp}.pdf"
        filepath = self.output_dir / filename

        # Create PDF document
        doc = SimpleDocTemplate(
            str(filepath),
            pagesize=letter,
            rightMargin=0.75*inch,
            leftMargin=0.75*inch,
            topMargin=0.75*inch,
            bottomMargin=0.75*inch
        )

        # Container for elements
        elements = []
        styles = getSampleStyleSheet()

        # Custom styles
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        )

        heading_style = ParagraphStyle(
            'CustomHeading',
            parent=styles['Heading2'],
            fontSize=14,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=10,
            spaceBefore=12,
            fontName='Helvetica-Bold'
        )

        # Header
        elements.append(Paragraph("CARDIOVASCULAR RISK ASSESSMENT REPORT", title_style))
        elements.append(Spacer(1, 0.2*inch))

        # Medical facility info
        if hospital_name:
            elements.append(Paragraph(f"<b>{hospital_name}</b>", styles['Normal']))
        elements.append(Paragraph(f"Report Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}", styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))

        # Patient Information Section
        elements.append(Paragraph("PATIENT INFORMATION", heading_style))

        patient_data = [
            ['Patient Name:', patient_info.get('name', 'N/A')],
            ['Patient ID:', patient_info.get('id', 'N/A')],
            ['Date of Birth:', patient_info.get('dob', 'N/A')],
            ['Age:', f"{patient_info.get('age', 'N/A')} years"],
            ['Sex:', patient_info.get('sex', 'N/A')],
        ]

        if doctor_name:
            patient_data.append(['Ordering Physician:', doctor_name])

        patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
        patient_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
        ]))
        elements.append(patient_table)
        elements.append(Spacer(1, 0.3*inch))

        # Prediction Results Section
        elements.append(Paragraph("PREDICTION RESULTS", heading_style))

        prediction = prediction_result['prediction']
        probability = prediction_result['disease_probability']
        risk_level = prediction_result['risk_level']
        risk_color = self._get_risk_color(risk_level)

        # Result summary box
        result_data = [
            ['Prediction:', prediction],
            ['Disease Probability:', f"{probability:.1%}"],
            ['Risk Level:', risk_level],
            ['Model Used:', model_name],
            ['Confidence:', f"{prediction_result['confidence']:.1%}"]
        ]

        result_table = Table(result_data, colWidths=[2*inch, 4*inch])
        result_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('BACKGROUND', (1, 2), (1, 2), risk_color),
            ('TEXTCOLOR', (1, 2), (1, 2), colors.white),
            ('ALIGN', (1, 2), (1, 2), 'CENTER'),
            ('FONTNAME', (1, 2), (1, 2), 'Helvetica-Bold'),
        ]))
        elements.append(result_table)
        elements.append(Spacer(1, 0.3*inch))

        # Clinical Parameters Section
        elements.append(Paragraph("CLINICAL PARAMETERS", heading_style))

        feature_names = ['age', 'sex', 'cp', 'trestbps', 'chol', 'fbs',
                        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal']

        # Format feature values
        formatted_features = []
        for name, value in zip(feature_names, features):
            display_name = self.FEATURE_NAMES.get(name, name)
            formatted_value = self._format_feature_value(name, value)
            formatted_features.append([display_name, formatted_value])

        # Split into two columns
        half = len(formatted_features) // 2
        col1 = formatted_features[:half]
        col2 = formatted_features[half:]

        clinical_data = []
        for i in range(max(len(col1), len(col2))):
            row = []
            if i < len(col1):
                row.extend(col1[i])
            else:
                row.extend(['', ''])
            if i < len(col2):
                row.extend(col2[i])
            else:
                row.extend(['', ''])
            clinical_data.append(row)

        clinical_table = Table(clinical_data, colWidths=[1.5*inch, 1.3*inch, 1.5*inch, 1.3*inch])
        clinical_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (2, 0), (2, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (2, 0), (2, -1), colors.HexColor('#667eea')),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        elements.append(clinical_table)
        elements.append(Spacer(1, 0.3*inch))

        # AI Medical Explanation Section
        if llm_explanation:
            elements.append(PageBreak())
            elements.append(Paragraph("AI-POWERED MEDICAL ANALYSIS", heading_style))

            explanation_style = ParagraphStyle(
                'Explanation',
                parent=styles['BodyText'],
                fontSize=10,
                alignment=TA_JUSTIFY,
                spaceAfter=10
            )

            # Split explanation into paragraphs
            paragraphs = llm_explanation.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    # Handle markdown-style bold
                    para = para.replace('**', '<b>').replace('**', '</b>')
                    elements.append(Paragraph(para, explanation_style))
                    elements.append(Spacer(1, 0.1*inch))

        # Disclaimer Section
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("IMPORTANT DISCLAIMER", heading_style))

        disclaimer_text = """
        <b>This report is generated by an AI-assisted cardiovascular risk assessment system and is intended
        for informational and educational purposes only.</b> This is NOT a medical diagnosis and should NOT
        be used as a substitute for professional medical advice, diagnosis, or treatment.
        <br/><br/>
        The predictions and recommendations provided are based on machine learning algorithms and should be
        interpreted by qualified healthcare professionals. Always seek the advice of your physician or other
        qualified health provider with any questions regarding a medical condition.
        <br/><br/>
        <b>Recommended Actions:</b><br/>
        • Consult with a cardiologist for comprehensive evaluation<br/>
        • Schedule appropriate diagnostic tests (ECG, stress test, angiography as needed)<br/>
        • Discuss treatment options with your healthcare provider<br/>
        • Follow prescribed medication and lifestyle recommendations
        """

        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['BodyText'],
            fontSize=9,
            textColor=colors.grey,
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20
        )

        elements.append(Paragraph(disclaimer_text, disclaimer_style))

        # Footer
        elements.append(Spacer(1, 0.3*inch))
        footer_style = ParagraphStyle(
            'Footer',
            parent=styles['Normal'],
            fontSize=8,
            textColor=colors.grey,
            alignment=TA_CENTER
        )
        elements.append(Paragraph(
            f"Report ID: {patient_id}_{timestamp} | Generated by Heart Disease Prediction System v1.0",
            footer_style
        ))

        # Build PDF
        doc.build(elements)

        return str(filepath)

    def _format_feature_value(self, feature_name: str, value: float) -> str:
        """Format feature value for display"""
        if feature_name == 'sex':
            return 'Male' if value == 1 else 'Female'
        elif feature_name == 'cp':
            cp_types = ['Typical Angina', 'Atypical Angina', 'Non-Anginal', 'Asymptomatic']
            return cp_types[int(value)] if 0 <= value < len(cp_types) else str(value)
        elif feature_name == 'fbs':
            return 'Yes' if value == 1 else 'No'
        elif feature_name == 'restecg':
            ecg_types = ['Normal', 'ST-T Abnormality', 'LV Hypertrophy']
            return ecg_types[int(value)] if 0 <= value < len(ecg_types) else str(value)
        elif feature_name == 'exang':
            return 'Yes' if value == 1 else 'No'
        elif feature_name == 'slope':
            slope_types = ['Upsloping', 'Flat', 'Downsloping']
            return slope_types[int(value)] if 0 <= value < len(slope_types) else str(value)
        elif feature_name == 'thal':
            thal_types = ['Normal', 'Fixed Defect', 'Reversible Defect', 'Unknown']
            return thal_types[int(value)] if 0 <= value < len(thal_types) else str(value)
        elif feature_name == 'oldpeak':
            return f"{value:.1f}"
        else:
            return str(int(value)) if value == int(value) else f"{value:.1f}"


# For numpy import
import numpy as np


if __name__ == "__main__":
    # Test report generation
    print("Testing PDF Report Generator...")

    generator = MedicalReportGenerator()

    # Sample data
    patient_info = {
        'name': 'John Doe',
        'id': 'P123456',
        'dob': 'January 15, 1960',
        'age': 63,
        'sex': 'Male'
    }

    features = [63, 1, 3, 145, 233, 1, 0, 150, 0, 2.3, 0, 0, 1]

    prediction_result = {
        'prediction': 'Disease Detected',
        'prediction_value': 1,
        'disease_probability': 0.85,
        'risk_level': 'High Risk',
        'confidence': 0.85
    }

    llm_explanation = """
    **Clinical Summary:**
    This 63-year-old male patient presents with multiple cardiovascular risk factors including
    elevated cholesterol, reduced exercise tolerance, and concerning ECG findings.

    **Risk Factor Analysis:**
    • Cholesterol level of 233 mg/dl is above optimal range
    • Maximum heart rate of 150 suggests reduced cardiovascular fitness
    • ST depression of 2.3 indicates potential ischemia
    """

    filepath = generator.generate_report(
        patient_info=patient_info,
        features=features,
        prediction_result=prediction_result,
        llm_explanation=llm_explanation,
        model_name="Decision Tree (Gini)",
        doctor_name="Dr. Sarah Johnson",
        hospital_name="Metropolitan Heart Center"
    )

    print(f"Report generated successfully: {filepath}")
