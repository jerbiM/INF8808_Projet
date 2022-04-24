from dash import Dash, dcc,html
import dash_bootstrap_components as dbc

from dash.dependencies import Input, Output
import heatmap
import preprocess as preproc
import os


# print("Current path : " + os.getcwd())
# print("Folders in path : ", os.listdir('.'))
# os.chdir("code/src/assets")
# print("Current path : " + os.getcwd())
# print("Folders in path : ", os.listdir('.'))
df_file_preprocessed = "code/src/assets/df_ghali_v3.csv"
df_preprocessed = preproc.to_df(df_file_preprocessed)
low_density_years = [2012, 2015, 2024 , 2030]
df = df_preprocessed[~df_preprocessed.year.isin(set(low_density_years))]
fig4 = heatmap.filter_plot_heatmap(df, [2021], 
                                ["all"], 
                                "all", 
                                "all")

app = Dash(__name__)

app.layout = html.Div([

#######################################################################
# Radio buttons for year
#######################################################################
html.Div(
    [
        dbc.Label("Année : "),
        dbc.Checklist(
            options=[
                {"label": "2016", "value": 2016},
                {"label": "2017", "value": 2017},
                {"label": "2018", "value": 2018},
                {"label": "2019", "value": 2019},
                {"label": "2020", "value": 2020},
                {"label": "2021", "value": 2021},
                {"label": "2022", "value": 2022},
                {"label": "2023", "value": 2023},
                {"label": "Toutes les années", "value": 0},
            ],
            value=[2021],
            id="bullets_year",
        ),
    ]
),
#######################################################################

#######################################################################
# Radio buttons for category
#######################################################################
html.Div(
    [
        dbc.Label("Catégorie : "),
        dbc.Checklist(
            options=[
                {"label": "Musique", "value": "Musique"},
                {"label": "Théatre", "value": "Théâtre"},
                {"label": "Arts visuels", "value": "ArtsVisuels"},
                {"label": "Humour", "value": "Humour"},
                {"label": "Danse", "value": "Danse"},
                {"label": "Cirque", "value": "Cirque"},
                {"label": "Autre", "value": "ÉvénementielAutre"},
                {"label": "Toute catégorie", "value": "all"},
            ],
            value=["all"],
            id="bullets_category",
        ),
    ]
),
#######################################################################

#######################################################################
# Radio buttons for price
#######################################################################
html.Div(
    [
        dbc.Label("Prix : "),
        dbc.Checklist(
            options=[
                {"label": "Gratuit", "value": "free"},
                {"label": "Payant", "value": "pricy"},
                {"label": "Voir tout", "value": "all"},
                {"label": "Comparer gratuit et payant", "value": "compare"},
            ],
            value="all",
            id="bullets_price",
        ),
    ]
),
#######################################################################

#######################################################################
# Radio buttons for Modality
#######################################################################
html.Div(
    [
        dbc.Label("Modalité : "),
        dbc.Checklist(
            options=[
                {"label": "Virtuel", "value": "online"},
                {"label": "Présentiel", "value": "inperson"},
                {"label": "Voir tout", "value": "all"},
                {"label": "Comparer virtuel et présentiel", "value": "compare"},
            ],
            value="all",
            id="bullets_modality",
        ),
    ]
),
#######################################################################

#######################################################################
# Viz
#######################################################################
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
])
#######################################################################
                 ])



@app.callback(

    Output("viz_4", 'figure'),
    Input('bullets_year', 'value'),
    Input('bullets_category', 'value'),
    Input('bullets_price', 'value'),
    Input('bullets_modality', 'value'),
    
   # [Input(component_id='radio-selected-style', component_property='value')],
)

def showfig4(bullets_year, bullets_category, bullets_price, bullets_modality):
    print("Year is ",bullets_year)
    print("Category is ",bullets_category)
    print("Price is ",bullets_price)
    print("Modality is ",bullets_modality)
    #return heatmap.make_heatmap(df_preprocessed, years=set(testradio))
    return heatmap.filter_plot_heatmap(df, bullets_year, 
                                bullets_category, 
                                bullets_price, 
                                bullets_modality)




if __name__ == "__main__":
    app.run_server(debug=True)