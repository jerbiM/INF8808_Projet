import plotly.graph_objects as go
from src import hover_template as hover


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

def percent(l1, l2, data):
    total = sum(data)

    #sommes et pourcentages par groupe
    sumg=list()
    pg = list()
    for i in l1:
        sumg.append(sum(data.loc[i]))
        pg.append(sum(data.loc[i])/total*100)
    #sommes et pourcentages par categorie
    sumcat=list()
    pcat=list()
    
    for i in l2:
        sumcatj=0
        for j in l1:
            if (j,i) in data.keys():
                sumcatj+=data.loc[j,i]
        sumcat.append(sumcatj)
        pcat.append(sumcatj/total*100)
    
    #pourcentages de chaque lien par rapport a groupe et categorie
    plink=list()
    idj=0
    for j in l1:
        idi=0
        for i in l2:
            if (j,i) in data.keys():
                plink.append((data.loc[j,i]/sumg[idj]*100,data.loc[j,i]/sumcat[idi]*100))
            idi+=1
        idj+=1
    return pg+pcat, plink


	
def sankey_diagram_g_cat(df):

	l1, l2, data = group_by_column2_count(df, 'groupe', 'categorie')
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list(data.values)
	label = l1+l2
	
	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			customdata = percent(l1, l2, data)[0],
			hovertemplate = hover.sankey_hover_template_node()
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			customdata = percent(l1, l2, data)[1],
			color = '#dafbfb',
			hovertemplate= hover.sankey_hover_template_link()
			#color = '#7d8cb4',
		))])
	fig.update_layout(#title_text="Diagramme de Sankey des centres et catégories culturelles",
	                  font_size=10,
					font={'color': '#e72489'},
		#title_font_color= 'black'
	)
	return fig

def sankey_diagram_r_cat(df, cond):

	l1, l2, data = cond_group_by_column2_count(df, 'region', 'categorie', 'groupe', cond)
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list(data.values)
	label = l1+l2

	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			customdata = percent(l1, l2, data)[0],
			hovertemplate = hover.sankey_hover_template_node()
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			customdata = percent(l1, l2, data)[1],
			color = '#dafbfb',
			hovertemplate= hover.sankey_hover_template_link()
			#color = '#7d8cb4',
		))])
	fig.update_layout(title_text="Diagramme de Sankey des régions de "+cond+ " et des catégories culturelles", font_size=10, font={'color': '#e72489'}, title_font_color= 'black')
	return fig

def sankey_diagram_g_scat(df, cond):

	# create labels
	l1, l2, data = cond_group_by_column2_count(df, 'groupe', 'sousCategorie', 'categorie', cond)
	
	source = [i for i in range(len(l1)) for j in range(len(l2))]
	target = [4 + j for i in range(len(l1)) for j in range(len(l2))]
	values = list(data.values)
	label = l1+l2
	
	#creat sankeyDiagram
	fig = go.Figure(data=[go.Sankey(
		node=dict(
			pad=8,
			thickness=20,
			line=dict(color="black", width=0.5),
			label=label,
			color="#34347c",
			customdata = percent(l1, l2, data)[0],
			hovertemplate = hover.sankey_hover_template_node()
			#line = {'color': '#7d8cb4'}
		),
		link=dict(
			source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
			target=target,
			value=values,
			customdata = percent(l1, l2, data)[1],
			color = '#dafbfb',
			hovertemplate= hover.sankey_hover_template_link()
			#color = '#7d8cb4',
		))])
	
	fig.update_layout(title_text="Diagramme de Sankey des centres et des sous-catégories de "+cond, font_size=10, font={'color': '#e72489'}, title_font_color= 'black')

	return fig