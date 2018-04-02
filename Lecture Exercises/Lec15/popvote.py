import plotly.plotly as py
import plotly.graph_objs as go
import csv

with open('PopVote.csv', 'r') as f:
	reader = csv.reader(f)
	nl=list(reader)
votes=[]
for row in nl[11:23]:
	votes.append((row[0],row[1],row[2]))
for row in nl[26:]:
	votes.append((row[0],row[1],row[2]))

states=[]
for tups in votes:
	states.append(tups[0])
dems=[]
for d_votes in votes:
	dems.append(d_votes[1])

rep=[]

for r_votes in votes:
	rep.append(r_votes[2])


red=[]
for items in range(len(rep)):
	red.append('rgba(222,45,38,0.8)')


trace1 = go.Bar(
    x=states,
    y=dems,
    name='Democrats'
    
)
trace2 = go.Bar(
    x=states,
    y=rep,
    name='Republicans',
    marker=dict(
        color=red
        ),
)

data = [trace1, trace2]
layout = go.Layout(
	title="Poular Votes per State",
    barmode='group',
    height=600,
    width=1000,
)

fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='grouped-bar')

