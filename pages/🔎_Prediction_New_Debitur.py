import streamlit as st

import pandas as pd
import plotly.express as px

import joblib
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(
    page_title="Loan Analytics Dashboard",
    page_icon="💰",
    layout="wide"
)

st.markdown("<h1 style='text-align: center;'>Loan Condition Prediction Dashboard</h1>", unsafe_allow_html=True)

st.markdown("---")

# Sidebar section
# Sidebar for feature information
with st.sidebar:
    st.header("Feature Information")
    st.markdown("""
    Below are the features used in the loan prediction model. 
    Please input the relevant values in the main section to make predictions.
    """)
    
    st.subheader("Features:")
    st.markdown("""
    - **`employment_length`**: The length of employment in years (numeric).
    - **`home_ownership`**: The type of home ownership (categorical: MORTGAGE, OWN, RENT).
    - **`income_category`**: The income category of the borrower (categorical: Low, Medium, High).
    - **`annual_income`**: The annual income of the borrower (numeric).
    - **`loan_amount`**: The amount of the loan requested (numeric).
    - **`term`**: The term of the loan (categorical: 36 months, 60 months).
    - **`purpose`**: The purpose of the loan (categorical).
    - **`interest_payments`**: The type of interest payments (categorical).
    - **`loan_condition`**: The condition of the loan (target variable).
    - **`interest_rate`**: The interest rate for the loan (numeric).
    - **`grade`**: The grade assigned to the loan (categorical).
    - **`dti`**: Debt-to-Income ratio (numeric).
    - **`total_payment`**: Total payment amount over the loan term (numeric).
    - **`installment`**: Monthly installment amount (numeric).
    - **`issue_weekday`**: The day of the week the loan was issued (categorical).
    """)






## _____CONTENT______


# Load the trained model and expected features
model = joblib.load('loan_prediction_model.pkl')
expected_features = joblib.load('model_features.pkl')  # Load expected feature names

# Input container for user inputs
with st.container():
    st.markdown("### Input Loan Details:")
    
    # Employment length
    employment_length = st.slider(
        "Employment Length (years)", 
        min_value=0.0, 
        max_value=50.0, 
        value=1.0, 
        step=0.5, 
        help="Select the length of employment"
    )

    # Home ownership
    home_ownership = st.selectbox(
        "Home Ownership", 
        options=["MORTGAGE", "OWN", "RENT"], 
        help="Select the type of home ownership"
    )

    # Income category
    income_category = st.selectbox(
        "Income Category", 
        options=["Low", "Medium", "High"], 
        help="Select the income category"
    )

    # Annual income
    annual_income = st.number_input(
        "Annual Income", 
        min_value=10000, 
        max_value=500000, 
        value=50000, 
        step=5000, 
        help="Enter the annual income"
    )

    # Loan amount
    loan_amount = st.number_input(
        "Loan Amount", 
        min_value=1000, 
        max_value=100000, 
        value=15000, 
        step=1000, 
        help="Enter the loan amount"
    )

    # Term
    term = st.selectbox(
        "Loan Term", 
        options=["36 months", "60 months"], 
        help="Select the loan term"
    )

    # Purpose
    purpose = st.selectbox(
        "Loan Purpose", 
        options=["debt_consolidation", "credit_card", "home_improvement", "major_purchase", "other"], 
        help="Select the purpose of the loan"
    )

    # Interest payments
    interest_payments = st.selectbox(
        "Interest Payments", 
        options=["High", "Low"], 
        help="Select the type of interest payments"
    )

    # Grade
    grade = st.selectbox(
        "Loan Grade", 
        options=["A", "B", "C", "D", "E", "F", "G"], 
        help="Select the loan grade"
    )

    # Debt-to-Income ratio (dti)
    dti = st.slider(
        "Debt-to-Income Ratio (DTI)", 
        min_value=0.0, 
        max_value=50.0, 
        value=15.0, 
        step=0.1, 
        help="Select the DTI ratio"
    )

# Convert inputs into a DataFrame format with the expected features
input_data = pd.DataFrame({
    "employment_length": [employment_length],
    "home_ownership_MORTGAGE": [1 if home_ownership == "MORTGAGE" else 0],
    "home_ownership_OWN": [1 if home_ownership == "OWN" else 0],
    "home_ownership_RENT": [1 if home_ownership == "RENT" else 0],
    "income_category_Low": [1 if income_category == "Low" else 0],
    "income_category_Medium": [1 if income_category == "Medium" else 0],
    "income_category_High": [1 if income_category == "High" else 0],
    "annual_income": [annual_income],
    "loan_amount": [loan_amount],
    "term_36 months": [1 if term == "36 months" else 0],
    "term_60 months": [1 if term == "60 months" else 0],
    "purpose_debt_consolidation": [1 if purpose == "debt_consolidation" else 0],
    "purpose_credit_card": [1 if purpose == "credit_card" else 0],
    "purpose_home_improvement": [1 if purpose == "home_improvement" else 0],
    "purpose_major_purchase": [1 if purpose == "major_purchase" else 0],
    "purpose_other": [1 if purpose == "other" else 0],
    "interest_payments_High": [1 if interest_payments == "High" else 0],
    "interest_payments_Low": [1 if interest_payments == "Low" else 0],
    "grade": [ord(grade) - ord("A")],  # Convert grade to numeric
    "dti": [dti]
})

# Reindex to match expected features, filling missing columns with 0
input_data = input_data.reindex(columns=expected_features, fill_value=0)

# Predict and Display Results
if st.button("Predict Loan Condition"):
    # Probability and Prediction
    prob = model.predict_proba(input_data)[0][1] * 100  # Probability of "Good Loan"
    prediction = "Good Loan" if prob > 50 else "Bad Loan"
    
    # Gauge plot for prediction probability
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=prob,
        title={'text': f"Prediction: {prediction}"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': '#FFA07A' if prediction == "Good Loan" else "salmon"},
            'steps': [
                    {'range': [0, 50], 'color': '#F8F8F8'},
                    {'range': [50, 100], 'color': '#FFE4E1'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 50
                }
        }
    ))
    
    st.plotly_chart(fig_gauge)





# Footer
footer_content = """
---

© 2024 Dwi Gustin Nurdialit
"""
st.markdown(f"<h1 style='text-align: center;'>{footer_content}</h1>", unsafe_allow_html=True)

