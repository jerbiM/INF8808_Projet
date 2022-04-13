import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import preprocess as preproc
import sankey
import stackedBarChart
import heatmap
import pymsgbox

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

df_file = "assets/donnees_culturelles_synapseC_2.csv"
df = preproc.to_df(df_file)
# data preparation
repartition_region = preproc.to_df("assets/repartion_region.csv")
clusters = preproc.add_cluster(repartition_region)

new_df = preproc.add_clusters(df, clusters)

df_2016 = preproc.group_by_year_month(df, 2016, 7)

df_file_preprocessed = "assets/df.csv"
df_preprocessed = preproc.to_df(df_file_preprocessed)

fig1 = stackedBarChart.stackedBarChart(df_2016)
fig2 = sankey.sankey_diagram_g_cat(new_df)
fig3 = sankey.sankey_diagram_r_cat(new_df, 'Centre')
#fig4 = sankey.sankey_diagram_g_scat(new_df, 'Musique')
fig4 = heatmap.make_heatmap(df_preprocessed, years=set([2019,2020]))
fig5 = sankey.sankey_diagram_r_cat(new_df, 'Sud')
fig6 = sankey.sankey_diagram_g_scat(new_df, 'ArtsVisuels')


fig4.write_html("index4.html")
def init_app_layout(fig1, fig2, fig3, fig4, fig5, fig6):

    return html.Div(className='content', children=[
        html.Header(children=[
            html.H1('Que faire au Québec ?'),
            html.H2('Une analyse des évènements proposés sur le territoire')
        ]),
        html.Main(children=[
            html.Div([
                html.Div([

                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {'label': '2016', 'value': '2016'},
                                {'label': '2017', 'value': '2017'},
                                {'label': '2018', 'value': '2018'},
                                {'label': '2019', 'value': '2019'},
                                {'label': '2020', 'value': '2020'},
                                {'label': '2021', 'value': '2021'},
                                {'label': '2022', 'value': '2022'},
                                {'label': '2023', 'value': '2023'},
                                {'label': '2024', 'value': '2024'},
                                {'label': '2029', 'value': '2029'},
                                {'label': '2041', 'value': '2041'},
                            ],
                            value='2016',
                            id='dropdownYear'
                        ),
                    ], style={'width': '48%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {'label': 'Montréal', 'value': 'Montréal'},
                                {'label': 'Laval', 'value': 'Laval'},
                                {'label': 'Estrie', 'value': 'Estrie'}
                            ],
                            value='Montréal',
                            id='dropdownRegion'
                        ),
                    ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
                ]),

                dcc.Graph(figure=fig1,
                          config=dict(
                              scrollZoom=False,
                              showTips=False,
                              showAxisDragHandles=False,
                              doubleClick=False,
                              displayModeBar=False
                          ),
                          className='graph',
                          id='viz_1'),
                dcc.Slider(
                    id='MonthsSlider',
                    min=0,
                    max=12,
                    step=1,
                    value='12'
                ),
                html.Label(['Month'], style={'font-weight': 'bold'})
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
                    figure=fig6,
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


app.layout = init_app_layout(fig1, fig2, fig3, fig4, fig5, fig6)


fig1.write_html("indexViz1.html")
#fig2.write_html("indexFig2.html")
##fig3.write_html("indexFig3.html")
#fig4.write_html("indexFig4.html")
#fig5.write_html("indexFig5.html")
#fig6.write_html("indexFig6.html")

@app.callback(
    Output('viz_1', 'figure'),
    [Input(component_id='dropdownYear', component_property='value')],
    [Input(component_id='MonthsSlider', component_property='value')]
)
def figWithNewDf(selected_year, selected_month):
    print(selected_year)
    print(selected_month)
    print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    new_df_selected = preproc.group_by_year_month(df, int(selected_year), selected_month)
    #if new_df_selected.empty:
        #pymsgbox.alert('Pas d''événements pour la période choisie.', 'Avertissement')
    return stackedBarChart.stackedBarChart(preproc.group_by_year_month(df, int(selected_year), selected_month))
        