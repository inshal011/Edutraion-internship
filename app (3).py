import gradio as gr
import pandas as pd
import numpy as np
import joblib

# Load model and scaler
rf_model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")

# Feature columns used in training
feature_cols = ['CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
                'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
                'Geography_Germany', 'Geography_Spain', 'Gender_Male']

# Prediction function with rule-based explanation
def predict_churn(*inputs):
    # Convert inputs to DataFrame
    data = np.array(inputs).reshape(1, -1)
    df = pd.DataFrame(data, columns=feature_cols)

    # Scale the data
    scaled_data = scaler.transform(df)

    # Make prediction
    pred = rf_model.predict(scaled_data)[0]
    prob = rf_model.predict_proba(scaled_data)[0][1]

    # Generate explanation
    explanation = ""
    if df['Age'].values[0] > 50:
        explanation += "- Older customers tend to churn more.
"
    if df['Balance'].values[0] > 100000:
        explanation += "- High balance might indicate low product usage.
"
    if df['IsActiveMember'].values[0] == 0:
        explanation += "- Inactive members are more likely to churn.
"
    if df['Geography_Germany'].values[0] == 1:
        explanation += "- Customers from Germany have shown higher churn historically.
"
    if df['CreditScore'].values[0] < 600:
        explanation += "- Low credit score is a potential churn indicator.
"
    if explanation == "":
        explanation = "No strong churn indicators detected based on input."

    # Result
    status = "Prediction: Customer is likely to churn." if pred == 1 else "Prediction: Customer is likely to stay."
    result = f"{status}
Churn Probability: {prob:.2f}

Explanation:
{explanation}"
    return result

# Define Gradio inputs
inputs = [
    gr.Number(label="Credit Score"),
    gr.Number(label="Age"),
    gr.Number(label="Tenure"),
    gr.Number(label="Balance"),
    gr.Number(label="Number of Products"),
    gr.Radio([0, 1], label="Has Credit Card (0 = No, 1 = Yes)"),
    gr.Radio([0, 1], label="Is Active Member (0 = No, 1 = Yes)"),
    gr.Number(label="Estimated Salary"),
    gr.Radio([0, 1], label="Germany? (1 = Yes, 0 = No)"),
    gr.Radio([0, 1], label="Spain? (1 = Yes, 0 = No)"),
    gr.Radio([0, 1], label="Male? (1 = Yes, 0 = No)")
]

# Launch app
gr.Interface(
    fn=predict_churn,
    inputs=inputs,
    outputs="text",
    title="Customer Churn Predictor",
    description="Predict customer churn and understand important contributing factors."
).launch()


