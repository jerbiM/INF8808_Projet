import plotly.express as px


def mapQuebec(dfMap, geojsonQc):
    fig = px.choropleth_mapbox(dfMap, geojson=geojsonQc, locations='region',
                               color='nombreEvenements',
                               color_continuous_scale="Viridis",
                               featureidkey="properties.res_nm_reg",
                               range_color=(0, 1715),
                               mapbox_style="carto-positron",
                               zoom=3,
                               center={"lat": 52.541377, "lon": -70.373741},
                               opacity=0.5
                               )

    return fig
