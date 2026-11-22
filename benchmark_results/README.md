# Benchmark Results Directory

This directory contains model comparison and evaluation results.

## What Gets Stored Here

- **CSV files**: Detailed metrics comparison tables
- **PNG files**: Visualization charts (ROC curves, confusion matrices, etc.)
- **JSON files**: Complete benchmark reports

## Generated Files

After running benchmarks, you'll find:

```
benchmark_results/
├── metrics_comparison_YYYYMMDD_HHMMSS.csv
├── model_comparison_YYYYMMDD_HHMMSS.png
├── confusion_matrices_YYYYMMDD_HHMMSS.png
└── benchmark_report_YYYYMMDD_HHMMSS.json
```

## Usage

Run benchmarks using:

**Method 1 - Web App:**
```bash
streamlit run app_enhanced.py
# Go to "Benchmarks" tab → Click "Run Complete Benchmark"
```

**Method 2 - Command Line:**
```bash
cd src
python benchmark.py
```

## Git Ignore

Result files are ignored by `.gitignore` because they:
- Can be large (especially PNG files)
- Can be regenerated anytime
- May vary based on random seed
- Should be generated fresh for each analysis

## For Thesis/Publication

To include results in your thesis:
1. Run benchmarks
2. Copy desired files to your thesis directory
3. Reference them in your document
4. Keep originals here for reproducibility

## Reproducibility

To reproduce exact results:
- Use same random seed (42)
- Use same train/test split
- Document software versions
- Save configuration in JSON report
