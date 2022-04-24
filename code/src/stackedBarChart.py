import pandas as pd
import plotly.express as px


def stackedBarChart(df):
    sizeY = 1
    df['date'] = pd.to_datetime(df["date"])
    # print(df['date'])
    df.insert(0, 'Événements', sizeY)

    fig = px.bar(df, x="date", y="Événements", color='categorie',
                 hover_name="Nom", hover_data=["here_address", "date", "prix"],
                 labels={
                     "date": "Date",
                     "Événements": "Nombre d'événements",
                     "categorie": "Catégorie"
                 },
                 title="Chronologie temporelle des événements et attentes financières").update_layout(
        xaxis={"rangeslider": {"visible": True},
               "autorange": True
               },
        yaxis={
            "autorange": True
        }
    )

    return fig
