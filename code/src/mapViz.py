import plotly.express as px


def mapQuebec(dfMap, geojsonQc):
    fig = px.choropleth_mapbox(dfMap, geojson=geojsonQc, locations='region',
                               color='nombreEvenements',
                               color_continuous_scale="Viridis",
                               featureidkey="properties.RES_NM_REG",
                               range_color=(0, 1715),
                               mapbox_style="carto-positron",
                               zoom=3,
                               center={"lat": 52.541377, "lon": -70.373741},
                               opacity=0.5,
                               title="Distribution des événements au Québec géographiquement")

    return fig
