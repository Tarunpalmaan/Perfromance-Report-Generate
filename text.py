import streamlit as st
import pandas as pd
from datetime import datetime

import base64

def get_image_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Set up the Streamlit layout
st.set_page_config(page_title="DP Performance Report", layout="centered")

logo_base64 = get_image_base64(r"E:\Perfromance and dp report project\TarunIX Logo.png")  # replace with your file name

st.markdown(
    f"""
    <style>
    .header-container {{
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 20px;
    }}

    .logo {{
        height: 60px;
        border-radius: 10px;
    }}

    .header-title {{
        animation: fadeGlow 2s ease-in-out;
        background: linear-gradient(to right, black, gold);
        color: white;
        padding: 15px 20px;
        font-size: 32px;
        font-weight: bold;
        border-radius: 10px;
        flex-grow: 1;
    }}

    @keyframes fadeGlow {{
        0% {{ opacity: 0; text-shadow: none; }}
        50% {{ opacity: 1; text-shadow: 0 0 10px gold; }}
        100% {{ opacity: 1; text-shadow: 0 0 20px gold; }}
    }}
    </style>

    <div class="header-container">
        <img class="logo" src="data:image/png;base64,{logo_base64}" alt="Logo">
        <div class="header-title">📝 DP Performance Report Generator</div>
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
st.markdown("<h5 style='text-align: right; color: blue;'>Tarunix Group</h5>", unsafe_allow_html=True)
