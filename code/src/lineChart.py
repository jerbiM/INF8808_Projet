import pandas as pd
import plotly.express as px


def lineChart(df):
    fig = px.line(df, x="year", y="count", color='region',
                  labels={
                      "year": "Année",
                      "count": "Nombre d'événements",
                      "region": "Régions"
                  },
                  title="Régions les plus chères selon les catégories").update_layout(
        xaxis={"rangeslider": {"visible": True},
               "range": [2012, 2030],
               },
        yaxis={
            "autorange": True
        }
    )
    fig.update_traces(connectgaps=True)

    return fig
