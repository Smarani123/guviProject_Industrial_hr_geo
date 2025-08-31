import sys, os
# Add parent directory (project root) to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

import pandas as pd
import plotly.express as px
import streamlit as st
from src.data_loader import load_and_merge_csvs

st.set_page_config(page_title="Industrial Human Resource Geo-Visualization", layout="wide")

st.title("Industrial Human Resource Geo-Visualization")
st.caption("Explore main vs marginal workers across industries, states, and genders (2011 NIC).")

@st.cache_data(show_spinner=False)
def load_data():
    data_path = os.path.join(os.path.dirname(__file__), "..", "data")
    df = load_and_merge_csvs(data_path)
    return df

df = load_data()

# Sidebar filters
states = sorted(df["source_state"].dropna().unique().tolist())
industries = sorted(df["industry_group"].dropna().unique().tolist()) if "industry_group" in df.columns else []
gender_cols = [
    "main_workers_total_persons","main_workers_total_males","main_workers_total_females",
    "marginal_workers_total_persons","marginal_workers_total_males","marginal_workers_total_females"
]
metric = st.sidebar.selectbox("Metric", gender_cols, index=0)
state_sel = st.sidebar.multiselect("States", states, default=states[:8])
industry_sel = st.sidebar.multiselect("Industry Groups", industries, default=industries[:8] if industries else [])

filt = df[df["source_state"].isin(state_sel)]
if industries:
    filt = filt[filt["industry_group"].isin(industry_sel)]

# 1) State totals
st.subheader("State totals")
state_tot = filt.groupby("source_state", as_index=False)[metric].sum().sort_values(metric, ascending=False)
fig1 = px.bar(state_tot, x="source_state", y=metric)
st.plotly_chart(fig1, use_container_width=True)

# 2) Industry totals
if industries:
    st.subheader("Industry totals")
    ind_tot = filt.groupby("industry_group", as_index=False)[metric].sum().sort_values(metric, ascending=False)
    fig2 = px.bar(ind_tot, x="industry_group", y=metric)
    st.plotly_chart(fig2, use_container_width=True)

# 3) Rural vs Urban split (Persons)
st.subheader("Rural vs Urban (Total Persons)")
ru_cols = ["main_workers_rural_persons","main_workers_urban_persons"]
ru = filt[["source_state"] + ru_cols].groupby("source_state", as_index=False).sum()
ru_melt = ru.melt(id_vars="source_state", var_name="area", value_name="count")
fig3 = px.bar(ru_melt, x="source_state", y="count", color="area", barmode="group")
st.plotly_chart(fig3, use_container_width=True)

st.info("Tip: Use the left sidebar to change metric, states and industry groups.")
