import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.graph_objs as go
import data
import sqlite3
db_name='YoutuberDB.db'
conn = sqlite3.connect(db_name)
cur=conn.cursor()

def sort(logic):

    if logic[0].lower()=='bar':
        if logic[1].lower()=='totalsubs':
            dat=data.get_data('subs')
            print(dat)
            traces = []
            for item in dat:
                trace= go.Bar(
                    x=['Subscriber Total'],
                    y=[item[1]],
                    name=items[0]
                )
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Subscribers: Bar graph comparison of Youtuber Total Subscribers
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalviews':
            dat=data.get_data('views')
            print(dat)
            traces = []
            for item in dat:
                trace= go.Bar(
                    x=['Subscriber Total'],
                    y=[item[1]],
                    name=items[0]
                )
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Subscribers: Bar graph comparison of Youtuber Total Subscribers
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalview30':
            dat=data.get_data('ViewsLastThirty')
            print(dat)
            traces = []
            for item in dat:
                trace= go.Bar(
                    x=['Subscriber Total'],
                    y=[item[1]],
                    name=items[0]
                )
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Subscribers: Bar graph comparison of Youtuber Total Subscribers
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalsubs30':
            dat=data.get_data('SubsLastThirty')
            print(dat)
            traces = []
            for item in dat:
                trace= go.Bar(
                    x=['Subscriber Total'],
                    y=[item[1]],
                    name=items[0]
                )
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Subscribers: Bar graph comparison of Youtuber Total Subscribers
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout

    if logic[0].lower()=='box':
        if logic[1].lower()=='twitter':
            d=data.get_data('twitter')
            traces = []
            for items in d:
                data_points=[]
                for points in items[0]:
                    data_points.append(points[1])
                trace= go.Box(x=data_points, name=items[1])
                traces.append(trace)
            fig = go.Figure(data=traces)
            app_box.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Twitter: Bar graph comparison of Twitter Senitment Analysis
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_box.layout
    if logic[0].lower()=='line':
        


            






app_bar = dash.Dash()
app_box = dash.Dash()
app_line = dash.Dash()


   


if __name__ == '__main__':
    print('Welcome to the Youtube Analyzer Application!\n')
    ipt=input('Please enter a command or type "help" for more information: ')
    logic=ipt.split()
    if logic[0]=='bar':
        lay=sort(logic)
        app_bar.run_server()
    if logic[0]=='box':
        lay=sort(logic)
        app_box.run_server()