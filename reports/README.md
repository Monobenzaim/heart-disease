# Reports Directory

This directory contains generated PDF reports.

## ⚠️ SECURITY WARNING

**DO NOT commit patient reports to Git!**

This directory is ignored by `.gitignore` to protect patient privacy and comply with data protection regulations.

## What Gets Stored Here

- PDF medical reports with patient information
- JSON exports with prediction details
- CSV files with batch predictions

## Usage

Reports are automatically saved here when you:
1. Use the "Generate PDF Report" feature in the web app
2. Run `report_generator.py` programmatically

## File Naming Convention

```
heart_disease_report_<patient_id>_<timestamp>.pdf
```

Example: `heart_disease_report_P123456_20261122_153045.pdf`

## Privacy & Compliance

- All files in this directory are automatically ignored by Git
- Never commit files containing patient information
- Delete old reports regularly
- Encrypt reports when sharing electronically
- Follow HIPAA/GDPR guidelines if applicable

## For Development/Demo

If you need sample reports for demonstration:
1. Use fake patient data
2. Use patient ID: "DEMO123"
3. Clearly label as "SAMPLE" or "DEMONSTRATION"
