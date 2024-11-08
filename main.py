import streamlit as st
import pandas as pd
import numpy as np

st.subheader("Retirement Planner")

col1, col2, col3 = st.columns(3)

with col1:
    cur_age = st.slider(label="Current Age", step=1, value=25)
    ret_age = st.slider(label="Retirement Age", step=1, value=55)
    expenses_planned_until = st.slider(label="Expenses Planned Until", step=1, value=85, min_value=cur_age)

with col2:
    average_return = st.slider(label="Average Return (%)", step=1, value=8)
    step_up_saving = st.slider(label="Step up Saving (%)", step=1, value=5)
    inflation_rate = st.slider(label="Inflation Rate (%)", step=1, value=6)

with col3:
    current_saving = st.text_input(label="Current Saving", value=100000)
    monthly_investment = st.text_input(label="Monthly Saving", value=20000)
    post_retirement_monthly_expense = st.text_input(label="Post Retirement Monthly Expense", value=30000)

st.divider()
st.subheader("Forecast")

def forecast(cur_age,
             ret_age,
             expenses_planned_until,
             average_return,
             step_up_saving,
             inflation_rate,
             current_saving,
             monthly_investment,
             post_retirement_monthly_expense
             ):
    
    age = []
    start_savings = []
    additional_saving = []
    expenses = []
    ending_saving = []
    status = []

    for i in range(cur_age, expenses_planned_until + 1):
        age.append(i)
        # Check for first run
        if i == cur_age:
            start_savings.append(round(float(current_saving), 2))
            additional_saving.append(round(float(monthly_investment) * 12 if i < ret_age else 0, 2))
            expenses.append(float(post_retirement_monthly_expense) * 12 if i >= ret_age else 0)
            ending_saving.append(round(float(start_savings[0]) * (100 + average_return) / 100 - expenses[i - cur_age]/(100 - 20) * 100 + additional_saving[0], 2))
            status.append("Earning" if cur_age < ret_age else "Retired")
        else:
            start_savings.append(ending_saving[i - cur_age - 1])
            additional_saving.append(round(float(additional_saving[i - cur_age - 1] * (100 + step_up_saving)/100), 2) if i < ret_age else 0)
            
            if i == ret_age:
                expenses.append(float(post_retirement_monthly_expense) * ((100 + inflation_rate)/100) ** (ret_age - cur_age) * 12)
            else:
                expenses.append(float(expenses[i - cur_age - 1]) * (100 + inflation_rate) / 100)

            if i >= ret_age:
                ending_saving.append(round(float(start_savings[i - cur_age]) * (100 + average_return) / 100 - expenses[i - cur_age] + additional_saving[i - cur_age], 2))
            else:
                ending_saving.append(round(float(start_savings[i - cur_age]) * (100 + average_return) / 100 - expenses[i - cur_age]/(100 - 20) * 100 + additional_saving[i - cur_age], 2))

            status.append("Earning" if i < ret_age else "Retired")
    
    return pd.DataFrame({
        "Age": age,
        "Starting Saving": start_savings,
        "Additional Savings": additional_saving,
        "Expenses": expenses,
        "Ending Savings": ending_saving,
        "Status": status
    })

df = forecast(
        cur_age=cur_age,
        ret_age=ret_age,
        expenses_planned_until=expenses_planned_until,
        average_return=average_return,
        step_up_saving=step_up_saving,
        inflation_rate=inflation_rate,
        current_saving=current_saving,
        monthly_investment=monthly_investment,
        post_retirement_monthly_expense=post_retirement_monthly_expense,
    )

st.line_chart(df[['Age', 'Ending Savings', 'Expenses']], x="Age", color=["#4dbf90", '#f05435'])

st.subheader("Details")
df.set_index("Age", inplace=True)
st.table(df.style.format(precision=2))