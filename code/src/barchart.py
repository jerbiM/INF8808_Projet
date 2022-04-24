import plotly.express as px
import hover_template as hover
def barchart_gratuit(df):


	fig = px.bar(df, x='groupe', y=['événements_gratuits','événement_payant'],
	             color_discrete_map={
		             'événements_gratuits': '#DDB5B5',
		             'événement_payant': '#840921'
	             }
	             )
	newnames = {'événements_gratuits': 'Les événements gratuits', 'événement_payant': 'Les événenments payants'}

	fig.update_traces( hovertemplate=hover.barchart_gratuit())
	fig.update_layout(

		xaxis_title="Régions du Québec",
		yaxis_title="Nombre d'événements",
		legend={'title_text': "Type d'événements"},
		paper_bgcolor='rgb(233,233,233)',  # set the background colour
		plot_bgcolor='rgb(233,233,233)'

	)
	fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))
	return fig




def barchart_filtrage(df):

	#interval of prrice
	seuil1='{}  ≥ prix < {}'.format(df['seuil1_value'][0],df['seuil2_value'][0])
	seuil2='{}  ≥ prix < {}'.format(df['seuil2_value'][0],df['seuil3_value'][0])
	seuil3='{}  ≥ prix ≤ {}'.format(df['seuil3_value'][0],df['seuil4_value'][0])

	newnames = {'seuil1':seuil1, 'seuil2':seuil2, 'seuil3': seuil3}

	list_prix=[df['seuil1_value'],df['seuil2_value'],df['seuil3_value'],df['seuil4_value']]
	fig = px.bar(df, x='categorie', y=['seuil1','seuil2','seuil3'],
	color_discrete_map = {
		'seuil1': '#D7B1D3',
		'seuil2': '#B71184',
		'seuil3': '#6F0A55',

	},
	    hover_data=list_prix

	)

	fig.update_layout(
		xaxis_title="Catégories",
		yaxis_title="Nombre d'événements",
		legend={'title_text': "Les intervalles du prix"},
		paper_bgcolor='rgb(233,233,233)',  # set the background colour
		plot_bgcolor='rgb(233,233,233)'

	)

	fig.update_traces(hovertemplate=hover.barchart_payant())

	#show intervalle
	fig.for_each_trace(lambda t: t.update(name=newnames[t.name]))

	return fig


