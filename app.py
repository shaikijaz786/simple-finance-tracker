import streamlit as st
import pandas as pd
# Import our database functions
from database import init_db, add_transaction_to_db, get_all_transactions, clear_db

# Initialize the database table right when the app loads
init_db()

# # 1. Page Configuration & Title
st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
st.title("💰 Simple Personal Finance Tracker")
st.write("Track your income and expenses to visualize your monthly savings.")

# # 2. User Input Form
st.header("Add New Transaction")
with st.form("transaction_form", clear_on_submit=True):
    title = st.text_input("Transaction Name (e.g., Grocery, Salary, Rent)")
    amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    type_trans = st.selectbox("Type", ["Expense", "Income"])
    category = st.selectbox("Category", ["Food", "Housing", "Entertainment", "Salary", "Other"])
    
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted and title:
        # Save directly to SQLite database instead of session_state
        add_transaction_to_db(title, amount, type_trans, category)
        st.success(f"Added: {title}")

# # 3. Display Summary Metrics & History from Database
# Fetch the latest data from SQLite
df = get_all_transactions()

if not df.empty:
    st.header("Financial Summary & History")
    
    # Calculate Metrics using Pandas
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum()
    net_savings = total_income - total_expense
    
    # Show summary cards side-by-side
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expense:,.2f}")
    col3.metric("Net Savings", f"${net_savings:,.2f}")
    
    st.markdown("---")
    
    # Show the interactive data table
    st.subheader("Transaction History Log")
    st.dataframe(df, use_container_width=True)
    
    # Clear history button linked to database
    if st.button("Clear All History"):
        clear_db()
        st.rerun()
else:
    st.info("No transactions recorded yet. Use the form above to add your first transaction!")