import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import preprocess as preproc
import sankey

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

df_file = "assets/donnees_culturelles_synapseC.csv"
df = preproc.to_df(df_file)
#data preparation
repartition_region = preproc.to_df("assets/repartion_region.csv")
clusters=preproc.add_cluster(repartition_region)

new_df=preproc.add_clusters(df,clusters)


fig1 = sankey.sankey_diagram_g_cat(new_df)
fig2 = sankey.sankey_diagram_r_cat(new_df, 'Centre')
fig3 = sankey.sankey_diagram_g_scat(new_df, 'Musique')
fig4 = sankey.sankey_diagram_r_cat(new_df, 'Sud')
fig5 = sankey.sankey_diagram_g_scat(new_df, 'ArtsVisuels')


def init_app_layout(fig1, fig2, fig3, fig4, fig5):

    return html.Div(className='content', children=[
        html.Header(children=[
                html.H1('Que faire au Québec ?'),
                html.H2('Une analyse des évènements proposés sur le territoire')
            ]),
            html.Main(children=[
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig1,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='viz_1'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig2,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='sankey-link',
                        id='viz_2'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig3,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            doubleClick=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='viz_3'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig4,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='viz_4'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig5,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='viz_5'
                    )
                ]),
                html.Div(className='viz-container', children=[
                    dcc.Graph(
                        figure=fig2,
                        config=dict(
                            scrollZoom=False,
                            showTips=False,
                            showAxisDragHandles=False,
                            displayModeBar=False
                        ),
                        className='graph',
                        id='viz_6'
                    )
                ])
            ])
        ])
        


app.layout = init_app_layout(fig1, fig2, fig3, fig4, fig5)