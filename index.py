from dash import exceptions
from app import app
from app import server
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
import threading
import base64
import plotly.graph_objects as ply_go

# import sys
# sys.path.append('/media/yy7/F00E06B10E0670C0/Users/YY7/Desktop/DESK/Files/PRG/Inno Code/DE/project')
import logic as DE

class Master_plotter:
    de:DE.DE
    meth:DE.Solution_plotter
    max_gte:DE.GTE_plotter

    def __init__(self) -> None:
        self.de = DE.DE(DE.Initial_value(2, 12, 0))
        self.meth = DE.Solution_plotter(self.de, 10)
        self.meth.calc_and_save_all()
        
        self.max_gte = DE.GTE_plotter(self.de, 10, 100)
        self.max_gte.calc_and_save_all()

        self.load_solution()
        self.load_max_gte()


    def change_solution_iv(self, iv, n):
        self.de.set_initial_value(iv)
        self.meth.set_n(n)
        th = threading.Thread(target=self.meth.calc_and_save_all)
        th.start()
        th.join()
        
        
    def change_gte_bounds(self, n0, n):
        self.max_gte.set_bounds(n0, n)
        th = threading.Thread(target=self.max_gte.calc_and_save_all)
        th.start()
        th.join()
    
    def load_solution(self):
        self.exact_csv = pd.read_csv('data/exact.csv')
        self.exact_domain = self.exact_csv['x']
        self.exact_solution = self.exact_csv['y(x)']

        self.euler_csv = pd.read_csv('data/euler.csv')
        self.euler_solution = self.euler_csv['y(x)']
        self.euler_lte = self.euler_csv['LTE']
        self.euler_gte = self.euler_csv['GTE']

        self.im_euler_csv = pd.read_csv('data/im_euler.csv')
        self.im_euler_solution = self.im_euler_csv['y(x)']
        self.im_euler_lte = self.im_euler_csv['LTE']
        self.im_euler_gte = self.im_euler_csv['GTE']

        self.rg_kt_csv = pd.read_csv('data/rg_kt.csv')
        self.rg_kt_solution = self.rg_kt_csv['y(x)']
        self.rg_kt_lte = self.rg_kt_csv['LTE']
        self.rg_kt_gte = self.rg_kt_csv['GTE']

    def load_max_gte(self):
        self.gte_euler_csv = pd.read_csv('data/gte_euler.csv')
        self.gte_euler = self.gte_euler_csv['max GTE']

        self.gte_im_euler_csv = pd.read_csv('data/gte_im_euler.csv')
        self.gte_im_euler = self.gte_im_euler_csv['max GTE']

        self.gte_rg_kt_csv = pd.read_csv('data/gte_rg_kt.csv')
        self.gte_rg_kt = self.gte_rg_kt_csv['max GTE']
        self.gte_domain = self.gte_rg_kt_csv['x']
        # print(len(self.gte_domain))
    
    def gen_solution_fig(self):
        fig = ply_go.Figure()
        # fig_eu = ply_go.Figure()
        # fig_ieu = ply_go.Figure()
        fig.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.exact_solution,
                # type='line', 
                name='Exact Solution'
            )
        )
        fig.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.rg_kt_solution,
                # type='line', 
                name='Range-Kerutta Method'
            )
        )
        fig.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.im_euler_solution,
                # type='line', 
                name='Improved Euler Method'
            )
        )
        # fig_rg = ply_go.Figure()
        fig.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.euler_solution,
                # type='line', 
                name='Euler Method'
            )
        )
        fig.update_layout(
                title={
                    'text': 'Solution',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'y': 0.9,
                    'x': 0.5,
                },
            )
        
        fig_lte = ply_go.Figure()
        fig_lte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.euler_lte,
                # type='line', 
                name='Euler Method'
            )
        )
        fig_lte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.im_euler_lte,
                # type='line', 
                name='Improved Euler Method'
            )
        )
        fig_lte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.rg_kt_lte,
                # type='line', 
                name='Range-Kerutta Method'
            )
        )
        # fig_rg = ply_go.Figure()
        fig_lte.update_layout(
                title={
                    'text': 'LTE',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'y': 0.9,
                    'x': 0.5,
                },
            )
        
        fig_gte = ply_go.Figure()
        fig_gte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.euler_gte,
                # type='line', 
                name='Euler Method'
            )
        )
        fig_gte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.im_euler_gte,
                # type='line', 
                name='Improved Euler Method'
            )
        )
        fig_gte.add_trace(
            ply_go.Line(
                x = self.exact_domain,
                y = self.rg_kt_gte,
                # type='line', 
                name='Range-Kerutta Method'
            )
        )
        # fig_rg = ply_go.Figure()
        fig_gte.update_layout(
                title={
                    'text': 'GTE',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'y': 0.9,
                    'x': 0.5,
                },
            )
        

        return [fig, fig_lte, fig_gte]

    def gen_max_gte_fig(self):
        fig = ply_go.Figure()
        # fig_eu = ply_go.Figure()
        fig.add_trace(
            ply_go.Line(
                x = self.gte_domain,
                y = self.gte_euler,
                # type='line', 
                name='Euler Method'
            )
        )
        # fig_ieu = ply_go.Figure()
        fig.add_trace(
            ply_go.Line(
                x = self.gte_domain,
                y = self.gte_im_euler,
                # type='line', 
                name='Improved Euler Method'
            )
        )
        # fig_rg = ply_go.Figure()
        fig.add_trace(
            ply_go.Line(
                x = self.gte_domain,
                y = self.gte_rg_kt,
                # type='line', 
                name='Range-Kerutta Method'
            )
        )
        fig.update_layout(
                title={
                    'text': 'Maximum GTE',
                    'xanchor': 'center',
                    'yanchor': 'top',
                    'y': 0.9,
                    'x': 0.5,
                },
                # plot_bgcolor={'white'}

            )
        return fig

ms_plot = Master_plotter()

def decode_png(src):
    image_filename = src
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    return 'data:image/png;base64,{}'.format(encoded_image.decode())



app.layout = html.Div([html.H1('DE Practicum',
                               style={
                                      'textAlign': 'center',
                                      "background": "yellow"}),
                        # dcc.Dropdown(
                        #     id='crossfilter-xaxis-column',
                        #     options=[{'label': i, 'value': i} for i in ['Solution', '?Convergence?', 'Approximation error']],
                        #     value='Solution'
                        # ),
                        
                        html.Div([
                            html.Br(),
                            html.Img(src=decode_png('img/DEpracticum.png'), style={'height':'47px', 'margin-top':'10px'}),                        
                            html.Br(),
                            html.Img(src=decode_png('img/Solpracticum.png'), style={'height':'27px', 'margin-top':'10px'}),                        
                            html.Br(),
                            html.Img(src=decode_png('img/Constpracticum.png'), style={'height':'47px', 'margin-top':'10px'}),                        
                        ], style={'textAlign':'center', 'background':'white'}),

                        html.Div([
                            html.Br(),
                            html.Div([
                                "x0: ",
                                dcc.Input(id='x0', value='2', type='text')
                                ], 
                                # id='x0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Div([
                                "X: ",
                                dcc.Input(id='X', value='12', type='text')
                                ], 
                                # id='X', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Div([
                                "y0: ",
                                dcc.Input(id='y0', value='0', type='text')
                                ], 
                                # id='y0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Div([
                                "N: ",
                                dcc.Input(id='N', value='10', type='text')
                                ], 
                                # id='y0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Br(),
                            html.Div([
                                # "N: ",
                                # dcc.Input(id='N', value='10', type='text')
                                html.Button(id='submit-button-state', n_clicks=0, children='Submit'),
                                ], 
                                # id='y0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            
                        ], 
                        id='initial-values', 
                        style={'background':'white', 'textAlign': 'center'}
                        ),
                        
                        html.Div(
                        dcc.Graph(
                           id='graph-solution',
                           figure={
                               'data': [
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.exact_solution, 'type': 'line', 'name': 'Exact'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.rg_kt_solution, 'type': 'line', 'name': 'Range-Kerutta Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.im_euler_solution, 'type': 'line', 'name': 'Improved Euler Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.euler_solution, 'type': 'line', 'name': 'Euler Method'},
                               ],
                               'layout': {
                                   'title': 'Solutions',
                                     }
                                 }
                            ),
                        ),
                        html.Div([
                        dcc.Graph(
                           id='graph-lte',
                           figure={
                               'data': [
                                #    {'x': exact_domain, 'y': exact_lte, 'type': 'line', 'name': 'Exact'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.euler_lte, 'type': 'line', 'name': 'Euler Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.im_euler_lte, 'type': 'line', 'name': 'Improved Euler Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.rg_kt_lte, 'type': 'line', 'name': 'Range-Kerutta Method'}
                               ],
                               'layout': {
                                   'title': 'LTE', 
                                     }
                                 }
                            )], style={'width':'50%','display': 'inline-block'}
                        ),
                        html.Div([
                        dcc.Graph(
                           id='graph-gte',
                           figure={
                               'data': [
                                #    {'x': exact_domain, 'y': exact_lte, 'type': 'line', 'name': 'Exact'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.euler_gte, 'type': 'line', 'name': 'Euler Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.im_euler_gte, 'type': 'line', 'name': 'Improved Euler Method'},
                                   {'x': ms_plot.exact_domain, 'y': ms_plot.rg_kt_gte, 'type': 'line', 'name': 'Range-Kerutta Method'}
                               ],
                               'layout': {
                                   'title': 'GTE', 
                                     }
                                 }
                            )], style={'width':'50%','display': 'inline-block'}
                        ),

                        html.Div([
                            html.Br(),
                            html.Div([
                                "n0: ",
                                dcc.Input(id='gte-n0', value='10', type='text')
                                ], 
                                # id='x0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Div([
                                "N: ",
                                dcc.Input(id='gte-n', value='100', type='text')
                                ], 
                                # id='X', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            html.Br(),
                            html.Div([
                                # "N: ",
                                # dcc.Input(id='N', value='10', type='text')
                                html.Button(id='submit-button-gte', n_clicks=0, children='Submit'),
                                ], 
                                # id='y0', 
                                style={'display': 'inline-block', 'margin':'10px'}
                            ),
                            
                        ], 
                        id='gte-bounds', 
                        style={'background':'white', 'textAlign': 'center'}
                        ),

                        html.Div([
                        # html.Div(),
                        dcc.Graph(
                            id='graph-max-gte',
                           figure={
                               'data': [
                                #    {'x': exact_domain, 'y': exact_lte, 'type': 'line', 'name': 'Exact'},
                                   {'x': ms_plot.gte_domain, 'y': ms_plot.gte_euler, 'type': 'line', 'name': 'Euler Method'},
                                   {'x': ms_plot.gte_domain, 'y': ms_plot.gte_im_euler, 'type': 'line', 'name': 'Improved Euler Method'},
                                   {'x': ms_plot.gte_domain, 'y': ms_plot.gte_rg_kt, 'type': 'line', 'name': 'Range-Kerutta Method'}
                               ],
                               'layout': {
                                   'title': 'Maximum GTE', 
                                     }
                                 }
                            )], #style={'width':'50%','display': 'inline-block'}
                        ),

                            ], style={
                                "background": "#000080"}
                        )

#Solution
@app.callback(
    Output('graph-solution', 'figure'),
    Output('graph-lte', 'figure'),
    Output('graph-gte', 'figure'),
    # Output('graph-max-gte', 'figure'),
    Input('submit-button-state', 'n_clicks'),
    State('x0', 'value'),
    State('X', 'value'),
    State('y0', 'value'),
    State('N', 'value')
)# th_sol = threading.Thread(target=meth.calc_and_save_all)
# th_sol.start()

# th_sol = threading.Thread(target=meth.calc_and_save_all)
# th_sol.start()

# meth.calc_and_save_all()
# meth.calc_and_save_all()
def update_solution(n_clicks, x0, x, y0, n):
    # if float(x0)==0:
    #     x0 = 1e-10
    # if float(x)==0:
    #     x = 1e-10
    iv = DE.Initial_value(float(x0), float(x), float(y0))
    
    # if(iv != ms_plot.de.get_initial_value()):
    #     ms_plot.change_gte_bounds(ms_plot.max_gte.get_n0(), ms_plot.max_gte.get_n())
    #     ms_plot.load_max_gte()

    ms_plot.change_solution_iv(iv, int(n))
    ms_plot.load_solution()
    # update_gte_max(n_clicks, 10, 100)
    # m_gte = ms_plot.gen_max_gte_fig()
    
    out = ms_plot.gen_solution_fig()
    return out
    # return [out, m_gte]

# GTE-max
@app.callback(
    Output('graph-max-gte', 'figure'),
    Input('submit-button-gte', 'n_clicks'),
    State('gte-n0', 'value'),
    State('gte-n', 'value')
)
def update_gte_max(n_clicks, n0, n):
    # print(input1, input2)
    # if isinstance(input1, int) and isinstance(input2, int):
    ms_plot.change_gte_bounds(int(n0), int(n))
    ms_plot.load_max_gte()
    # print(ms_plot.max_gte.get_n())

    return ms_plot.gen_max_gte_fig()


if __name__ == '__main__':
    # Fuck you marat.
    app.run_server(debug=True)