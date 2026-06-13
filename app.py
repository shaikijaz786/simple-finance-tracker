import streamlit as st
import pandas as pd

# 1. Page Configuration & Title
st.set_page_config(page_title="Personal Finance Tracker", layout="centered")
st.title("💰 Simple Personal Finance Tracker")
st.write("Track your income and expenses to visualize your monthly savings.")

# 2. Initialize Session State (This acts as our temporary database)
if "transactions" not in st.session_state:
    st.session_state.transactions = []

# 3. User Input Form
st.header("Add New Transaction")
with st.form("transaction_form", clear_on_submit=True):
    title = st.text_input("Transaction Name (e.g., Grocery, Salary, Rent)")
    amount = st.number_input("Amount ($)", min_value=0.0, format="%.2f")
    type_trans = st.selectbox("Type", ["Expense", "Income"])
    category = st.selectbox("Category", ["Food", "Housing", "Entertainment", "Salary", "Utilities", "Other"])
    
    submitted = st.form_submit_button("Add Transaction")
    
    if submitted and title:
        # Save data to our list
        st.session_state.transactions.append({
            "Name": title,
            "Amount": amount if type_trans == "Income" else -amount,
            "Type": type_trans,
            "Category": category
        })
        st.success(f"Added {title} successfully!")

# 4. Display Data & Insights
if st.session_state.transactions:
    # Convert our list of dictionaries into a clean Pandas Dataframe
    df = pd.DataFrame(st.session_state.transactions)
    
    # Calculate Metrics
    total_income = df[df["Type"] == "Income"]["Amount"].sum()
    # Expenses are stored as negative numbers, so we multiply by -1 to show a positive total
    total_expense = df[df["Type"] == "Expense"]["Amount"].sum() * -1 
    net_savings = total_income - total_expense

    st.markdown("---")
    st.header("📊 Financial Summary")
    
    # Display beautiful dashboard metric boxes
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"${total_income:,.2f}")
    col2.metric("Total Expenses", f"${total_expense:,.2f}")
    col3.metric("Net Savings", f"${net_savings:,.2f}", delta=f"${net_savings:,.2f}")

    # Display the breakdown table
    st.subheader("Transaction History")
    st.dataframe(df, use_container_width=True)

    # 5. Data Visualization (Pie Chart)
    st.subheader("Expense Breakdown by Category")
    expense_df = df[df["Type"] == "Expense"]
    if not expense_df.empty:
        # Group expenses by category and sum them up
        category_data = expense_df.groupby("Category")["Amount"].sum().abs()
        st.bar_chart(category_data)
    else:
        st.info("Add some expenses to see the chart breakdown.")
else:
    st.info("No transactions added yet. Use the form above to get started!")