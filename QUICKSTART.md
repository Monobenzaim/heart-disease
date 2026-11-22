# 🚀 Quick Start Guide

Get up and running with Heart Disease Prediction in 5 minutes!

## Prerequisites

- Python 3.8 or higher installed
- Basic command line knowledge

## Step 1: Clone or Download

```bash
# If you're cloning from GitHub
git clone https://github.com/yourusername/heart-disease-prediction.git
cd heart-disease-prediction

# Or if you downloaded a ZIP file, extract it and navigate to the folder
cd heart-disease-prediction
```

## Step 2: Set Up Virtual Environment

### Windows
```bash
python -m venv venv
venv\Scripts\activate
```

### Mac/Linux
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` at the beginning of your command line.

## Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

This will install all required packages (takes ~2-5 minutes).

## Step 4: Train the Models

```bash
cd src
python train.py
cd ..
```

This will:
- Load the heart disease dataset
- Train multiple ML models
- Save them to the `models/` folder
- Takes ~5-10 minutes depending on your computer

## Step 5: Run the Web App

```bash
streamlit run app.py
```

The app will automatically open in your browser at `http://localhost:8501`

If it doesn't open automatically, manually navigate to: http://localhost:8501

## 🎉 You're Done!

You should now see the Heart Disease Prediction web interface!

## Usage Tips

1. **Making Predictions**:
   - Go to the "Prediction" tab
   - Adjust the sliders for patient information
   - Click "Predict Heart Disease Risk"

2. **Exploring Data**:
   - Check out the "Data Explorer" tab
   - View dataset statistics and distributions

3. **Learning More**:
   - Visit the "Information" tab
   - Learn about each clinical feature

## Troubleshooting

### "Module not found" error
```bash
# Make sure virtual environment is activated
# Then reinstall dependencies
pip install -r requirements.txt
```

### "Models not found" error
```bash
# Train the models first
cd src
python train.py
cd ..
```

### Port already in use
```bash
# Use a different port
streamlit run app.py --server.port 8502
```

### Python version error
```bash
# Check your Python version
python --version

# Should be 3.8 or higher
```

## Need Help?

- Check the full [README.md](README.md) for detailed documentation
- Open an issue on GitHub
- Review the code in `src/` directory for examples

## Next Steps

- Customize the models in `src/train.py`
- Modify the UI in `app.py`
- Add your own datasets in `data/`
- Deploy to Streamlit Cloud (free!)

Happy Predicting! ❤️
