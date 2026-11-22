"""
Heart Disease Prediction Model Training Script
This script trains multiple machine learning models for heart disease prediction.
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve
)
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression


class HeartDiseaseTrainer:
    """Train and evaluate heart disease prediction models"""

    def __init__(self, data_path: str):
        """Initialize trainer with data path"""
        self.data_path = data_path
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        self.scaler = StandardScaler()
        self.models = {}

    def load_data(self):
        """Load and prepare the dataset"""
        print("Loading data...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset shape: {self.df.shape}")
        print(f"Missing values: {self.df.isnull().sum().sum()}")
        return self.df

    def prepare_data(self, test_size=0.2, random_state=42):
        """Split and scale the data"""
        print("\nPreparing data...")
        X = self.df.drop(columns=["target"])
        y = self.df["target"]

        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )

        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)

        print(f"Training set: {self.X_train.shape}")
        print(f"Test set: {self.X_test.shape}")

    def train_decision_tree_gini(self):
        """Train Decision Tree with Gini criterion"""
        print("\n" + "="*60)
        print("Training Decision Tree (Gini)...")
        print("="*60)

        param_grid = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': [None, 'sqrt', 'log2']
        }

        grid_search = GridSearchCV(
            estimator=DecisionTreeClassifier(criterion='gini', random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            verbose=1,
            n_jobs=-1
        )

        grid_search.fit(self.X_train, self.y_train)
        best_model = grid_search.best_estimator_

        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV accuracy: {round(grid_search.best_score_ * 100, 2)}%")

        self.models['decision_tree_gini'] = best_model
        self._evaluate_model(best_model, "Decision Tree (Gini)")

        return best_model

    def train_decision_tree_entropy(self):
        """Train Decision Tree with Entropy criterion"""
        print("\n" + "="*60)
        print("Training Decision Tree (Entropy)...")
        print("="*60)

        param_grid = {
            'max_depth': [3, 5, 10, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': [None, 'sqrt', 'log2']
        }

        grid_search = GridSearchCV(
            estimator=DecisionTreeClassifier(criterion='entropy', random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            verbose=1,
            n_jobs=-1
        )

        grid_search.fit(self.X_train, self.y_train)
        best_model = grid_search.best_estimator_

        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV accuracy: {round(grid_search.best_score_ * 100, 2)}%")

        self.models['decision_tree_entropy'] = best_model
        self._evaluate_model(best_model, "Decision Tree (Entropy)")

        return best_model

    def train_random_forest(self):
        """Train Random Forest Classifier"""
        print("\n" + "="*60)
        print("Training Random Forest...")
        print("="*60)

        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4],
            'max_features': ['sqrt', 'log2', None],
            'criterion': ['entropy', 'gini']
        }

        grid_search = GridSearchCV(
            estimator=RandomForestClassifier(random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            verbose=1,
            n_jobs=-1
        )

        grid_search.fit(self.X_train, self.y_train)
        best_model = grid_search.best_estimator_

        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV accuracy: {round(grid_search.best_score_ * 100, 2)}%")

        self.models['random_forest'] = best_model
        self._evaluate_model(best_model, "Random Forest")

        return best_model

    def train_logistic_regression(self):
        """Train Logistic Regression"""
        print("\n" + "="*60)
        print("Training Logistic Regression...")
        print("="*60)

        param_grid = {
            'C': [0.001, 0.01, 0.1, 1, 10, 100],
            'penalty': ['l1', 'l2'],
            'solver': ['liblinear']
        }

        grid_search = GridSearchCV(
            estimator=LogisticRegression(max_iter=1000, random_state=42),
            param_grid=param_grid,
            cv=5,
            scoring='accuracy',
            verbose=1,
            n_jobs=-1
        )

        grid_search.fit(self.X_train, self.y_train)
        best_model = grid_search.best_estimator_

        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV accuracy: {round(grid_search.best_score_ * 100, 2)}%")

        self.models['logistic_regression'] = best_model
        self._evaluate_model(best_model, "Logistic Regression")

        return best_model

    def _evaluate_model(self, model, model_name):
        """Evaluate a trained model"""
        y_pred = model.predict(self.X_test)

        print(f"\n{model_name} Performance:")
        print("-" * 40)
        print(f"Accuracy: {accuracy_score(self.y_test, y_pred):.4f}")

        # Classification Report
        print("\nClassification Report:")
        print(classification_report(self.y_test, y_pred,
                                   target_names=["No Disease", "Disease"]))

        # ROC-AUC Score
        if hasattr(model, "predict_proba"):
            y_prob = model.predict_proba(self.X_test)[:, 1]
        elif hasattr(model, "decision_function"):
            y_prob = model.decision_function(self.X_test)
        else:
            return

        auc_score = roc_auc_score(self.y_test, y_prob)
        print(f"ROC-AUC Score: {auc_score:.4f}")

    def save_models(self, output_dir: str = "../models"):
        """Save all trained models"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        print(f"\n{'='*60}")
        print("Saving models...")
        print(f"{'='*60}")

        for name, model in self.models.items():
            model_path = output_path / f"{name}.pkl"
            joblib.dump(model, model_path)
            print(f"Saved {name} to {model_path}")

        # Save scaler
        scaler_path = output_path / "scaler.pkl"
        joblib.dump(self.scaler, scaler_path)
        print(f"Saved scaler to {scaler_path}")

    def train_all(self):
        """Train all models"""
        self.load_data()
        self.prepare_data()

        self.train_decision_tree_gini()
        self.train_decision_tree_entropy()
        self.train_logistic_regression()
        # Random Forest takes longer, uncomment if needed
        # self.train_random_forest()

        self.save_models()

        print("\n" + "="*60)
        print("Training Complete!")
        print("="*60)
        print("\nModel Performance Summary:")
        for name, model in self.models.items():
            y_pred = model.predict(self.X_test)
            acc = accuracy_score(self.y_test, y_pred)
            print(f"{name}: {acc:.4f}")


if __name__ == "__main__":
    # Set paths
    data_path = "../data/heart.csv"

    # Initialize and train
    trainer = HeartDiseaseTrainer(data_path)
    trainer.train_all()
