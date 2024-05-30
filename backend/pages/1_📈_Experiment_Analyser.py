import pandas as pd
import streamlit as st
import plotly.express as px
from utils.db_connector import DBConnector
from utils.results import Results

st.set_page_config(
    page_title="Experiment Analyser - PromptSLR",
    page_icon="📈",
    layout="wide",
)

db_connector = DBConnector()


def get_results_df(project_ids):
    results = []
    for project_id in project_ids:
        result = Results(project_id)
        results.append(
            {
                "ProjectID": project_id,
                "Completed Articles": result.tp + result.fp + result.tn + result.fn,
                "Articles with Error": result.fp + result.fn,
                "True Positive": result.tp,
                "False Positive": result.fp,
                "True Negative": result.tn,
                "False Negative": result.fn,
                "Accuracy": result.get_accuracy(),
                "Precision": result.get_precision(),
                "Recall": result.get_recall(),
                "F1 Score": result.get_f1_score(),
                "Specificity": result.get_specificity(),
                "MCC": result.get_mcc(),
                "Balanced Accuracy": result.get_balanced_accuracy(),
                "Miss Rate": result.get_miss_rate(),
                "Fβ Score": result.get_fb_score(),
                "WSS": result.get_wss(),
                "WSS@95": result.get_wss(recall=0.95),
                "NPV": result.get_npv(),
                "G-Mean": result.get_g_mean(),
            }
        )
    return pd.DataFrame(results)


st.title("Experiment Analyser")
st.header("Choose the experiment you want to analyse")
experiment = st.multiselect(
    "Experiment",
    [f"{value} - {key}" for key, value in db_connector.get_projects().items()],
)
project_lables, project_ids = zip(*[project.split(" - ") for project in experiment])

st.subheader("Choose the metrics you want to analyse")
metrics = st.multiselect(
    "Metrics",
    [
        "Completed Articles",
        "Articles with Error",
        "True Positive",
        "False Positive",
        "True Negative",
        "False Negative",
        "Accuracy",
        "Precision",
        "Recall",
        "F1 Score",
        "Specificity",
        "MCC",
        "Balanced Accuracy",
        "Miss Rate",
        "Fβ Score",
        "WSS",
        "WSS@95",
        "NPV",
        "G-Mean",
    ],
)

st.subheader("Choose the plot you want to see")
plot = st.selectbox("Plot", ["Bar", "Line", "Pie", "Scatter", "Radial"], index=0)

if plot == "Bar":
    st.subheader("Choose the x and y axis")
    x_axis = st.selectbox("X-Axis", metrics, index=0)
    y_axis = st.selectbox("Y-Axis", metrics, index=1)
    df = get_results_df(project_ids)
    fig = px.bar(df, x=x_axis, y=y_axis, hover_name=project_lables)
    st.plotly_chart(fig)

elif plot == "Line":
    st.subheader("Choose the x and y axis")
    x_axis = st.selectbox("X-Axis", metrics, index=0)
    y_axis = st.selectbox("Y-Axis", metrics, index=1)
    df = get_results_df(project_ids)
    fig = px.line(df, x=x_axis, y=y_axis, hover_name=project_lables)
    st.plotly_chart(fig)

elif plot == "Pie":
    st.subheader("Choose the values")
    values = st.selectbox("Values", metrics, index=0)
    df = get_results_df(project_ids)
    fig = px.pie(df, values=values, hover_name=project_lables)
    st.plotly_chart(fig)

elif plot == "Scatter":
    st.subheader("Choose the x and y axis")
    x_axis = st.selectbox("X-Axis", metrics, index=0)
    y_axis = st.selectbox("Y-Axis", metrics, index=1)
    df = get_results_df(project_ids)
    fig = px.scatter(df, x=x_axis, y=y_axis, hover_name=project_lables)
    st.plotly_chart(fig)

elif plot == "Radial":
    st.subheader("Choose the values")
    values = st.selectbox("Values", metrics, index=0)
    df = get_results_df(project_ids)
    fig = px.line_polar(df, r=values, theta=project_lables, line_close=True)
    st.plotly_chart(fig)
