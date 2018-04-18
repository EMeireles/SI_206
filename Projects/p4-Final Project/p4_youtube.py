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
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)

            search_list=[(data.get_channel_info(yt)[0],data.get_channel_info(yt)[1]) for yt in tubers[:-1]]
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
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)

            search_list=[]
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
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Views: Bar graph comparison of Youtuber Total Views.
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalview30':
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)
            subs=[(data.get_social(yt)[0][8],yt) for yt in tubers[:-1]]
            cleaned=[(item[0].split('\n')[0],item[1]) for item in subs]
            traces = []
            for items in cleaned:
                trace= go.Bar(
                    x=['Views Total in the last 30 days'],
                    y=[items[0]],
                    name=items[1]
                )
                
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    View Total in the last 30 days: Bar graph comparison of Youtuber views within the last 30 days.
                '''),

                dcc.Graph(
                    id='example-graph',
                    figure=fig)
                ])
            return app_bar.layout
        if logic[1].lower()=='totalsubs30':
            ipt='a'
            tubers=[]
            while(ipt!='done'):
                ipt=input("Enter Youtuber: ")
                tubers.append(ipt)
            subs=[(data.get_social(yt)[0][7],yt) for yt in tubers[:-1]]
            cleaned=[(item[0].split('\n')[0],item[1]) for item in subs]
            traces = []
            for items in cleaned:
                trace= go.Bar(
                    x=['Subscribers in the last 30 days'],
                    y=[items[0]],
                    name=items[1]
                )
                
                traces.append(trace)
            layout = go.Layout(
                barmode='group'
            )
            fig = go.Figure(data=traces, layout=layout)
            app_bar.layout = html.Div(children=[
                html.H1(children='Youtube Analyzer'),

                html.Div(children='''
                    Subscribers in the last 30 days: Bar graph comparison of Youtuber Subscribers within the last 30 days.
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