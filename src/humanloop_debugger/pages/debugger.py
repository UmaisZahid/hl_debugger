from collections import Counter
from textwrap import dedent
import base64
import glob, os
import pkgutil

import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, State, Output
import pandas as pd
import plotly.express as px

from ..app import app

file_df = None
API_KEY = "fe20f8db14ca9cec47e9b1c9d982da9f"

def get_layout(**kwargs):
    initial_text = kwargs.get("text", "Type some text into me!")

    # Note that if you need to access multiple values of an argument, you can
    # use args.getlist("param")
    return html.Div(
        [
            dcc.Markdown(
                dedent(
                    """
                    ## Upload Data!

                    """
                )
            ),
            dbc.FormGroup(
                [

                    dbc.Label("Upload your data:"),
                    html.P('Currently using default data', style={"font-weight":"bold"}, id="default_label"),
                    dcc.Upload(
                        id='upload-data',
                        children=html.Div([
                            'Drag and Drop or ',
                            html.A('Select Files'),
                        ]),
                        style={
                            'width': '100%',
                            'height': '60px',
                            'lineHeight': '60px',
                            'borderWidth': '1px',
                            'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'margin': '10px'
                        },
                        # Allow multiple files to be uploaded
                        multiple=False
                    ),
                ]
            ),
            dbc.FormGroup(
                [
                    dcc.Markdown(
                        dedent(
                            """
                            ### Classifier Entropy
                            Entropy is one way of determining how "confused" a classifier is about a prediction.
                            High entropy denotes less certainty.
                            """
                        )
                    ),
                    dbc.FormGroup(
                        [
                            dbc.Label("Split by usage or intent/class", width=3),
                            dbc.RadioItems(
                                id="usage_or_intent",
                                options=[
                                        {"label":"Usage", "value": "usage"},
                                        {"label":"Intent", "value": "intent"}
                                    ],
                                value="intent", inline=True
                            )
                        ], row=True
                    ),
                    dcc.Graph(id="graph"),
                ]
            ),
            dbc.FormGroup(
                [
                    dcc.Markdown(
                        dedent(
                            """
                            ### Entropy Quantiles Per Class or Usage
                            """
                        )
                    ),
                    dcc.Graph(id="average_entropy_graph"),
                ]
            ),
            dbc.FormGroup(
                [
                    dcc.Markdown(
                        dedent(
                            """
                            ### Enrich Data with Predictions
                            Functionality incomplete due to internal server errors via HumanLoop API
                            """
                        )
                    ),
                    html.Div(
                        [
                        dash_table.DataTable(
                            id="data_table"
                        ),
                        ], id="data_table_container"
                    ),
                ]
            ),
        ]
    )

@app.callback(
    [
        Output("graph", "figure"),
        Output("default_label", "children"),
        Output("average_entropy_graph", "figure"),
        Output("data_table_container", "children"),
    ],
    [
        Input("upload-data", "contents"),
        Input("usage_or_intent", "value"),
    ],
    [
        State("upload-data", "filename"),
        State("default_label", "children"),
    ],  # States
)
def parse_file_callback(contents, usage_or_intent, filename, label):

    ctx = dash.callback_context

    global file_df

    if not ctx.triggered:
        default_json_file = pkgutil.get_data("humanloop_debugger", "data/chatbot_intent_classifier_data.json")
        file_df_raw = pd.read_json(default_json_file)
        label = f"Using default chat classifier data"
    elif contents is not None and "json" in filename:
        _, content_string = contents.split(',')
        contents = base64.b64decode(content_string)
        file_df_raw = pd.read_json(contents)
        label = f"Using user provided data"

    if ctx.triggered[0]["prop_id"].split(".")[0] != "usage_or_intent":
        file_df_data = pd.DataFrame.from_records(file_df_raw["data"].apply(eval).tolist())
        file_df = pd.concat([file_df_raw, file_df_data], axis=1)
        file_df["intent"] = file_df["intent"].fillna("").astype(str).fillna("Missing").str.strip().replace("", "Missing")
        file_df["usage"] = file_df["usage"].fillna("").astype(str).fillna("Missing").str.strip().replace("", "Missing")
        file_df["text"] = file_df["text"].fillna("").astype(str).fillna("Missing").str.strip().replace("", "Missing")
        file_df["Cached Predictions"] = ""

    fig = px.scatter(file_df, x="id", y="score", color=usage_or_intent, hover_data=["text", "intent", "usage"], log_y=True, height=800,
                        title="Entropy Score")

    fig_average = px.box(file_df, x=usage_or_intent, y="score", log_y=True, hover_data=["text", "intent", "usage"])

    table = dash_table.DataTable(
        data=file_df.sort_values(by="score", ascending=False).to_dict('records'),
        columns=[{"id": "text", "name": "Text"},
                 {"id": "intent", "name": "Intent"},
                 {"id": "usage", "name": "Usage"},
                 {"id": "score", "name": "Entropy Score"},
                 {"id": "Cached Predictions", "name": "Cached Predictions"},
        ],
        page_size=10,
        style_cell={
                'whiteSpace': 'normal',
                'height': 'auto',
            },

    )
    return fig, label, fig_average, [table]
