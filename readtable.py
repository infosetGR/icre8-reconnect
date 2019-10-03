import pandas as pd
import plotly.graph_objs as go
import plotly
## dfs is a list of data frames. Each data frame is a html table
import lxml
from utils import  make_dash_table
#dfs = pd.read_html('https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.DPND&country=ALB,BGR,CYP,GRC#',header=0)
#dfs = pd.read_html('https://databank.worldbank.org/reports.aspx?source=2&series=SP.POP.DPND.OL&country=ALB,BGR,CYP,GRC',header=0)


dfs = pd.read_html('https://databank.worldbank.org/reports.aspx?source=2&series=TM.VAL.FOOD.ZS.UN&country=ALB,BGR,CYP,GRC')

df=dfs[5].transpose()
x=df.set_axis(['Y'], axis=1, inplace=False)
y = dfs[19].transpose()
y.columns = y.iloc[0]
y=y.drop(y.index[0])

tab= pd.concat([x, y],axis=1)
print(tab)


trace1 = go.Scatter(y=tab.Albania, x=tab.Y, mode='lines', line_color='red')
trace2 = go.Scatter(y=tab.Bulgaria, x=tab.Y, mode='lines', line_color='green')
trace3 = go.Scatter(y=tab.Greece, x=tab.Y, mode='lines', line_color='blue')
trace4 = go.Scatter(y=tab.Cyprus, x=tab.Y, mode='lines', line_color='deepskyblue')
data = [trace1,trace2,trace3,trace4]
layout = go.Layout(title='Simple Line Chart',
                   xaxis={'title': 'This is the X Axis'},
                   yaxis=dict(title='This is the Y Asis')
                  )
fig =go.Figure(data=data, layout=layout)
fig.show()

#print(make_dash_table(df))
#x_values = df[0]

'''def plot_graph(inp,f,v):
    col = inp
    da = df
    print(f)
    for ctr in range(len(f)):
        da = da[da[f]<=v[1]]
        da = da[da[f]>=v[0]]
    c = da[inp].dropna()
    print(c.name)
    #print(c.describe())
    #plt.clf();
    plt.figure(figsize=(20,10))
    plt.subplot(2,2,1);
    plt.text(0.03,0.2,str(c.describe()), fontsize=13)
    plt.subplot(2,2,2);
    plt.plot(df['Series Name'], df[c.name]);
    plt.title(str("Graph of "+c.name));
    plt.subplot(2,2,3);
    sns.distplot(c);
    plt.title("Histogram");
    plt.subplot(2,2,4)
    sns.boxplot(c);
    plt.title("Box Plot")'''
    #plt.show()
#plotly.
#y_values = [random.randrange(20,25) for x in range(50)] #50 random values between 20

'''for i in range(len(dfs)):
    print('i=', i)
    df = dfs[i]
    print(df)'''


## Getting the maximum Opening Amazon Stock Price
#i = df.iloc[:, 1].idxmax()
#df.iloc[i]
