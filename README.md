
# Credit Scoring Model using Machine Learning

## Objective
Build a machine learning model to predict an individual's creditworthiness based on financial and demographic data.

##  Tools & Technologies
- Python, Pandas, NumPy
- Scikit-learn, Matplotlib, Seaborn
- Logistic Regression, Decision Tree, Random Forest

##  Dataset
Synthetic version of the German Credit Dataset with 1000 samples and labeled "Risk" as good/bad credit.

## Key Features
- Credit amount
- Age
- Duration
- Housing, Job, Saving and Checking accounts, Purpose

##  Model Performance
Random Forest achieved:
- Precision (class 1): 0.69
- Recall (class 1): 0.96
- ROC-AUC: ~0.51

> Most important features: Credit amount, Age, Duration

##  How to Run
1. Open `credit_scoring_model.ipynb` in Jupyter or Google Colab.
2. Upload `german_credit_data_full.csv` when prompted.
3. Run all cells to see model training and evaluation.

##  Files
- `credit_scoring_model.ipynb`: Full project notebook.
- `german_credit_data_full.csv`: Dataset.
- `README.md`: Project summary and instructions.

## Author
Yara Mahmoud — ML Intern @ CodeAlpha
