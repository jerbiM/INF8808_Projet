import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go

import preprocess as preproc
import sankey
import stackedBarChart
import heatmap
# import pymsgbox
import barchart

app = dash.Dash(__name__)
app.title = 'Projet | INF8808'

df_file = "assets/df_ghaliUpdated.csv"
df = preproc.to_df(df_file)
# data preparation
repartition_region = preproc.to_df("assets/repartion_region.csv")
clusters = preproc.add_cluster(repartition_region)

new_df = preproc.add_clusters(df, clusters)

df_2016 = preproc.group_by_year_month(df, 2016, 12)

df_file_preprocessed = "assets/df.csv"
df_preprocessed = preproc.to_df(df_file_preprocessed)

clus_est_gratuit_data = preproc.group_by_column2_count(
    df, 'groupe', 'est_gratuit')
df_barchart = preproc.data_prepartion_barchart_gratuit(
    new_df, clus_est_gratuit_data)


fig1 = stackedBarChart.stackedBarChart(df_2016)
fig2 = sankey.sankey_diagram_g_cat(new_df)
fig3 = sankey.sankey_diagram_r_cat(new_df, 'Centre')
# fig4 = sankey.sankey_diagram_g_scat(new_df, 'Musique')
fig4 = heatmap.make_heatmap(df_preprocessed, years=set([2019, 2020]))
fig5 = sankey.sankey_diagram_r_cat(new_df, 'Sud')
fig6 = sankey.sankey_diagram_g_scat(new_df, 'ArtsVisuels')
fig7 = barchart.barchart_gratuit(df_barchart)


# fig4.write_html("index4.html")
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
                                {'label': '2012', 'value': '2012'},
                                {'label': '2015', 'value': '2015'},
                                {'label': '2016', 'value': '2016'},
                                {'label': '2017', 'value': '2017'},
                                {'label': '2018', 'value': '2018'},
                                {'label': '2019', 'value': '2019'},
                                {'label': '2020', 'value': '2020'},
                                {'label': '2021', 'value': '2021'},
                                {'label': '2022', 'value': '2022'},
                                {'label': '2023', 'value': '2023'},
                                {'label': '2024', 'value': '2024'},
                                {'label': '2030', 'value': '2030'}
                            ],
                            value='2016',
                            id='dropdownYear'
                        ),
                    ], style={'width': '48%', 'display': 'inline-block'}),

                    html.Div([
                        dcc.Dropdown(
                            options=[
                                {'label': 'Abitibi-Témiscamingue',
                                    'value': 'Abitibi-Témiscamingue'},
                                {'label': 'Bas-Saint-Laurent',
                                    'value': 'Bas-Saint-Laurent'},
                                {'label': 'Capitale-Nationale',
                                    'value': 'Capitale-Nationale'},
                                {'label': 'Centre-du-Québec',
                                    'value': 'Centre-du-Québec'},
                                {'label': 'Chaudière-Appalaches',
                                    'value': 'Chaudière-Appalaches'},
                                {'label': 'Côte-Nord', 'value': 'Côte-Nord'},
                                {'label': 'Gaspésie–Îles-de-la-Madeleine',
                                    'value': 'Gaspésie–Îles-de-la-Madeleine'},
                                {'label': 'Lanaudière', 'value': 'Lanaudière'},
                                {'label': 'Laurentides', 'value': 'Laurentides'},
                                {'label': 'Laval', 'value': 'Laval (13)'},
                                {'label': 'Mauricie', 'value': 'Mauricie'},
                                {'label': 'Montérégie', 'value': 'Montérégie'},
                                {'label': 'Montréal', 'value': 'Montréal (06)'},
                                {'label': 'Nord-du-Québec',
                                    'value': 'Nord-du-Québec'},
                                {'label': 'Outaouais', 'value': 'Outaouais'},
                                {'label': 'Saguenay-Lac-Saint-Jean',
                                    'value': 'Saguenay-Lac-Saint-Jean'},
                                {'label': 'Toutes les régions',
                                    'value': 'Toutes les régions'}
                            ],
                            value='Toutes les régions',
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
                html.Label(['Choisir le mois'], style={
                    'font-weight': 'bold'}),
                dcc.Slider(
                    id='MonthsSlider',
                    min=0,
                    max=12,
                    step=1,
                    value='12'
                ),
                html.Label(['Choisir le prix en CAD'],
                           style={'font-weight': 'bold'}),
                html.Div([
                    dcc.Input(type='text', id='minPrice'),
                    dcc.RangeSlider(
                        id='PriceSlider',
                        min=0,
                        max=1000,
                        value=[0, 1000],
                        step=250,
                        allowCross=False
                    ),
                    dcc.Input(type='text', id='maxPrice'),
                ],
                    style={"display": "grid", "grid-template-columns": "10% 40% 10%"})

            ]),
            # html.Div(className='viz-container', children=[
            #     dcc.Graph(
            #         figure=fig2,
            #         config=dict(
            #             scrollZoom=False,
            #             showTips=False,
            #             showAxisDragHandles=False,
            #             doubleClick=False,
            #             displayModeBar=False
            #         ),
            #         className='sankey-link',
            #         id='viz_2'
            #     )
            # ]),
            # html.Div(className='viz-container', children=[
            #     dcc.Graph(
            #         figure=fig3,
            #         config=dict(
            #             scrollZoom=False,
            #             showTips=False,
            #             showAxisDragHandles=False,
            #             doubleClick=False,
            #             displayModeBar=False
            #         ),
            #         className='graph',
            #         id='viz_3'
            #     )
            # ]),
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
            html.Div(className='img-quebec', children=[
                html.Img(src="assets/Quebec_clusters.PNG",
                             id="quebec-cluster"),
                html.Div(className="overlay", children=[
                    html.Div(
                        'Les centres culturels sont les suivants:', className="title"),
                    html.Div(children=['Nord du Québec :',
                                       html.Div(className="text-nord", children=[
                                           'Abitibi-Témiscamingue',
                                           html.Div('Capitale-Nationale'),
                                           html.Div('Côte-Nord'),
                                           html.Div('Mauricie'),
                                           html.Div(
                                               'Nord-du-Québec et de la Baie-James'),
                                           html.Div(
                                               'Saguenay-Lac-Saint-Jean')
                                       ], style={'color': 'black'}),
                                       ], className="title-nord"),
                    html.Div(children=['Centre du Québec :',
                                       html.Div(className="text-centre", children=[
                                           'Centre-du-Québec',
                                           html.Div('Lanaudière'),
                                           html.Div('Laurentides'),
                                           html.Div('Laval'),
                                           html.Div('Outaouais')
                                       ], style={'color': 'black'}),
                                       ], className="title-centre"),
                    html.Div(children=['Sud du Québec :',
                                       html.Div(className="text-sud", children=[
                                           'Bas-Saint-Laurent',
                                           html.Div(
                                               'Chaudière-Appalaches'),
                                           html.Div('Estrie'),
                                           html.Div(
                                               'Gaspésie et îles-de-la-Madeleine'),
                                           html.Div('Montérégie')
                                       ], style={'color': 'black'}),
                                       ], className="title-sud"),
                    html.Div(children=['Montréal'],
                             className="title-montreal")
                ])
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
                    id='viz_5'
                )
            ]),
            # html.Div(className='viz-container', children=[
            #     dcc.Graph(
            #         figure=fig3,
            #         config=dict(
            #             scrollZoom=False,
            #             showTips=False,
            #             showAxisDragHandles=False,
            #             displayModeBar=False
            #         ),
            #         className='graph',
            #         id='viz_6'
            #     )
            # ]),
            html.Div(className='viz-container', children=[
                dcc.Graph(
                    figure=fig7,
                    config=dict(
                        scrollZoom=False,
                        showTips=False,
                        showAxisDragHandles=False,
                        displayModeBar=False
                    ),
                    className='graph',
                    id='viz_7'
                )
            ])
        ])
    ])


app.layout = init_app_layout(fig1, fig2, fig3, fig4, fig5, fig6)


with open('indexViz_alpha.html', 'a') as f:
    f.write(fig1.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig2.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig3.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig4.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig5.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig6.to_html(full_html=False, include_plotlyjs='cdn'))
    f.write(fig7.to_html(full_html=False, include_plotlyjs='cdn'))


@ app.callback(
    Output('viz_1', 'figure'),
    [Input(component_id='dropdownYear', component_property='value')],
    [Input(component_id='MonthsSlider', component_property='value')],
    [Input(component_id='dropdownRegion', component_property='value')],
    #[Input(component_id='minPrice', component_property='value')],
    [Input(component_id='PriceSlider', component_property='value')],
    #[Input(component_id='maxPrice', component_property='value')],


)
def figWithNewDf(selected_year, selected_month, selected_region, selected_price):
    print(selected_year)
    print(selected_month)
    print(selected_region)
    print(selected_price)
    print('hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh')
    if selected_region == 'Toutes les régions':
        print('ICI')
        return stackedBarChart.stackedBarChart(preproc.group_by_year_month(
            df, int(selected_year), int(selected_month)))
    else:
        return stackedBarChart.stackedBarChart(preproc.group_by_year_month_region(
            df, int(selected_year), int(selected_month), selected_region))
    # if new_df_selected.empty:
        # pymsgbox.alert('Pas d''événements pour la période choisie.', 'Avertissement')