import numpy as np
import pandas as pd
from sklearn.datasets import load_iris

import plotly.express as px

import dash
import dash_core_components as dcc
import dash_html_components as html

iris = load_iris() ## It returns simple dictionary like object with all data.

## Creating dataframe of total data
iris_df = pd.DataFrame(data=np.concatenate((iris.data,iris.target.reshape(-1,1)), axis=1), columns=(iris.feature_names+['Flower Type']))
iris_df["Flower Name"] = [iris.target_names[int(i)] for i in iris_df["Flower Type"]]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


header = html.H2(children="IRIS Dataset Analysis")

chart1 = px.scatter(data_frame=iris_df,
           x="sepal length (cm)",
           y="petal length (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="sepal length (cm) vs petal length (cm) color-encoded by flower type")


graph1 = dcc.Graph(
        id='graph1',
        figure=chart1,
        className="six columns"
    )

chart2 = px.scatter(data_frame=iris_df,
           x="sepal width (cm)",
           y="petal width (cm)",
           color="Flower Name",
           size=[1.0]*150,
           title="sepal width (cm) vs petal width (cm) color-encoded by flower type")


graph2 = dcc.Graph(
        id='graph2',
        figure=chart2,
        className="six columns"
    )

chart3 = px.histogram(data_frame=iris_df,
             x="sepal length (cm)",
             color="Flower Name",
             title="Distributions of sepal length (cm) color-encoded by flower name")

graph3 = dcc.Graph(
        id='graph3',
        figure=chart3,
        className="six columns"
    )

chart4 = px.box(data_frame=iris_df,
           x="Flower Name",
           y="sepal width (cm)",
           color="Flower Name",
           title="concentration of sepal width (cm) by flower types")


graph4 = dcc.Graph(
        id='graph4',
        figure=chart4,
        className="six columns"
    )



row1 = html.Div(children=[graph1, graph3],)

row2 = html.Div(children=[graph2, graph4])

layout = html.Div(children=[header, row1, row2], style={"text-align": "center"})

app.layout = layout

if __name__ == "__main__":
    app.run_server(debug=True)