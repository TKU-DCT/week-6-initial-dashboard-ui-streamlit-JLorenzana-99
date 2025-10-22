import streamlit as st
import pandas as pd
import os

# Page configuration
st.set_page_config(
    page_title="System Monitor Dashboard", 
    layout="wide",
    page_icon="🖥️"
)

# Title and description
st.title("🖥️ System Monitoring Dashboard")

# Check if log.csv exists
if os.path.exists("log.csv"):
    # Load the CSV file
    df = pd.read_csv("log.csv")
    
    # Display metrics summary at the top
    col1, col2, col3, col4 = st.columns(4)
    
    if len(df) > 0:
        latest = df.iloc[-1]
        
        with col1:
            st.metric("Latest CPU Usage", f"{latest['CPU']:.1f}%")
        with col2:
            st.metric("Latest Memory Usage", f"{latest['Memory']:.1f}%")
        with col3:
            st.metric("Latest Disk Usage", f"{latest['Disk']:.1f}%")
        with col4:
            status_emoji = "✅" if latest['Ping_Status'] == "UP" else "❌"
            st.metric("Ping Status", f"{status_emoji} {latest['Ping_Status']}")
    
    st.divider()
    
    # Display most recent 5 records
    st.subheader("📊 Latest 5 Records")
    
    # Style the dataframe with color coding for Ping_Status
    def highlight_ping_status(row):
        if row['Ping_Status'] == 'UP':
            return ['background-color: #026917'] * len(row)
        else:
            return ['background-color: #b50202'] * len(row)
    
    recent_df = df.tail(5).copy()
    styled_df = recent_df.style.apply(highlight_ping_status, axis=1)
    st.dataframe(styled_df, use_container_width=True)
    
    st.divider()
    
    # Plot line charts for CPU, Memory, Disk
    st.subheader("📈 CPU / Memory / Disk Usage Over Time")
    
    if len(df) > 0:
        # Create a chart with Timestamp as index
        chart_data = df.set_index("Timestamp")[["CPU", "Memory", "Disk"]]
        st.line_chart(chart_data, use_container_width=True)
    else:
        st.info("No data available to plot.")
    
    st.divider()
    
    # Bonus: Ping Status Chart
    st.subheader("🌐 Network Connectivity")
    col1, col2 = st.columns(2)
    
    with col1:
        # Show ping status over time
        ping_data = df.copy()
        ping_data['Ping_Up'] = (ping_data['Ping_Status'] == 'UP').astype(int)
        st.line_chart(ping_data.set_index("Timestamp")["Ping_Up"], use_container_width=True)
        st.caption("1 = UP, 0 = DOWN")
    
    with col2:
        # Show ping response times (only when UP)
        ping_times = df[df['Ping_ms'] > 0].copy()
        if len(ping_times) > 0:
            st.line_chart(ping_times.set_index("Timestamp")["Ping_ms"], use_container_width=True)
            st.caption("Response time in milliseconds")
        else:
            st.info("No successful ping responses recorded.")
    
    st.divider()
    
    # Show total records
    st.caption(f"📝 Total records in log: **{len(df)}**")
    
    # Bonus: Download button
    csv = df.to_csv(index=False)
    st.download_button(
        label="⬇️ Download Full Log",
        data=csv,
        file_name="system_log_export.csv",
        mime="text/csv"
    )

else:
    # Warning if file doesn't exist
    st.warning("⚠️ log.csv not found. Please run your system logger first.")
    st.info("Run the following command to generate logs:")
    st.code("python main.py", language="bash")
    
    st.markdown("### Expected CSV Format")
    st.code("""Timestamp,CPU,Memory,Disk,Ping_Status,Ping_ms
2025-10-01 12:00:00,15.2,40.1,58.9,UP,22.5
2025-10-01 12:00:10,18.3,42.0,59.1,UP,20.8""", language="csv")