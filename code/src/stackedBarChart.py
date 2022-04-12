import pandas as pd
import plotly.express as px


def stackedBarChart(df):
    sizeY = 1
    df['date_debut'] = pd.to_datetime(df["date_debut"])
    print(df['date_debut'])
    df.insert(0, 'Yaxis', sizeY)

    fig = px.bar(df, x="date_debut", y="Yaxis", color='categorie').update_layout(
        xaxis={"rangeslider": {"visible": True}, "type": "date",
               "range": [df.tail(50)["date_debut"].min(), df.tail(50)["date_debut"].max()]},
        yaxis={
            "autorange": True
        }
    )

    return fig
