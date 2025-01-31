from pathlib import Path
from typing import Optional
from dash import dcc, html, Input, Output, register_page, callback
import plotly.express as px
import numpy as np
from dash.html import Figure
from src.utils.data_loader import load_image


register_page(__name__, path="/lbs")

SAMPLE_IMAGES = {
    'X-ray': 'assets/images/xray.jpeg',
    'CT': 'assets/images/ct.jpg',
    'MRI': 'assets/images/mri.jpg',
    'Ultrasound': 'assets/images/ultrasound.jpg',
    'Histology': 'assets/images/histology.jpg'
}

layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Explore Modalities', children=[
            html.Div([
                html.Label('Select Imaging Modality:'),
                dcc.Dropdown(
                    id='modality-dropdown',
                    options=[{'label': key, 'value': key} for key in SAMPLE_IMAGES.keys()],
                    value='X-ray'
                ),
                html.Label('Adjust Contrast:'),
                dcc.Slider(id='contrast-slider', min=0.5, max=2.0, step=0.1, value=1.0),
                html.Label('Adjust Resolution:'),
                dcc.Slider(id='resolution-slider', min=0.5, max=1.5, step=0.1, value=1.0),
                dcc.Graph(id='image-display')
            ])
        ]),
        dcc.Tab(label='Modality Selection', children=[
            html.Div([
                html.Label('Case Scenario: A patient with suspected brain hemorrhage.'),
                dcc.RadioItems(
                    id='modality-selection',
                    options=[{'label': key, 'value': key} for key in SAMPLE_IMAGES.keys()],
                    value=None
                ),
                html.Div(id='modality-feedback')
            ])
        ]),
        dcc.Tab(label='Compare Modalities', children=[
            html.Div([
                html.Label('Select Imaging Modalities to Compare:'),
                dcc.Dropdown(
                    id='compare-modalities',
                    options=[{'label': key, 'value': key} for key in SAMPLE_IMAGES.keys()],
                    value=['X-ray', 'CT'],
                    multi=True
                ),
                dcc.Graph(id='comparison-display')
            ])
        ])
    ])
])


@callback(
    Output('image-display', 'figure'),
    [Input('modality-dropdown', 'value'),
     Input('contrast-slider', 'value'),
     Input('resolution-slider', 'value')]
)
def update_exercise_1(modality: str, contrast: float, resolution: float):
    img_path = Path(SAMPLE_IMAGES.get(modality))
    img = load_image(img_path, contrast, resolution)
    if img is not None:
        fig = px.imshow(img, color_continuous_scale='gray', title=f'{modality} Image')
        fig.update_layout(coloraxis_showscale=False)
        return fig
    return px.imshow(np.zeros((10, 10)), title='Image not found')


@callback(
    Output('modality-feedback', 'children'),
    Input('modality-selection', 'value')
)
def update_exercise_2(selected_modality: Optional[str]) -> str:
    if selected_modality is None:
        return 'Which modality would you use in this situation?'
    if selected_modality == 'CT':
        return 'Correct! CT scans are often used for brain hemorrhage detection due to their high tissue contrast'
    return 'Consider using a modality with better tissue contrast for brain hemorrhages.'


@callback(
    Output('comparison-display', 'figure'),
    Input('compare-modalities', 'value')
)
def update_exercise_3(modalities: list[str]) -> Figure:
    if len(modalities) == 2:
        img_1 = load_image(Path(SAMPLE_IMAGES.get(modalities[0])))
        img_2 = load_image(Path(SAMPLE_IMAGES.get(modalities[1])))
        if img_1 is not None and img_2 is not None:
            fig = px.imshow(np.hstack([img_1, img_2]), color_continuous_scale="gray", title="Comparison")
            fig.update_layout(coloraxis_showscale=False)
            return fig
    return px.imshow(np.zeros((10, 10)), title="Select two modalities")
