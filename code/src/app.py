import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import preprocess as preproc
import sankey

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

df_file = "../assets/donnees_culturelles_synapseC.csv"
df = preproc.to_df(df_file)
#data preparation
repartition_region = preproc.to_df("../assets/repartion_region.csv")
clusters=preproc.add_cluster(repartition_region)

new_df=preproc.add_clusters(df,clusters)


#sankey Diagram
categorie_data = preproc.group_by_category(new_df)

clus_cat_data=preproc.group_by_column2_count(df, 'groupe','categorie')

fig=sankey.sankey_daigram(clus_cat_data,categorie_data,clusters)



app.layout = html.Div(
    className='row',
    children=[
        dcc.Graph(figure=fig, id='sankey_diagram',
                  ),])







