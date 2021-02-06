import os
import dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output

from dash.testing.wait import until


def test_dltx001_download_text(dash_dcc):
    text = "Hello, world!"
    filename = "hello.txt"
    # Create app.
    app = dash.Dash(__name__)
    app.layout = html.Div(
        [dcc.Store(id="content", data=text), dcc.Download(id="download")]
    )

    @app.callback(Output("download", "data"), [Input("content", "data")])
    def download(content):
        return dcc.send_string(content, filename)

    # Check that there is nothing before starting the app
    fp = os.path.join(dash_dcc.download_path, filename)
    assert not os.path.isfile(fp)
    # Run the app.
    dash_dcc.start_server(app)

    # Check that a file has been download, and that it's content matches the original text.
    until(lambda: os.path.exists(fp), 5)
    with open(fp, "r") as f:
        content = f.read()
    assert content == text
