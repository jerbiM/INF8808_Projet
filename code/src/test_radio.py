from dash import Dash, dcc
from dash.dependencies import Input, Output


app = Dash(__name__)

app.layout = dcc.RadioItems(
   options={
        'New York City': 'New York City',
        'Montreal': 'Montreal',
        'San Francisco': 'San Francisco'
   },
   value='Montreal',
    id="testradio"

   ,inline=True)

viz_heatmap = 

@app.callback(

    Output("viz_heatmap", 'figure'),
    Input('testradio', 'value')
   # [Input(component_id='radio-selected-style', component_property='value')],
)

def showfig8(testradio):
    print(testradio)


if __name__ == "__main__":
    app.run_server(debug=True)