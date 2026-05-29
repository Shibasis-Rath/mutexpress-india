import streamlit as st
import pandas as pd
import plotly.express as px

# Set up the page
st.set_page_config(page_title="MutExpress-India", page_icon="🧬", layout="wide")
st.title("🧬 MutExpress-India Dashboard")
st.markdown("**Indian-Population-Aware Variant & Expression Prioritization**")

# Try to load the data we generated in Phase 3
try:
    df = pd.read_csv("../results/mutexpress_india_output.csv")
    st.success("Phase 3 Integration Data Loaded Successfully!")
    
    # Calculate metrics
    high_count = len(df[df["MutExpress_Priority"] == "HIGH"])
    med_v_count = len(df[df["MutExpress_Priority"] == "MEDIUM_V"])
    med_e_count = len(df[df["MutExpress_Priority"] == "MEDIUM_E"])
    
    # Display top-level metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("HIGH Priority Genes", high_count)
    col2.metric("MEDIUM_V (Variant Only)", med_v_count)
    col3.metric("MEDIUM_E (Expression Only)", med_e_count)
    
    st.markdown("---")
    
    # Display the Pie Chart
    st.subheader("Priority Distribution")
    counts = df["MutExpress_Priority"].value_counts().reset_index()
    counts.columns = ["Priority", "Count"]
    fig_pie = px.pie(counts, names="Priority", values="Count", color="Priority",
                     color_discrete_map={"HIGH": "#E63946", "MEDIUM_V": "#F4A261", "MEDIUM_E": "#457B9D", "LOW": "#A8DADC"})
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Display the Data Table
    st.subheader("Top Ranked Priority Genes")
    st.dataframe(df.head(100))
    
    # Add a download button for the results
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download Full Results CSV",
        data=csv,
        file_name='mutexpress_india_final.csv',
        mime='text/csv',
    )

except FileNotFoundError:
    st.error("Results file not found. Please ensure Phase 3 is completed and mutexpress_india_output.csv exists in the results folder.")
