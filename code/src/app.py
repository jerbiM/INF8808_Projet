import  dash
from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import preprocess as preproc
import sankey
import stackedBarChart
import lineChart
import mapViz
import barchart
import json
import pandas as pd



# Load informations from geojson file to create the map of Quebec
with open("assets/Regions_Du_Quebec.json", "r") as response:
    qc = json.load(response)

df_file = "assets/data_prix.csv"

df = preproc.to_df(df_file)

df_N = preproc.to_df("assets/data_Cluster.csv")

#dfEventsCount = preproc.group_by_column_count(df, 'region')
# Create df from result obtained from dfEventsCount
d = {'region': ['Abitibi-Temiscamingue', 'Bas-Saint-Laurent', 'Capitale-Nationale', 'Centre-du-Quebec',
                'Chaudiere-Appalaches', 'Cote-Nord', 'Estrie', 'Gaspesie-iles-de-la-Madeleine',
                'Lanaudiere', 'Laurentides', 'Laval', 'Mauricie', 'Montreal', 'Monteregie',
                'Nord-du-Quebec', 'Outaouais', 'Saguenay-Lac-Saint-Jean'],
     'nombreEvenements': [63, 124, 1382, 1103, 99, 16, 578, 68, 480, 491, 177, 1216, 14693, 1715, 1, 282, 182]}
dfMap = pd.DataFrame(data=d)

# data preparation
repartition_region = preproc.to_df("assets/data_repartion_region.csv")
montreal_quartier = preproc.to_df("assets/data_montreal.csv")
clusters = preproc.add_cluster(repartition_region, montreal_quartier)

new_df = preproc.add_clusters(df, clusters)

df_sankey = preproc.add_clusters(df_N, clusters)

df_2021 = preproc.group_by_year_month(df, 2021, 12)


clus_est_gratuit_data = preproc.group_by_column2_count(
    df_sankey, 'groupe', 'est_gratuit')
df_barchart_gratuit = preproc.data_prepartion_barchart_gratuit(
    df_sankey, clus_est_gratuit_data)

# DataFrame for LineChart
df['count'] = 1

dfa = preproc.group_by_price(df, [0, 80])
dfa = preproc.group_by_selected_category(dfa, 'Musique')

df_final = dfa[['year', 'categorie', 'region', 'count']].groupby(
    ['year', 'categorie', 'region'], as_index=False).sum()


df_barchart_prix=preproc.data_prepartion_barchart_par_prix(df_sankey,"Montréal")

#Viz1,2,3 Maroua
fig10 = lineChart.lineChart(df_final)
fig9 = mapViz.mapQuebec(dfMap, qc)
fig1 = stackedBarChart.stackedBarChart(df_2021)



#Viz3 - Sankey Diagramme Nina
fig2 = sankey.sankey_diagram_g_cat(df_sankey)
fig3 = sankey.sankey_diagram_r_cat(df_sankey, 'Centre')
fig5 = sankey.sankey_diagram_r_cat(df_sankey, 'Sud')
fig6 = sankey.sankey_diagram_g_scat(df_sankey, 'ArtsVisuels')


#Viz6 - Barchart  Mahsa
fig7 = barchart.barchart_gratuit(df_barchart_gratuit)
fig8=barchart.barchart_filtrage(df_barchart_prix)


BS = "https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css"
app = Dash(external_stylesheets=[BS])
app.config.suppress_callback_exceptions=True



def init_app_layout(fig1,fig2,fig7,fig8,fig9,fig10):

	return dbc.Container(

		 #dbc.CardGroup(
		[

	#Cart Vide

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visualisation1 - Stacked Bar", className="card-title"),

					]
				),style={'backgroundColor':'#77E05A'}
			),

			# StackBarchart
			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Chronologie temporelle des événements et attentes financières", className="card-title"),

						html.Div([

							html.Div([
								dcc.Dropdown(
									options=[
										{'label': '2012', 'value': 2012},
										{'label': '2015', 'value': 2015},
										{'label': '2016', 'value': 2016},
										{'label': '2017', 'value': 2017},
										{'label': '2018', 'value': 2018},
										{'label': '2019', 'value': 2019},
										{'label': '2020', 'value': 2020},
										{'label': '2021', 'value': 2021},
										{'label': '2022', 'value': 2022},
										{'label': '2023', 'value': 2023},
										{'label': '2024', 'value': 2024},
										{'label': '2030', 'value': 2030}
									],
									value=2021,
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
							value=12
						),
						html.Label(['Choisir le range du prix en CAD'],
						           style={'font-weight': 'bold'}),
						html.Div([

							dcc.RangeSlider(
								id='PriceSlider',
								min=0,
								max=1000,
								value=[0, 1000],
								step=50,
								allowCross=False
							),
							# dcc.Input(type='text', id='maxPrice'),
						]),

					]
				)
			),
			#Cart Vide

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visualisation2 - LineChart", className="card-title"),

					]
				),style={'backgroundColor':'#77E05A'}
			),

			#linechart
			dbc.Card(
				dbc.CardBody([
					html.H5("Régions les plus chères selon les catégories", className="card-title"),
					html.Div([
						html.Div([
							dcc.Dropdown(
								options=[
									{'label': 'Musique', 'value': 'Musique'},
									{'label': 'ArtsVisuels',
									 'value': 'ArtsVisuels'},
									{'label': 'ÉvénementielAutre',
									 'value': 'ÉvénementielAutre'},
									{'label': 'Humour', 'value': 'Humour'},
									{'label': 'Théâtre', 'value': 'Théâtre'},
									{'label': 'Danse', 'value': 'Danse'},
									{'label': 'Cirque', 'value': 'Cirque'},
								],
								value='Musique',
								id='dropdownCategory'
							),
						], style={'width': '48%', 'display': 'inline-block'}),
						html.Label(['Choisir le prix'], style={
							'font-weight': 'bold'}),
						dcc.RangeSlider(
							id='PriceSliderLineChart',
							min=0,
							max=1000,
							value=[0, 1000],
							allowCross=False
						),
						dcc.Graph(figure=fig10,
						          config=dict(
							          scrollZoom=False,
							          showTips=False,
							          showAxisDragHandles=False,
							          doubleClick=False,
							          displayModeBar=False
						          ),
						          className='graph',
						          id='viz_10')
					]),

				])

			),

	#Cart Vide
			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visualisation3 - Map", className="card-title"),

					]
				),style={'backgroundColor':'#77E05A'}
			),
	#map Viz
			dbc.Card(
				dbc.CardBody([
					html.H5("Distribution des événements au Québec géographiquement", className="card-title"),
					html.Div([
						dcc.Graph(figure=fig9,
						          config=dict(
							          scrollZoom=False,
							          showTips=False,
							          showAxisDragHandles=False,
							          doubleClick=False,
							          displayModeBar=False
						          ),
						          className='graph',
						          id='viz_9')
					]),


				])

			),




			# Cart Vide
			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visulisation5 - Sankey Diagramme", className="card-title"),

					]
				), style={'backgroundColor': '#77E05A'}
			),
			#Sankey Diagram in groupe
			#dbc.CardGroup([
			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Guide for Visulisation5 - Sankey Diagramme", className="card-title"),
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

					]
				),
			),

			# Sankey Diagramme

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Sankey Diagramme", className="card-title"),
						html.Div(className='viz-container', children=[
							html.Div(id='sankey-container', children=[
								dcc.Graph(
									figure=fig2,
									config=dict(
										scrollZoom=False,
										showTips=False,
										showAxisDragHandles=False,
										displayModeBar=False
									),
									className='graph',
									id='sankey'
								)]),
							html.Div(dbc.Button("Retour au graphique initial", color="primary", id="reset-sankey"),
							         className='sankey-btn', id='sankey-btn', style={'visibility': 'hidden'})
						]),

					]
				)
			),
			#]),

			# Cart Vide

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visulisation6 - Bar Charts", className="card-title"),

					]
				), style={'backgroundColor': '#77E05A'}
			),

			# Barchart-Gratuit Diagramme

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Barchart Gratuits", className="card-title"),

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
						]),

					]
				)
			),

	# Cart Vide

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Visulisation6 - Bar Charts", className="card-title"),

					]
				), style={'backgroundColor': '#77E05A'}
			),


	# Barchart-Payant Diagramme

			dbc.Card(
				dbc.CardBody(
					[
						html.H5("Bar Charts Payant", className="card-title"),
						html.P(
							"Choisir une région",
							className="card-text",
						),
						html.Div([

							dbc.RadioItems(
								id="radiobutton",
								options=[
									{"label": "Montréal", "value": "Montréal"},
									{"label": "Sud", "value": "Sud"},
									{"label": "Centre", "value": "Centre"},
									{"label": "Nord", "value": "Nord"},
								],
								value="Montréal",
								labelCheckedClassName="text-success",
								inputCheckedClassName="border border-success bg-success",
							),
						]), dcc.Graph(
						figure=fig8,
						config=dict(
							scrollZoom=False,
							showTips=False,
							showAxisDragHandles=False,
							displayModeBar=False
						),
						className="p-5",
						id='viz_8'
					),
					]
				),




			),


		]
		# )
	)


app.layout = init_app_layout(fig1,fig2,fig7,fig8,fig9,fig10)
#fig3,fig5

@app.callback(
	Output('viz_1', 'figure'),
	[Input(component_id='dropdownYear', component_property='value')],
	[Input(component_id='MonthsSlider', component_property='value')],
	[Input(component_id='dropdownRegion', component_property='value')],
	[Input(component_id='PriceSlider', component_property='value')],

)
def figWithNewDf(selected_year, selected_month, selected_region, selected_price):

	if selected_region == 'Toutes les régions':

		return stackedBarChart.stackedBarChart(preproc.group_by_year_month_price(
			df, selected_year, selected_month, selected_price))
	else:

		return stackedBarChart.stackedBarChart(preproc.group_by_year_month_region_price(
			df, selected_year, selected_month, selected_region, selected_price))




@app.callback(
	Output('viz_10', 'figure'),
	[Input(component_id='dropdownCategory', component_property='value')],
	[Input(component_id='PriceSliderLineChart', component_property='value')]
)
def LineChartWithNewDf(selected_category, selected_price_lineChart):

	df['count'] = 1
	dfa = preproc.group_by_price(df, selected_price_lineChart)
	dfa = preproc.group_by_selected_category(dfa, selected_category)

	df_final = dfa[['year', 'categorie', 'region', 'count']].groupby(
		['year', 'categorie', 'region'], as_index=False).sum()

	return lineChart.lineChart(df_final)




@app.callback(
    Output(component_id='viz_8', component_property='figure'),
    Input(component_id='radiobutton', component_property='value')
)
def update_output_div(radiobutton):

    df_barchart_prix = preproc.data_prepartion_barchart_par_prix(df_sankey, radiobutton)
    fig8 = barchart.barchart_filtrage(df_barchart_prix)
    return fig8



@app.callback(
    [Output('sankey', 'figure')],
    [Input('sankey', 'clickData')],
    [State('sankey', 'figure')]
)
def display(clicks_fig, figure):  # noqa : E501 pylint: disable=unused-argument too-many-arguments line-too-long


    ctx = dash.callback_context

    if not ctx.triggered[0]['value']:
        return [figure]

    if not ctx.triggered[0]['value']['points'][0]['label']:
        # link -> modify color with its index

        # find what is the diagramm
        if "Nord" in ctx.states['sankey.figure']['data'][0]['node']['label']:
            # group with ?
            if "ArtsVisuels" in ctx.states['sankey.figure']['data'][0]['node']['label']:
                # group with categ
                fig = sankey.sankey_diagram_g_cat(df_sankey).to_dict()
            else:
                # group with sous cat
                cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split(
                )[-1]
                fig = sankey.sankey_diagram_g_scat(df_sankey, cond2).to_dict()

        else:
            # region with ?
            cond = ctx.states['sankey.figure']['layout']['title']['text'].split()[
                6]
            if "ArtsVisuels" in ctx.states['sankey.figure']['data'][0]['node']['label']:
                # group with categ
                fig = sankey.sankey_diagram_r_cat(df_sankey, cond).to_dict()
            else:
                # group with sous cat
                cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split(
                )[-1]
                fig = sankey.sankey_diagram_reg_scat(
                    df_sankey, cond, cond2).to_dict()

        click_index = ctx.triggered[0]['value']['points'][0]['index']
        return [sankey.change_color_link(figure, click_index)]

    # node -> modify

    click_node = ctx.triggered[0]['value']['points'][0]['label']

    node_group = list(df_sankey['groupe'].unique())
    node_cat = list(df_sankey['categorie'].unique())
    node_region = list(df_sankey['region'].unique())
    node_sous_cat = list(df_sankey['sousCategorie'].unique())

    # check in which case we are
    # if in node_region or node_sous_cat --> change color
    # else : change diagramm

    if click_node in node_group:
        if "ArtsVisuels" in ctx.states['sankey.figure']['data'][0]['node']['label']:
            return [sankey.sankey_diagram_r_cat(df_sankey, click_node)]
        cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split(
        )[-1]
        return [sankey.sankey_diagram_reg_scat(df_sankey, click_node, cond2)]

    elif click_node in node_cat:
        if "Nord" in ctx.states['sankey.figure']['data'][0]['node']['label']:
            return [sankey.sankey_diagram_g_scat(df_sankey, click_node)]
        cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split()[
            6]

        return [sankey.sankey_diagram_reg_scat(df_sankey, cond2, click_node)]

    elif click_node in node_region or click_node in node_sous_cat:

        # change color
        if "Nord" in ctx.states['sankey.figure']['data'][0]['node']['label']:
            # group with ?
            if "ArtsVisuels" in ctx.states['sankey.figure']['data'][0]['node']['label']:
                # group with categ
                fig = sankey.sankey_diagram_g_cat(df_sankey).to_dict()
            else:
                # group with sous cat
                cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split(
                )[-1]
                fig = sankey.sankey_diagram_g_scat(df_sankey, cond2).to_dict()

        else:
            # region with ?
            cond = ctx.states['sankey.figure']['layout']['title']['text'].split()[
                6]
            if "ArtsVisuels" in ctx.states['sankey.figure']['data'][0]['node']['label']:
                # group with categ
                fig = sankey.sankey_diagram_r_cat(df_sankey, cond).to_dict()
            else:
                # group with sous cat
                cond2 = ctx.states['sankey.figure']['layout']['title']['text'].split(
                )[-1]
                fig = sankey.sankey_diagram_reg_scat(
                    df_sankey, cond, cond2).to_dict()

        click_index = ctx.triggered[0]['value']['points'][0]['index']
        return [sankey.change_color_node(figure, click_index)]

    return figure

if __name__ == '__main__':
    app.run_server(debug=True)