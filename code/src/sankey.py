import plotly.graph_objects as go



def sankey_daigram(clus_cat_data,categorie_data,clusters):

	# create labels
	key_list = list(clusters.keys())
	key_list.sort()
	
	source = [i for i in range(len(list(clusters.keys()))) for j in range(len(list(categorie_data.index)))]
	target = [4 + j for i in range(len(list(clusters.keys()))) for j in range(len(list(categorie_data.index)))]
	values = list()
	for row in clus_cat_data:
		values.append(row)

	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=15,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=list(clusters.keys()) + list(categorie_data.index),
			color="blue"
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values
		))])

	return fig
