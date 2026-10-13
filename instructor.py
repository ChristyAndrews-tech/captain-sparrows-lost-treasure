import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Instructor Dashboard", layout="wide")

st.title("👨‍🏫 Captain Sparrow – Instructor Dashboard")

FILE = "scores.csv"

if os.path.exists(FILE):
    df = pd.read_csv(FILE)
else:
    df = pd.DataFrame(columns=["Pirate", "Score"])

st.subheader("📊 Player Results")

st.dataframe(df, use_container_width=True)

st.subheader("📈 Summary")

if len(df) > 0:
    st.write("Total Players:", len(df))
    st.write("Average Score:", round(df["Score"].mean(), 2))
    st.write("Highest Score:", df["Score"].max())
    st.write("Lowest Score:", df["Score"].min())
else:
    st.write("No data yet.")
