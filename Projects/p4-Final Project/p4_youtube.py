import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import data

def sort(logic):

    if logic[0].lower()=='bar':
        if logic[1].lower()=='totalsubs':
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)

            search_list=[(data.get_channel_info(yt)[0],data.get_channel_info(yt)[1]) for yt in tubers]
            subs=[(data.get_current_subcribers(tup[0]),tup[1]) for tup in search_list]
            traces = []
            for items in subs:
                trace= go.Bar(
                    x=['Subscriber Total'],
                    y=[items[0][0]],
                    name=items[1][1]
                )
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalviews':
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)

            search_list=[(data.get_channel_info(yt)[0],data.get_channel_info(yt)[1]) for yt in tubers]
            subs=[(data.get_current_subcribers(tup[0]),tup[1]) for tup in search_list]
            traces = []
            for items in subs:
                trace= go.Bar(
                    x=['Views Total'],
                    y=[items[0][1]],
                    name=items[1][1]
                )
                
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Hello Dash'),

                html.Div(children='''
                    Dash: A web application framework for Python.
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout





app_bar = dash.Dash()
app_scatter = dash.Dash()
app_line = dash.Dash()


   


if __name__ == '__main__':
    print('Welcome to the Youtube Analyzer Application!\n')
    ipt=input('Please enter a command or type "help" for more information: ')
    logic=ipt.split()
    if logic[0]=='bar':
        lay=sort(logic)
        app_bar.run_server()