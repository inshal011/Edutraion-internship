import gradio as gr
import pandas as pd
import numpy as np
import joblib

# Load trained model and scaler
model = joblib.load("rf_model.pkl")
scaler = joblib.load("scaler.pkl")

# Prediction function
def predict_churn(credit_score, age, tenure, balance, num_products, has_cr_card, is_active_member, salary, geography, gender):
    gender_male = 1 if gender == "Male" else 0
    geography_germany = 1 if geography == "Germany" else 0
    geography_spain = 1 if geography == "Spain" else 0

    data = pd.DataFrame([[
        credit_score, age, tenure, balance, num_products,
        has_cr_card, is_active_member, salary,
        geography_germany, geography_spain, gender_male
    ]], columns=[
        'CreditScore', 'Age', 'Tenure', 'Balance', 'NumOfProducts',
        'HasCrCard', 'IsActiveMember', 'EstimatedSalary',
        'Geography_Germany', 'Geography_Spain', 'Gender_Male'
    ])

    data_scaled = scaler.transform(data)
    prediction = model.predict(data_scaled)[0]
    prob = model.predict_proba(data_scaled)[0][1]

    explanation = ""
    if age > 50:
        explanation += "- Older customers tend to churn more.\n"
    if is_active_member == 0:
        explanation += "- Inactive members are more likely to churn.\n"
    if balance > 100000:
        explanation += "- High balance might indicate low engagement.\n"
    if geography == "Germany":
        explanation += "- German customers had slightly higher churn historically.\n"
    if credit_score < 600:
        explanation += "- Low credit score is a churn risk indicator.\n"

    status = "Customer is likely to churn." if prediction == 1 else "Customer is likely to stay."
    result = f"**{status}**\n\nChurn Probability: {prob:.2f}\n\n**Explanation:**\n{explanation if explanation else 'No strong churn indicators.'}"
    return result

# Gradio Blocks App
with gr.Blocks() as app:
    gr.Markdown("""
    #  Advanced Customer Churn Predictor

    This app predicts whether a customer is likely to churn based on their profile.  
    The model was trained on real customer behavior and demographic data.

    ### 🛠 How to Use
    - Fill in the customer details below.
    - **1 = Yes, 0 = No** for "Has Credit Card" and "Is Active Member".
    - Choose the customer's country and gender using the dropdowns.
    - Click **Submit** to see the prediction and an explanation.

    ---
    """)

    with gr.Row():
        with gr.Column():
            credit_score = gr.Slider(300, 850, value=650, label="Credit Score")
            age = gr.Slider(18, 100, value=40, label="Age")
            tenure = gr.Slider(0, 10, value=5, label="Tenure (Years)")
            balance = gr.Slider(0, 250000, step=1000, label="Balance ($)")
            num_products = gr.Slider(1, 4, label="Number of Products")
            has_cr_card = gr.Radio([1, 0], label="Has Credit Card? (1 = Yes, 0 = No)")
            is_active_member = gr.Radio([1, 0], label="Is Active Member? (1 = Yes, 0 = No)")
            salary = gr.Slider(10000, 200000, step=1000, label="Estimated Salary ($)")
            geography = gr.Dropdown(["France", "Germany", "Spain"], label="Geography")
            gender = gr.Dropdown(["Male", "Female"], label="Gender")

            submit_btn = gr.Button("Predict")

        with gr.Column():
            output = gr.Markdown()

    submit_btn.click(
        fn=predict_churn,
        inputs=[credit_score, age, tenure, balance, num_products, has_cr_card, is_active_member, salary, geography, gender],
        outputs=output
    )

app.launch()


