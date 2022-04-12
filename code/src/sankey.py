import plotly.graph_objects as go



def group_by_column2_count(df, column, col2):
    data= df.groupby([column, col2])[column].count()
    label1_list = list(data.index.get_level_values(column).unique())
    label2_list = list(data.index.get_level_values(col2).unique())
    return label1_list,label2_list, data

def cond_group_by_column2_count(df, column, col2, col, cond):
    new_df = df[df[col] == cond]
    data = new_df.groupby([column, col2])[column].count()
    label1_list = list(data.index.get_level_values(column).unique())
    label2_list = list(data.index.get_level_values(col2).unique())
    return label1_list,label2_list, data

def sankey_diagram_g_cat(df):

	l1, l2, data = group_by_column2_count(df, 'groupe', 'categorie')
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list()
	label = l1+l2
	for row in data:
		values.append(row)

	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			color = '#dafbfb',
			#color = '#7d8cb4',
		))])

	return fig

def sankey_diagram_r_cat(df, cond):

	l1, l2, data = cond_group_by_column2_count(df, 'region', 'categorie', 'groupe', cond)
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list()
	label = l1+l2
	for row in data:
		values.append(row)

	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			color = '#dafbfb',
			#color = '#7d8cb4',
		))])

	return fig

def sankey_diagram_g_scat(df, cond):

	# create labels
	l1, l2, data = cond_group_by_column2_count(df, 'groupe', 'sousCategorie', 'categorie', cond)
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list()
	label = l1+l2
	for row in data:
		values.append(row)
	
	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			color = '#dafbfb',
			#color = '#7d8cb4',
		))])

	return fig

