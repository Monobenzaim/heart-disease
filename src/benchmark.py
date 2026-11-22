"""
Comprehensive Model Benchmarking for Medical AI
Compares multiple ML models with detailed metrics and medical interpretation focus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import json
from datetime import datetime
import joblib

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    roc_auc_score, roc_curve, confusion_matrix, classification_report,
    matthews_corrcoef, cohen_kappa_score, balanced_accuracy_score,
    average_precision_score, log_loss
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
import time


class MedicalModelBenchmark:
    """Comprehensive benchmarking suite for medical AI models"""

    def __init__(self, data_path: str, test_size: float = 0.2, random_state: int = 42):
        """
        Initialize benchmark

        Args:
            data_path: Path to heart disease dataset
            test_size: Proportion of test set
            random_state: Random seed for reproducibility
        """
        self.data_path = data_path
        self.test_size = test_size
        self.random_state = random_state
        self.results = {}

        # Load and prepare data
        self._load_data()

    def _load_data(self):
        """Load and prepare dataset"""
        print("Loading dataset...")
        df = pd.read_csv(self.data_path)

        X = df.drop(columns=["target"])
        y = df["target"]

        # Split data
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=self.test_size, random_state=self.random_state, stratify=y
        )

        # Scale features
        self.scaler = StandardScaler()
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)

        print(f"Dataset loaded: {len(X)} samples")
        print(f"Training set: {len(self.X_train)} | Test set: {len(self.X_test)}")
        print(f"Class distribution - Disease: {y.sum()} | No Disease: {len(y) - y.sum()}")
        print()

    def _get_models(self):
        """Define models to benchmark"""
        models = {
            # Decision Trees
            'Decision Tree (Gini)': DecisionTreeClassifier(
                criterion='gini',
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state
            ),
            'Decision Tree (Entropy)': DecisionTreeClassifier(
                criterion='entropy',
                max_depth=10,
                min_samples_split=5,
                min_samples_leaf=2,
                random_state=self.random_state
            ),

            # Ensemble Methods
            'Random Forest': RandomForestClassifier(
                n_estimators=100,
                max_depth=20,
                min_samples_split=5,
                criterion='gini',
                random_state=self.random_state,
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100,
                learning_rate=0.1,
                max_depth=5,
                random_state=self.random_state
            ),

            # Linear Models
            'Logistic Regression': LogisticRegression(
                C=1.0,
                penalty='l2',
                solver='liblinear',
                max_iter=1000,
                random_state=self.random_state
            ),

            # Support Vector Machine
            'SVM (RBF)': SVC(
                kernel='rbf',
                C=1.0,
                gamma='scale',
                probability=True,
                random_state=self.random_state
            ),

            # Naive Bayes
            'Naive Bayes': GaussianNB()
        }

        return models

    def _calculate_medical_metrics(self, y_true, y_pred, y_prob):
        """
        Calculate comprehensive metrics relevant for medical AI

        Args:
            y_true: True labels
            y_pred: Predicted labels
            y_prob: Predicted probabilities

        Returns:
            Dictionary of metrics
        """
        # Confusion matrix components
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred).ravel()

        metrics = {
            # Basic Metrics
            'accuracy': accuracy_score(y_true, y_pred),
            'balanced_accuracy': balanced_accuracy_score(y_true, y_pred),

            # Medical Diagnostic Metrics
            'sensitivity_recall': recall_score(y_true, y_pred),  # True Positive Rate
            'specificity': tn / (tn + fp),  # True Negative Rate
            'precision_ppv': precision_score(y_true, y_pred),  # Positive Predictive Value
            'npv': tn / (tn + fn),  # Negative Predictive Value

            # Additional Performance Metrics
            'f1_score': f1_score(y_true, y_pred),
            'roc_auc': roc_auc_score(y_true, y_prob),
            'pr_auc': average_precision_score(y_true, y_prob),
            'mcc': matthews_corrcoef(y_true, y_pred),  # Matthews Correlation Coefficient
            'cohen_kappa': cohen_kappa_score(y_true, y_pred),
            'log_loss': log_loss(y_true, y_prob),

            # Confusion Matrix Components
            'true_positives': int(tp),
            'true_negatives': int(tn),
            'false_positives': int(fp),
            'false_negatives': int(fn),

            # Medical Decision Metrics
            'false_positive_rate': fp / (fp + tn),
            'false_negative_rate': fn / (fn + tp),
            'diagnostic_odds_ratio': (tp * tn) / (fp * fn) if (fp * fn) > 0 else np.inf,

            # Youden's Index (optimal threshold)
            'youdens_index': (tp / (tp + fn)) + (tn / (tn + fp)) - 1
        }

        return metrics

    def benchmark_model(self, model_name: str, model, use_scaled: bool = True):
        """
        Benchmark a single model

        Args:
            model_name: Name of the model
            model: Scikit-learn model instance
            use_scaled: Whether to use scaled features
        """
        print(f"\nBenchmarking: {model_name}")
        print("-" * 60)

        X_train = self.X_train_scaled if use_scaled else self.X_train
        X_test = self.X_test_scaled if use_scaled else self.X_test

        # Training
        start_time = time.time()
        model.fit(X_train, self.y_train)
        training_time = time.time() - start_time

        # Prediction
        start_time = time.time()
        y_pred = model.predict(X_test)
        prediction_time = time.time() - start_time

        # Probabilities
        if hasattr(model, 'predict_proba'):
            y_prob = model.predict_proba(X_test)[:, 1]
        elif hasattr(model, 'decision_function'):
            # Normalize decision function to [0, 1]
            decision = model.decision_function(X_test)
            y_prob = (decision - decision.min()) / (decision.max() - decision.min())
        else:
            y_prob = y_pred.astype(float)

        # Calculate metrics
        metrics = self._calculate_medical_metrics(self.y_test, y_pred, y_prob)

        # Cross-validation
        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=self.random_state)
        cv_scores = cross_val_score(model, X_train, self.y_train, cv=cv, scoring='roc_auc', n_jobs=-1)

        # Store results
        self.results[model_name] = {
            'metrics': metrics,
            'training_time': training_time,
            'prediction_time': prediction_time,
            'predictions_per_second': len(X_test) / prediction_time,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std(),
            'y_pred': y_pred,
            'y_prob': y_prob,
            'model': model
        }

        # Print key metrics
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"Sensitivity (Recall): {metrics['sensitivity_recall']:.4f}")
        print(f"Specificity: {metrics['specificity']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        print(f"Training Time: {training_time:.3f}s")
        print(f"CV Score: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

    def run_all_benchmarks(self):
        """Run benchmarks for all models"""
        print("=" * 80)
        print("COMPREHENSIVE MODEL BENCHMARKING FOR MEDICAL AI")
        print("=" * 80)
        print(f"Dataset: {self.data_path}")
        print(f"Test Size: {self.test_size}")
        print(f"Random State: {self.random_state}")
        print("=" * 80)

        models = self._get_models()

        for model_name, model in models.items():
            # Determine if model needs scaling
            use_scaled = model_name not in ['Decision Tree (Gini)', 'Decision Tree (Entropy)',
                                           'Random Forest', 'Gradient Boosting', 'Naive Bayes']
            self.benchmark_model(model_name, model, use_scaled)

        print("\n" + "=" * 80)
        print("BENCHMARKING COMPLETE!")
        print("=" * 80)

    def generate_comparison_report(self, output_dir: str = "benchmark_results"):
        """Generate comprehensive comparison report"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # 1. Metrics Comparison Table
        print("\n" + "=" * 80)
        print("COMPREHENSIVE METRICS COMPARISON")
        print("=" * 80)

        metrics_df = pd.DataFrame({
            model_name: result['metrics']
            for model_name, result in self.results.items()
        }).T

        # Sort by ROC-AUC
        metrics_df = metrics_df.sort_values('roc_auc', ascending=False)

        print("\n📊 KEY PERFORMANCE METRICS:")
        print(metrics_df[['accuracy', 'sensitivity_recall', 'specificity', 'roc_auc', 'f1_score']].to_string())

        print("\n🏥 MEDICAL DIAGNOSTIC METRICS:")
        print(metrics_df[['precision_ppv', 'npv', 'false_positive_rate', 'false_negative_rate']].to_string())

        # Save to CSV
        metrics_df.to_csv(output_path / f"metrics_comparison_{timestamp}.csv")

        # 2. Best Model Analysis
        print("\n" + "=" * 80)
        print("🏆 BEST MODEL ANALYSIS")
        print("=" * 80)

        # Find best models for different criteria
        best_overall = metrics_df['roc_auc'].idxmax()
        best_sensitivity = metrics_df['sensitivity_recall'].idxmax()
        best_specificity = metrics_df['specificity'].idxmax()
        best_accuracy = metrics_df['accuracy'].idxmax()
        fastest_training = min(self.results.items(), key=lambda x: x[1]['training_time'])[0]

        print(f"\n✓ Best Overall (ROC-AUC): {best_overall} ({metrics_df.loc[best_overall, 'roc_auc']:.4f})")
        print(f"✓ Best Sensitivity: {best_sensitivity} ({metrics_df.loc[best_sensitivity, 'sensitivity_recall']:.4f})")
        print(f"✓ Best Specificity: {best_specificity} ({metrics_df.loc[best_specificity, 'specificity']:.4f})")
        print(f"✓ Best Accuracy: {best_accuracy} ({metrics_df.loc[best_accuracy, 'accuracy']:.4f})")
        print(f"✓ Fastest Training: {fastest_training} ({self.results[fastest_training]['training_time']:.3f}s)")

        # 3. Medical Interpretation Recommendation
        print("\n" + "=" * 80)
        print("🏥 RECOMMENDATION FOR MEDICAL USE")
        print("=" * 80)

        # Score models based on medical criteria
        medical_scores = {}
        for model_name, result in self.results.items():
            m = result['metrics']
            # Weighted scoring for medical use
            # High sensitivity (avoid missing diseases)
            # High specificity (avoid false alarms)
            # Good overall performance
            score = (
                m['sensitivity_recall'] * 0.35 +  # Very important: catch diseases
                m['specificity'] * 0.25 +  # Important: avoid false positives
                m['roc_auc'] * 0.25 +  # Overall discrimination
                m['balanced_accuracy'] * 0.15  # Balance
            )
            medical_scores[model_name] = score

        recommended_model = max(medical_scores.items(), key=lambda x: x[1])[0]
        print(f"\n🎯 RECOMMENDED MODEL: {recommended_model}")
        print(f"   Medical Score: {medical_scores[recommended_model]:.4f}")

        result = self.results[recommended_model]
        m = result['metrics']

        print(f"\n   Key Characteristics:")
        print(f"   • Sensitivity: {m['sensitivity_recall']:.1%} (catches {m['sensitivity_recall']:.1%} of actual diseases)")
        print(f"   • Specificity: {m['specificity']:.1%} (correctly identifies {m['specificity']:.1%} of healthy patients)")
        print(f"   • ROC-AUC: {m['roc_auc']:.4f}")
        print(f"   • False Negatives: {m['false_negatives']} (missed cases)")
        print(f"   • False Positives: {m['false_positives']} (false alarms)")

        # 4. Generate Visualizations
        self._generate_visualizations(output_path, timestamp)

        # 5. Save detailed JSON report
        json_report = {
            'timestamp': timestamp,
            'dataset': str(self.data_path),
            'test_size': self.test_size,
            'recommended_model': recommended_model,
            'medical_scores': medical_scores,
            'best_models': {
                'overall': best_overall,
                'sensitivity': best_sensitivity,
                'specificity': best_specificity,
                'accuracy': best_accuracy,
                'fastest': fastest_training
            },
            'model_metrics': {
                model_name: {k: float(v) if isinstance(v, (np.floating, np.integer)) else v
                           for k, v in result['metrics'].items()}
                for model_name, result in self.results.items()
            }
        }

        with open(output_path / f"benchmark_report_{timestamp}.json", 'w') as f:
            json.dump(json_report, f, indent=2)

        print(f"\n📁 Results saved to: {output_path}")

    def _generate_visualizations(self, output_path: Path, timestamp: str):
        """Generate comparison visualizations"""
        print("\n📊 Generating visualizations...")

        # Set style
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 10)

        # 1. ROC Curves
        fig, axes = plt.subplots(2, 2, figsize=(16, 14))

        # ROC Curves comparison
        ax = axes[0, 0]
        for model_name, result in self.results.items():
            fpr, tpr, _ = roc_curve(self.y_test, result['y_prob'])
            auc = result['metrics']['roc_auc']
            ax.plot(fpr, tpr, label=f"{model_name} (AUC={auc:.3f})", linewidth=2)

        ax.plot([0, 1], [0, 1], 'k--', label='Random')
        ax.set_xlabel('False Positive Rate')
        ax.set_ylabel('True Positive Rate')
        ax.set_title('ROC Curves Comparison')
        ax.legend()
        ax.grid(True, alpha=0.3)

        # Metrics comparison bar chart
        ax = axes[0, 1]
        metrics_to_plot = ['accuracy', 'sensitivity_recall', 'specificity', 'f1_score']
        metrics_df = pd.DataFrame({
            model_name: [result['metrics'][m] for m in metrics_to_plot]
            for model_name, result in self.results.items()
        }, index=metrics_to_plot)

        metrics_df.T.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title('Performance Metrics Comparison')
        ax.set_ylabel('Score')
        ax.set_xlabel('Model')
        ax.legend(title='Metrics')
        ax.set_ylim([0, 1.1])
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

        # Training time comparison
        ax = axes[1, 0]
        training_times = {name: result['training_time'] for name, result in self.results.items()}
        ax.bar(range(len(training_times)), list(training_times.values()), color='skyblue')
        ax.set_xticks(range(len(training_times)))
        ax.set_xticklabels(list(training_times.keys()), rotation=45, ha='right')
        ax.set_ylabel('Time (seconds)')
        ax.set_title('Training Time Comparison')
        ax.grid(True, alpha=0.3)

        # Sensitivity vs Specificity scatter
        ax = axes[1, 1]
        sensitivities = [result['metrics']['sensitivity_recall'] for result in self.results.values()]
        specificities = [result['metrics']['specificity'] for result in self.results.values()]
        model_names = list(self.results.keys())

        scatter = ax.scatter(specificities, sensitivities, s=200, alpha=0.6, c=range(len(model_names)), cmap='viridis')
        for i, name in enumerate(model_names):
            ax.annotate(name, (specificities[i], sensitivities[i]),
                       xytext=(5, 5), textcoords='offset points', fontsize=8)

        ax.set_xlabel('Specificity (True Negative Rate)')
        ax.set_ylabel('Sensitivity (True Positive Rate)')
        ax.set_title('Sensitivity vs Specificity Trade-off')
        ax.grid(True, alpha=0.3)
        ax.plot([0, 1], [1, 0], 'r--', alpha=0.3, label='Trade-off line')

        plt.tight_layout()
        plt.savefig(output_path / f"model_comparison_{timestamp}.png", dpi=300, bbox_inches='tight')
        plt.close()

        # 2. Confusion Matrices
        n_models = len(self.results)
        fig, axes = plt.subplots((n_models + 1) // 2, 2, figsize=(14, 4 * ((n_models + 1) // 2)))
        axes = axes.flatten() if n_models > 1 else [axes]

        for idx, (model_name, result) in enumerate(self.results.items()):
            cm = confusion_matrix(self.y_test, result['y_pred'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=['No Disease', 'Disease'],
                       yticklabels=['No Disease', 'Disease'])
            axes[idx].set_title(f'{model_name}\nAccuracy: {result["metrics"]["accuracy"]:.3f}')
            axes[idx].set_ylabel('True Label')
            axes[idx].set_xlabel('Predicted Label')

        # Hide extra subplots
        for idx in range(len(self.results), len(axes)):
            axes[idx].axis('off')

        plt.tight_layout()
        plt.savefig(output_path / f"confusion_matrices_{timestamp}.png", dpi=300, bbox_inches='tight')
        plt.close()

        print("✓ Visualizations saved!")


if __name__ == "__main__":
    # Run comprehensive benchmark
    print("Starting Comprehensive Medical AI Benchmark...\n")

    benchmark = MedicalModelBenchmark(
        data_path="../data/heart.csv",
        test_size=0.2,
        random_state=42
    )

    # Run all benchmarks
    benchmark.run_all_benchmarks()

    # Generate report
    benchmark.generate_comparison_report()

    print("\n✓ Benchmark complete! Check 'benchmark_results/' for detailed reports.")
