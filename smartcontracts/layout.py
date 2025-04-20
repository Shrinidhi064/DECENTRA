import dash
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dummy layouts for each tab
layouts = {
    "overview": html.Div([html.H3("Overview Content"), html.P("Welcome to the overview.")]),
    "tab2": html.Div([html.H3("Tab 2 Content"), html.P("Details for Tab 2.")]),
    "tab3": html.Div([html.H3("Tab 3 Content"), html.P("Details for Tab 3.")]),
    "tab4": html.Div([html.H3("Tab 4 Content"), html.P("Details for Tab 4.")]),
}

# App layout with overview preloaded
app.layout = dbc.Container([
    dcc.Location(id="url", refresh=False),  # Tracks page URL
    dbc.Tabs(id="tabs", active_tab="overview", children=[
        dbc.Tab(label="Overview", tab_id="overview",),
        dbc.Tab(label="Tab 2", tab_id="tab2"),
        dbc.Tab(label="Tab 3", tab_id="tab3"),
        dbc.Tab(label="Tab 4", tab_id="tab4"),
    ]),
    html.Div(id="tab-content", children=layouts["overview"])  # Preload Overview Content
])

# Callback to switch tabs dynamically
@app.callback(
    Output("tab-content", "children"),
    Input("tabs", "active_tab")
)
def render_tab(active_tab):
    return layouts.get(active_tab, layouts["overview"])  # Default to "overview"

if __name__ == "__main__":
    app.run_server(debug=True)
