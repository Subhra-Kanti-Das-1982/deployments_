import pandas as pd
import plotly.express as px
import streamlit as st


def render_radar(scores):

    radar_scores = {
        "Dharma":
            scores["dharma"],

        "Satya":
            scores["satya"],

        "Karuna":
            scores["karuna"],

        "Self Control":
            scores["self_control"],

        "Responsibility":
            scores["responsibility"],

        "Humility":
            10 - scores["ego"]
    }

    df = pd.DataFrame({
        "Trait":
            list(
                radar_scores.keys()
            ),
        "Score":
            list(
                radar_scores.values()
            )
    })

    fig = px.line_polar(
        df,
        r="Score",
        theta="Trait",
        line_close=True
    )

    fig.update_traces(
        fill="toself"
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 10]
            )
        ),
        showlegend=False
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )