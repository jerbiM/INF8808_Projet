from dash import dcc
import plotly.graph_objects as go
import hover_template as hover


def extract(data):
    data_dict = data.to_dict()
    vals = list() #list values
    sources = list()
    targets = list() #list keys
    for key, val in data_dict.items():
        sources.append(key[0])
        targets.append(key[1])
        vals.append(val)
    p1, p2 = percent_node(data_dict, sources+targets)
    return sources, targets, vals, p1, p2
    
def encode(labels, liste, n):
    name_code = dict()
    i = n
    for k in labels:
        name_code[k]=i
        i+=1
    return list(map(name_code.get,liste))

def group_by_column2_count(df, column, col2):
    data= df.groupby([column, col2])[column].count()
    label1_list = list(data.index.get_level_values(column).unique())
    label2_list = list(data.index.get_level_values(col2).unique())
    sources, targets, vals, p1, p2 = extract(data)
    l1 = encode(label1_list, sources, 0)
    l2 = encode(label2_list, targets, len(label1_list))
    return l1,l2,vals, label1_list+label2_list, p1, p2

def cond_group_by_column2_count(df, column, col2, col, cond):
    new_df = df[df[col] == cond]
    data = new_df.groupby([column, col2])[column].count()
    label1_list = list(data.index.get_level_values(column).unique())
    label2_list = list(data.index.get_level_values(col2).unique())
    sources, targets, vals, p1, p2 = extract(data)
    l1 = encode(label1_list, sources, 0)
    l2 = encode(label2_list, targets, len(label1_list))
    return l1,l2,vals, label1_list+label2_list, p1, p2

def percent_node(data_dict, labels):
    total = sum(data_dict.values())

    #sommes et pourcentages par groupe et par catégorie
    sumgc={i:0 for i in labels}

    pgc ={i:0 for i in labels}
    for key, val in data_dict.items():
        sumgc[key[0]]+=val
        sumgc[key[1]]+=val
        
    for key, val in sumgc.items():
        pgc[key]=(sumgc[key]/total)*100
    
    #pourcentages de chaque lien par rapport a groupe et categorie
    plink=list()
    for key, val in data_dict.items():
        plink.append((val/sumgc[key[0]]*100, val/sumgc[key[1]]*100))
    return list(pgc.values()), plink


    
def sankey_diagram_g_cat(df):

    source, target, values, label, p1, p2 = group_by_column2_count(df, 'groupe', 'categorie')
    
    #creat sankeyDiagram
    fig = go.Figure(data=[go.Sankey(
        arrangement='fixed',
        node=dict(
            pad=8,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
            color="#34347c",
            customdata = p1,
            hovertemplate = hover.sankey_hover_template_node()
            #line = {'color': '#7d8cb4'}
        ),
        link=dict(
            source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target,
            value=values,
            customdata = p2,
            color = 'rgba(218, 251, 251, 1)',
            hovertemplate= hover.sankey_hover_template_link()
            #color = '#7d8cb4',
        ))])
    fig.update_layout(title_text="Diagramme de Sankey des centres et catégories culturelles", font_size=10, font={'color': '#e72489'}, title_font_color= 'black')
    return fig

def sankey_diagram_r_cat(df, cond):

    source, target, values, label, p1, p2 = cond_group_by_column2_count(df, 'region', 'categorie', 'groupe', cond)
    

    #creat sankeyDiagram
    fig = go.Figure(data=[go.Sankey(
        arrangement='fixed',
        node=dict(
            pad=8,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
            color="#34347c",
            customdata = p1,
            hovertemplate = hover.sankey_hover_template_node()
            #line = {'color': '#7d8cb4'}
        ),
        link=dict(
            source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target,
            value=values,
            customdata = p2,
            color = 'rgba(218, 251, 251, 1)',
            hovertemplate= hover.sankey_hover_template_link()
            #color = '#7d8cb4',
        ))])
    fig.update_layout(title_text="Diagramme de Sankey des régions de "+cond+ " et des catégories culturelles", font_size=10, font={'color': '#e72489'}, title_font_color= 'black')
    return fig

def sankey_diagram_g_scat(df, cond):

    # create labels
    source, target, values, label, p1, p2 = cond_group_by_column2_count(df, 'groupe', 'sousCategorie', 'categorie', cond)
    
    #creat sankeyDiagram
    fig = go.Figure(data=[go.Sankey(
        arrangement='fixed',
        node=dict(
            pad=8,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
            color="#34347c",
            customdata = p1,
            hovertemplate = hover.sankey_hover_template_node()
            #line = {'color': '#7d8cb4'}
        ),
        link=dict(
            source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target,
            value=values,
            customdata = p2,
            color = 'rgba(218, 251, 251, 1)',
            hovertemplate= hover.sankey_hover_template_link()
            #color = '#7d8cb4',
        ))])
    
    fig.update_layout(title_text="Diagramme de Sankey des centres et des sous-catégories de "+cond, font_size=10, font={'color': '#e72489'}, title_font_color= 'black')

    return fig

def sankey_diagram_reg_scat(df, cond, cond2):

    # create labels
    source, target, values, label, p1, p2 = cond_group_by_column2_count(df, 'region', 'sousCategorie', 'groupe', cond)

    
    #creat sankeyDiagram
    fig = go.Figure(data=[go.Sankey(
        arrangement='fixed',
        node=dict(
            pad=8,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label,
            color="#34347c",
            customdata = p1,
            hovertemplate = hover.sankey_hover_template_node()
            #line = {'color': '#7d8cb4'}
        ),
        link=dict(
            source=source,  # indices correspond to labels, eg A1, A2, A1, B1, ...
            target=target,
            value=values,
            customdata = p2,
            color = 'rgba(218, 251, 251, 1)',
            hovertemplate= hover.sankey_hover_template_link()
            #color = '#7d8cb4',
        ))])
    
    fig.update_layout(title_text="Diagramme de Sankey des régions de "+cond+ " et des sous-catégories de "+cond2, font_size=10, font={'color': '#e72489'}, title_font_color= 'black')

    return fig

def change_color_link(figure, index):
    if figure['data'][0]['link']['color'] == 'rgba(218, 251, 251, 1)':
    
        nb_value = len(figure['data'][0]['link']['value'])
        
        colors = []
        for i in range(nb_value):
            if i != index:
                colors.append("rgba(218, 251, 251, 0.5)")
            else :
                colors.append("rgba(52, 52, 124, 0.5)") #here change node color
    
        figure['data'][0]['link']['color'] = colors
    
    else :
        if figure['data'][0]['link']['color'][index]=="rgba(52, 52, 124, 0.5)":
            figure['data'][0]['link']['color'][index]="rgba(218, 251, 251, 0.5)"
        else:
            figure['data'][0]['link']['color'][index]="rgba(52, 52, 124, 0.5)"
    

    fig = go.Figure(figure)
    return fig
    raise Exception("change color link function not implemented")

def change_color_node(figure, index):
    
    if figure['data'][0]['node']['color'] == '#34347c':
    #change node color
        curr_color = figure['data'][0]['node']['color']
        nb_label = len(figure['data'][0]['node']['label'])

        colors = []
        for i in range(nb_label):
            if i != index:
                colors.append(curr_color)
            else :
                colors.append("rgba(231, 36, 137, 0.7)") #here change node color
    
        figure['data'][0]['node']['color'] = colors

    else :
        if figure['data'][0]['node']['color'][index]=="rgba(231, 36, 137, 0.7)":
            figure['data'][0]['node']['color'][index]="rgba(52, 52, 124, 1)"
        else:
            figure['data'][0]['node']['color'][index]="rgba(231, 36, 137, 0.7)"
    
    #finds indexes of the node
    
    uniq_value_source = set(figure['data'][0]['link']['source'])
    
    indexes= list()
    if index in uniq_value_source:
        for idx, val in enumerate(figure['data'][0]['link']['source']):
            if val == index:
                indexes.append(idx)
        #indexes = [idx for idx, val in enumerate(figure['data'][0]['link']['source']) if val in figure['data'][0]['link']['source'][:idx]]
    else :
        for idx, val in enumerate(figure['data'][0]['link']['target']):
            if val == index:
                indexes.append(idx)
    

    if figure['data'][0]['link']['color'] == 'rgba(218, 251, 251, 1)':
    
        nb_value = len(figure['data'][0]['link']['value'])
        
        colors_l = []
        for i in range(nb_value):
            if i in indexes:
                colors_l.append("rgba(52, 52, 124, 0.5)")
            else :
                colors_l.append("rgba(0, 0, 0, 0)") #here change node color
    
        figure['data'][0]['link']['color'] = colors_l
    
    else :
        for idx in indexes :
            if figure['data'][0]['link']['color'][idx]=="rgba(0, 0, 0, 0)" or figure['data'][0]['link']['color'][idx]=="rgba(218, 251, 251, 1)":
                figure['data'][0]['link']['color'][idx]="rgba(52, 52, 124, 0.5)"
            else:
                figure['data'][0]['link']['color'][idx]="rgba(0, 0, 0, 0)"
    

    setc = set(figure['data'][0]['link']['color'])

    if len(set(figure['data'][0]['link']['color']))==1:
        #all link are white
        figure['data'][0]['link']['color'] = 'rgba(218, 251, 251, 1)'

    fig = go.Figure(figure)
    return fig
