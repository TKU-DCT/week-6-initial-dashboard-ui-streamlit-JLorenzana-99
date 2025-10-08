import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="System Monitor Dashboard", layout="wide")

st.title("🖥️ System Monitoring Dashboard")
st.markdown("This is a simple dashboard that reads from **log.csv** and displays system metrics.")

# TODO: Load CSV if exists
if os.path.exists("log.csv"):
    df = pd.read_csv("log.csv")

    # TODO: Display most recent 5 records
    st.subheader("📊 Latest Records")
    st.dataframe(df.tail(5), use_container_width=True)

    # TODO: Plot line charts
    st.subheader("📈 CPU / Memory / Disk Usage Over Time")
    st.line_chart(df.set_index("Timestamp")[["CPU", "Memory", "Disk"]])
else:
    st.warning("log.csv not found. Please run your system logger first.")
