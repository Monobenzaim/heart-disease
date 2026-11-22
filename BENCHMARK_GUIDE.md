# 📊 Model Benchmarking Guide

## Overview

The comprehensive benchmarking system evaluates all ML models on **medical diagnostic metrics**, helping you choose the best model for clinical use.

## 🎯 Why Medical Benchmarking Matters

Traditional ML metrics (accuracy) aren't enough for medical applications:

### Medical Context
- **Sensitivity (Recall)**: How many actual diseases did we catch?
  - **Critical in medicine**: Missing a disease can be life-threatening
  - Goal: Maximize to avoid false negatives

- **Specificity**: How many healthy patients did we correctly identify?
  - **Important for resources**: False positives waste resources and cause anxiety
  - Goal: Balance with sensitivity

- **PPV (Precision)**: If we predict disease, how likely is it real?
  - **Clinical confidence**: Trust in positive predictions

- **NPV**: If we predict healthy, how likely is it true?
  - **Reassurance value**: Trust in negative predictions

## 🚀 Running the Benchmark

### Method 1: Via Web App (Easiest)

```bash
# Run the enhanced app
streamlit run app_enhanced.py
```

1. Go to "Benchmarks" tab
2. Click "Run Complete Benchmark"
3. Wait 2-5 minutes
4. View results in `benchmark_results/` folder

### Method 2: Command Line

```bash
cd src
python benchmark.py
```

### Method 3: Programmatically

```python
from src.benchmark import MedicalModelBenchmark

# Initialize
benchmark = MedicalModelBenchmark(
    data_path="../data/heart.csv",
    test_size=0.2,
    random_state=42
)

# Run all benchmarks
benchmark.run_all_benchmarks()

# Generate reports
benchmark.generate_comparison_report()
```

## 📊 Models Evaluated

1. **Decision Tree (Gini)** - Fast, interpretable
2. **Decision Tree (Entropy)** - Alternative splitting criterion
3. **Random Forest** - Ensemble method, robust
4. **Gradient Boosting** - Powerful sequential ensemble
5. **Logistic Regression** - Linear baseline, probabilistic
6. **SVM (RBF)** - Non-linear, kernel-based
7. **Naive Bayes** - Probabilistic, fast

## 📈 Metrics Explained

### Basic Performance
| Metric | Description | Medical Importance |
|--------|-------------|-------------------|
| **Accuracy** | Overall correctness | General performance |
| **Balanced Accuracy** | Accuracy adjusted for class imbalance | Fair comparison |

### Medical Diagnostic Metrics
| Metric | Formula | What It Means | Medical Goal |
|--------|---------|---------------|--------------|
| **Sensitivity (TPR)** | TP/(TP+FN) | % of diseases caught | **Maximize** (don't miss diseases) |
| **Specificity (TNR)** | TN/(TN+FP) | % of healthy correctly ID'd | High (reduce false alarms) |
| **Precision (PPV)** | TP/(TP+FP) | Reliability of positive prediction | High confidence |
| **NPV** | TN/(TN+FN) | Reliability of negative prediction | High reassurance |
| **F1-Score** | 2×(Prec×Rec)/(Prec+Rec) | Balance of precision/recall | Balanced performance |

### Advanced Metrics
| Metric | Range | Interpretation |
|--------|-------|----------------|
| **ROC-AUC** | 0-1 | Overall discrimination ability (higher = better) |
| **PR-AUC** | 0-1 | Precision-Recall curve area |
| **MCC** | -1 to 1 | Matthews Correlation (balanced metric) |
| **Cohen's Kappa** | -1 to 1 | Agreement beyond chance |
| **Youden's Index** | 0-1 | Optimal threshold point |

### Medical Decision Metrics
| Metric | Formula | Clinical Meaning |
|--------|---------|------------------|
| **FPR** | FP/(FP+TN) | False alarm rate |
| **FNR** | FN/(FN+TP) | Missed diagnosis rate |
| **DOR** | (TP×TN)/(FP×FN) | Diagnostic odds ratio |

## 📋 Output Files

After running, check `benchmark_results/` for:

### 1. `metrics_comparison_TIMESTAMP.csv`
Detailed metrics for all models in table format

### 2. `model_comparison_TIMESTAMP.png`
Visualizations including:
- ROC curves comparison
- Metrics bar chart
- Training time comparison
- Sensitivity vs Specificity scatter

### 3. `confusion_matrices_TIMESTAMP.png`
Confusion matrices for all models

### 4. `benchmark_report_TIMESTAMP.json`
Complete results in JSON format for programmatic use

## 🏆 Interpreting Results

### Best Model Selection

The benchmark automatically recommends models for:

1. **Best Overall (ROC-AUC)**: Highest discrimination ability
2. **Best Sensitivity**: Catches most diseases (use for screening)
3. **Best Specificity**: Fewest false alarms (use for confirmation)
4. **Best Accuracy**: Highest overall correctness
5. **Fastest Training**: For rapid experimentation

### Medical Use Recommendation

The system calculates a **Medical Score** weighted for clinical use:

```
Medical Score = (
    Sensitivity × 0.35 +      # Very important: catch diseases
    Specificity × 0.25 +      # Important: avoid false positives
    ROC-AUC × 0.25 +          # Overall discrimination
    Balanced Accuracy × 0.15  # Balance
)
```

**Higher medical score = better for clinical deployment**

## 📊 Example Results

```
════════════════════════════════════════════════════════════════
🏆 BEST MODEL ANALYSIS
════════════════════════════════════════════════════════════════

✓ Best Overall (ROC-AUC): Random Forest (0.9342)
✓ Best Sensitivity: Gradient Boosting (0.9123)
✓ Best Specificity: SVM (0.8947)
✓ Best Accuracy: Random Forest (0.8732)
✓ Fastest Training: Decision Tree (Gini) (0.021s)

════════════════════════════════════════════════════════════════
🏥 RECOMMENDATION FOR MEDICAL USE
════════════════════════════════════════════════════════════════

🎯 RECOMMENDED MODEL: Random Forest
   Medical Score: 0.9123

   Key Characteristics:
   • Sensitivity: 89.5% (catches 89.5% of actual diseases)
   • Specificity: 87.2% (correctly identifies 87.2% of healthy patients)
   • ROC-AUC: 0.9342
   • False Negatives: 7 (missed cases)
   • False Positives: 11 (false alarms)
```

## 🎯 Choosing the Right Model

### Scenario-Based Guidance

#### Screening Application (Priority: Catch all diseases)
✅ **Choose**: Model with highest **Sensitivity**
📌 Accept more false positives to catch all diseases
🎯 Examples: Population-wide screening, high-risk groups

#### Diagnostic Confirmation (Priority: High confidence)
✅ **Choose**: Model with highest **Specificity** or **Precision**
📌 Minimize false positives, used after screening
🎯 Examples: Before expensive procedures, treatment decisions

#### Balanced Clinical Use (Priority: Overall performance)
✅ **Choose**: Model with highest **Medical Score** or **ROC-AUC**
📌 Good balance of sensitivity and specificity
🎯 Examples: General clinical decision support

#### Research/Development (Priority: Speed)
✅ **Choose**: **Fastest Training** model
📌 Quick iterations during development
🎯 Examples: Prototyping, testing new features

#### Production Deployment (Priority: Reliability)
✅ **Choose**: **Random Forest** or **Gradient Boosting**
📌 Robust, well-tested, industry standard
🎯 Examples: Real-world clinical use

## 📈 Understanding Trade-offs

### Sensitivity vs Specificity
```
High Sensitivity → More FP (false alarms)
High Specificity → More FN (missed diseases)
```

**Medical Principle**:
> In life-threatening conditions, prioritize Sensitivity
> In chronic/manageable conditions, balance both

### Model Complexity vs Interpretability
```
Simple (Logistic Regression, Decision Tree):
  ✅ Easy to explain
  ✅ Fast
  ❌ May underperform

Complex (Random Forest, Gradient Boosting):
  ✅ Higher performance
  ❌ Harder to interpret
  ❌ Slower
```

## 🎓 For Your Thesis

### Include in Methodology:
"Model selection was performed using comprehensive benchmarking on
medical diagnostic metrics including sensitivity, specificity, ROC-AUC,
and Matthews Correlation Coefficient. Seven algorithms were evaluated
using 5-fold cross-validation on a held-out test set."

### Create Comparison Table:
Copy the CSV results into a formatted table:

| Model | Accuracy | Sensitivity | Specificity | ROC-AUC | F1 |
|-------|----------|-------------|-------------|---------|-----|
| Random Forest | 0.873 | 0.895 | 0.872 | 0.934 | 0.891 |
| ... | ... | ... | ... | ... | ... |

### Visualizations for Thesis:
1. ROC Curves comparison
2. Confusion matrices
3. Sensitivity-Specificity scatter
4. Training time comparison

### Discussion Points:
- Why you chose the final model
- Trade-offs considered
- Medical implications of false positives/negatives
- Comparison with literature

## 💡 Advanced Tips

### Custom Benchmarking

```python
# Add your own model
from your_model import CustomModel

models = benchmark._get_models()
models['My Custom Model'] = CustomModel(...)

# Run specific model
benchmark.benchmark_model('Random Forest', model, use_scaled=True)
```

### Statistical Significance Testing

```python
from scipy import stats

# Compare two models
model1_scores = benchmark.results['Model A']['cv_scores']
model2_scores = benchmark.results['Model B']['cv_scores']

t_stat, p_value = stats.ttest_rel(model1_scores, model2_scores)
print(f"P-value: {p_value}")  # < 0.05 = significant difference
```

### Optimal Threshold Analysis

```python
from sklearn.metrics import roc_curve

fpr, tpr, thresholds = roc_curve(y_test, y_prob)

# Find optimal threshold (Youden's Index)
optimal_idx = np.argmax(tpr - fpr)
optimal_threshold = thresholds[optimal_idx]

print(f"Optimal threshold: {optimal_threshold:.3f}")
```

## 🔧 Customization

### Modify Scoring Weights
Edit in `src/benchmark.py`:

```python
# For screening focus (catch more diseases)
score = (
    m['sensitivity_recall'] * 0.50 +  # Higher weight
    m['specificity'] * 0.20 +
    m['roc_auc'] * 0.20 +
    m['balanced_accuracy'] * 0.10
)
```

### Add Custom Metrics

```python
def _calculate_medical_metrics(self, y_true, y_pred, y_prob):
    # ... existing metrics ...

    # Add your custom metric
    metrics['custom_score'] = your_calculation(y_true, y_pred)

    return metrics
```

## 📚 References

### Medical Metrics
- Altman, D. G., & Bland, J. M. (1994). Diagnostic tests. BMJ.
- Trevethan, R. (2017). Sensitivity, Specificity, and Predictive Values.

### Model Evaluation
- Hastie, T., et al. (2009). The Elements of Statistical Learning.
- James, G., et al. (2013). An Introduction to Statistical Learning.

## ⚠️ Important Notes

1. **Stratified Sampling**: Benchmarking uses stratified splits to maintain class balance
2. **Random State**: Set to 42 for reproducibility
3. **Cross-Validation**: 5-fold CV used for robust estimates
4. **Scaling**: Applied appropriately per model type
5. **Class Imbalance**: Handled with balanced accuracy metric

## 🚀 Next Steps

1. ✅ Run the benchmark
2. ✅ Analyze results
3. ✅ Choose best model for your use case
4. ✅ Include in thesis
5. ✅ Document your choice
6. ✅ Deploy to production (optional)

---

**Comprehensive benchmarking = Strong thesis! 📊**

For questions: Review the code or check scikit-learn docs
