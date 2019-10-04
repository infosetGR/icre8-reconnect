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
{'points': [{'curveNumber': 0, 'pointNumber': 788, 'pointIndex': 788, 'lon': 34.07419003289721, 'lat': 34.97587069859949, 'text': 788, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 789, 'pointIndex': 789, 'lon': 34.07523469246115, 'lat': 34.97567136611131, 'text': 789, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 790, 'pointIndex': 790, 'lon': 34.075667394071075, 'lat': 34.97593001113786, 'text': 790, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 804, 'pointIndex': 804, 'lon': 34.07415242041512, 'lat': 34.977102941783556, 'text': 804, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 805, 'pointIndex': 805, 'lon': 34.07520231859225, 'lat': 34.976821803020535, 'text': 805, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 806, 'pointIndex': 806, 'lon': 34.076538894565964, 'lat': 34.97600823957727, 'text': 806, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 807, 'pointIndex': 807, 'lon': 34.07730209500326, 'lat': 34.976259489745004, 'text': 807, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 808, 'pointIndex': 808, 'lon': 34.07835197323687, 'lat': 34.97597831523271, 'text': 808, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 809, 'pointIndex': 809, 'lon': 34.07940184482233, 'lat': 34.975697128804214, 'text': 809, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 819, 'pointIndex': 819, 'lon': 34.07339566912943, 'lat': 34.97824578692803, 'text': 819, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 820, 'pointIndex': 820, 'lon': 34.07444558444545, 'lat': 34.97796465623166, 'text': 820, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 821, 'pointIndex': 821, 'lon': 34.07549549311362, 'lat': 34.97768351361849, 'text': 821, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 822, 'pointIndex': 822, 'lon': 34.07654539513376, 'lat': 34.97740235908866, 'text': 822, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 823, 'pointIndex': 823, 'lon': 34.077595290505684, 'lat': 34.97712119264227, 'text': 823, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 824, 'pointIndex': 824, 'lon': 34.078645179229284, 'lat': 34.976840014279446, 'text': 824, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 825, 'pointIndex': 825, 'lon': 34.07969506130438, 'lat': 34.976558824000314, 'text': 825, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 833, 'pointIndex': 833, 'lon': 34.07368883277002, 'lat': 34.97910750255038, 'text': 833, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 834, 'pointIndex': 834, 'lon': 34.074738758577716, 'lat': 34.97882636800386, 'text': 834, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 835, 'pointIndex': 835, 'lon': 34.07578867773721, 'lat': 34.9785452215404, 'text': 835, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 836, 'pointIndex': 836, 'lon': 34.076838590248315, 'lat': 34.978264063160154, 'text': 836, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 837, 'pointIndex': 837, 'lon': 34.077888496110866, 'lat': 34.97798289286326, 'text': 837, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 838, 'pointIndex': 838, 'lon': 34.07892779069336, 'lat': 34.97767054772854, 'text': 838, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 839, 'pointIndex': 839, 'lon': 34.07990566248962, 'lat': 34.97717771752574, 'text': 839, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 840, 'pointIndex': 840, 'lon': 34.08038587378715, 'lat': 34.97684804459111, 'text': 840, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 844, 'pointIndex': 844, 'lon': 34.07398200651269, 'lat': 34.97996921549698, 'text': 844, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 845, 'pointIndex': 845, 'lon': 34.07503194281235, 'lat': 34.97968807710016, 'text': 845, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 846, 'pointIndex': 846, 'lon': 34.076081872463455, 'lat': 34.9794069267863, 'text': 846, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 847, 'pointIndex': 847, 'lon': 34.07713179546582, 'lat': 34.979125764555505, 'text': 847, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 848, 'pointIndex': 848, 'lon': 34.07818171181926, 'lat': 34.97884459040797, 'text': 848, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 849, 'pointIndex': 849, 'lon': 34.07910584856173, 'lat': 34.97859709016551, 'text': 849, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 854, 'pointIndex': 854, 'lon': 34.07427519035788, 'lat': 34.98083092576783, 'text': 854, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 855, 'pointIndex': 855, 'lon': 34.075325137149775, 'lat': 34.98054978352057, 'text': 855, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 856, 'pointIndex': 856, 'lon': 34.07637507729276, 'lat': 34.98026862935617, 'text': 856, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 857, 'pointIndex': 857, 'lon': 34.077425010786676, 'lat': 34.97998746327471, 'text': 857, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 858, 'pointIndex': 858, 'lon': 34.07847493763131, 'lat': 34.979706285276364, 'text': 858, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 859, 'pointIndex': 859, 'lon': 34.07956019910846, 'lat': 34.979267897139806, 'text': 859, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 860, 'pointIndex': 860, 'lon': 34.08030455398767, 'lat': 34.97961588434617, 'text': 860, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 865, 'pointIndex': 865, 'lon': 34.07351842037245, 'lat': 34.981973767543316, 'text': 865, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 866, 'pointIndex': 866, 'lon': 34.074568384306005, 'lat': 34.98169263336287, 'text': 866, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 867, 'pointIndex': 867, 'lon': 34.07561834159043, 'lat': 34.98141148726505, 'text': 867, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 868, 'pointIndex': 868, 'lon': 34.07666829222559, 'lat': 34.981130329249964, 'text': 868, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 869, 'pointIndex': 869, 'lon': 34.07771823621131, 'lat': 34.98084915931772, 'text': 869, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 870, 'pointIndex': 870, 'lon': 34.078768173547424, 'lat': 34.98056797746846, 'text': 870, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 871, 'pointIndex': 871, 'lon': 34.07981810423381, 'lat': 34.98028678370227, 'text': 871, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 878, 'pointIndex': 878, 'lon': 34.074861588357514, 'lat': 34.982554338282085, 'text': 878, 'hovertext': '50-100', 'marker.color': '#004d80'}, {'curveNumber': 0, 'pointNumber': 879, 'pointIndex': 879, 'lon': 34.075911556134734, 'lat': 34.98227318833359, 'text': 879, 'hovertext': '10-50', 'marker.color': '#62acde'}, {'curveNumber': 0, 'pointNumber': 880, 'pointIndex': 880, 'lon': 34.07696151726235, 'lat': 34.981992026467694, 'text': 880, 'hovertext': '1-10', 'marker.color': '#97ccf0'}, {'curveNumber': 0, 'pointNumber': 881, 'pointIndex': 881, 'lon': 34.07801147174017, 'lat': 34.98171085268453, 'text': 881, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 882, 'pointIndex': 882, 'lon': 34.07906141956803, 'lat': 34.981429666984226, 'text': 882, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 883, 'pointIndex': 883, 'lon': 34.08011136074582, 'lat': 34.98114846936684, 'text': 883, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 892, 'pointIndex': 892, 'lon': 34.07830471737368, 'lat': 34.98257254337512, 'text': 892, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 893, 'pointIndex': 893, 'lon': 34.07935467569357, 'lat': 34.98229135382361, 'text': 893, 'hovertext': '0', 'marker.color': '#FFFFFF'}, {'curveNumber': 0, 'pointNumber': 894, 'pointIndex': 894, 'lon': 34.08037618213913, 'lat': 34.98192657812997, 'text': 894, 'hovertext': '0', 'marker.color': '#FFFFFF'}], 'range': {'mapbox': [[34.07338762998563, 34.982729492138404], [34.08042574643662, 34.975556209502955]]}}