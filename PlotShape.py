import numpy as np
import pandas as pd
import shapefile as shp
import matplotlib.pyplot as plt
import seaborn as sns
import LineBuilder

sns.set(style='whitegrid', palette='pastel', color_codes=True)
sns.mpl.rc('figure', figsize=(10, 6))

shp_path = '.\spatial-vector-lidar\Cyprus_mpa\Cyprus_mpa.shp'
sf = shp.Reader(shp_path)

'''Cyprus;mpa;.\spatial-vector-lidar\Cyprus_mpa\Cyprus_mpa.shp
Cyprus;Posidonia;.\spatial-vector-lidar\Cyprus_Posidonia\CY_Posidonia_100m.shp
Cyprus;Rocky;.\spatial-vector-lidar\Cyprus_Rocky\CY_Rocky_100m.shp  //read  records[id][0] for rocky
Cyprus;Sandy;.\spatial-vector-lidar\Cyprus_Sandy\CY_Sandy_100m.shp
'''
# print(len(sf.shapes()))
#for i in sf.records():
#   print(i)

def read_shapefile(sf):
    """
    Read a shapefile into a Pandas dataframe with a 'coords'
    column holding the geometry information. This uses the pyshp
    package
    """
    fields = [x[0] for x in sf.fields][1:]
    records = sf.records()
    print(records)
    shps = [s.points for s in sf.shapes()]
    df = pd.DataFrame(columns=fields, data=records)

    df = df.assign(coords=shps)

    return df


def plot_shape(id, s=None):
    """ PLOTS A SINGLE SHAPE """
    plt.figure()
    ax = plt.axes()
    ax.set_aspect('equal')
    shape_ex = sf.shape(id)
    x_lon = np.zeros((len(shape_ex.points), 1))
    y_lat = np.zeros((len(shape_ex.points), 1))
    for ip in range(len(shape_ex.points)):
        x_lon[ip] = shape_ex.points[ip][0]
        y_lat[ip] = shape_ex.points[ip][1]
    plt.plot(x_lon, y_lat)
    x0 = np.mean(x_lon)
    y0 = np.mean(y_lat)
    plt.text(x0, y0, s, fontsize=10)
    # use bbox (bounding box) to set plot limits
    plt.xlim(shape_ex.bbox[0], shape_ex.bbox[2])
    return x0, y0


def plot_map(sf, x_lim=None, y_lim=None, figsize=(11, 9)):
    '''
    Plot map with lim coordinates
    '''

    id = 0

    records = sf.records()

    print(records)
    for shape in sf.shapeRecords():

        x = [i[0] for i in shape.shape.points[:]]
        y = [i[1] for i in shape.shape.points[:]]

        plt.plot(x, y, 'k')

        #print(records[id][1])

        if records[id][1] == '0':
            color='#FFFFFF'
        elif records[id][1] == '1-10':
            color = '#CCE8FF'
        elif records[id][1] == '10-50':
            color = '#3379B2'
        elif records[id][1] == '50-100':
            color = '#002A4C'
        else :
            color = '#FFFFFF'
        plt.fill(x, y, color)

        if (x_lim == None) & (y_lim == None):
            x0 = np.mean(x)
            y0 = np.mean(y)
         #   plt.text(x0, y0, id, fontsize=10)
        id = id + 1

    if (x_lim != None) & (y_lim != None):
        plt.xlim(x_lim)
        plt.ylim(y_lim)




#plt.interactive(true)
plot_map(sf)



plt.show()
#df = read_shapefile(sf)
#df.shape
#df(50)