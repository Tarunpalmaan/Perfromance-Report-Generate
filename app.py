import streamlit as st
import pandas as pd
from datetime import datetime

# Set up the Streamlit layout
st.set_page_config(page_title="DP Performance Report", layout="centered")
st.markdown(
    """
    <div style="
        background: linear-gradient(to right, black, gold);
        color: white;
        padding: 20px;
        font-size: 36px;
        font-weight: bold;
        text-align: left;
        border-radius: 10px;
        margin-bottom: 20px;
    ">
        📝 Create Your Performance Report
    </div>
    """,
    unsafe_allow_html=True
)


def generate_report(df, name, doj):
    if 'Cancelled' in df.columns:
        df = df[df['Cancelled'] != 'Cancelled']
    df = df[df['Route'] != 'Grand Total']

    df['Revenue'] = df['Revenue'].replace({'₹': '', ',': ''}, regex=True).astype(float)
    df['ASP'] = df['ASP'].replace({'₹': '', ',': ''}, regex=True).astype(float)
    df['Occupancy'] = df['Occupancy'].replace({'%': ''}, regex=True).astype(float)

    total_revenue = df['Revenue'].sum()
    avg_occupancy = df['Occupancy'].mean()
    avg_asp = df['ASP'].mean()

    highest_performing = df.loc[df['Revenue'].idxmax()]
    high_occupancy_schedules = df[df['Occupancy'] >= 90]
    total_high_occupancy = len(high_occupancy_schedules)
    total_full_occupancy = len(high_occupancy_schedules[high_occupancy_schedules['Occupancy'] >= 100])

    doj_day = doj.strftime('%A')

    insights = [
        f"Hi Team,",
        f"Please find DP Performance report of {name} for DOJ: - {doj.strftime('%d-%m-%Y')} ({doj_day}): -",
        "Insights:",
        f"1) Overall revenue generated ₹{total_revenue:,.0f} with an average occupancy of {avg_occupancy:.0f}% and average ASP of ₹{avg_asp:,.0f}.",
        f"2) Highest performing service is {highest_performing['Route']} with overall revenue of ₹{highest_performing['Revenue']:,.0f}, occupancy of {highest_performing['Occupancy']}% and ASP of ₹{highest_performing['ASP']:,.0f}.",
        f"3) Total {total_high_occupancy} schedules have achieved more than 90% Occupancy, in which {total_full_occupancy} schedules have achieved 100% Occupancy."
    ]

    return insights

# UI Inputs
with st.form("report_form"):
    name = st.text_input("Enter Title of Your Report")
    doj = st.date_input("Select Date of Journey")
    uploaded_file = st.file_uploader("Upload Excel or CSV File", type=["xlsx", "xls", "csv"])
    submitted = st.form_submit_button("Generate Report")

    if submitted:
        if not name or not uploaded_file:
            st.warning("Please fill all fields and upload a valid file.")
        else:
            try:
                if uploaded_file.name.endswith('.csv'):
                    df = pd.read_csv(uploaded_file, skiprows=1)
                else:
                    df = pd.read_excel(uploaded_file, skiprows=1)

                insights = generate_report(df, name, doj)
                
                # Display results in a box
                with st.expander("📊 Report Insights"):
                    for line in insights:
                        st.markdown(f"- {line}")
            except Exception as e:
                st.error(f"Something went wrong while processing the file: {e}")
