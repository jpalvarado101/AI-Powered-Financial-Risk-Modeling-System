import streamlit as st
import pandas as pd

st.title("📊 Financial Risk Monitoring Dashboard")

# Load data
df = pd.read_csv("data/processed_data.csv")

# Display charts
st.subheader("Moving Averages")
st.line_chart(df[["SMA_50", "SMA_200"]])

st.subheader("RSI Indicator")
st.line_chart(df["RSI"])

st.subheader("MACD Indicator")
st.line_chart(df["MACD"])

st.subheader("Risk Level Distribution")
st.bar_chart(df["Risk_Label"].value_counts())

st.write("This dashboard provides a real-time overview of financial risk levels based on ML models.")