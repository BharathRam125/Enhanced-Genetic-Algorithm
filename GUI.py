#map_viz_test module for map and path visualization
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import matplotlib as mpl
mpl.rc('image', cmap='gray')

#function for gui to be called from SinglePathWithAPF
def gui(PATH1,lab):
    #setting colour map to gray
    mpl.rc('image', cmap='gray')

    #getting input matrix through map.txt file
    matrix = []
    with open('map.txt') as f:
        rows = f.readlines()
        for row in rows:
            matrix.append(list(map(int, row.split(" "))))
    x1=[] # list of x co-ordinates
    y1=[] # list of y co-ordinates

    #loading path into x, y co-ordinates
    for i in PATH1:
        x1.append(i[0])
        y1.append(i[1])
    l = len(PATH1) - 1
    ax=plt.gca()
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)
    plt.imshow(matrix) #shows map
    plt.plot(y1[0], x1[0],c='y',marker='*',label="Start") #plots start
    plt.plot(y1[l], x1[l], c='m',marker='s',label="Dest") #plots dest
    plt.plot(y1, x1, label=lab,linewidth=0.7) #plots path as line
    leg = plt.legend(loc=2,prop={'size': 7})
    plt.show() 

PATH1=[]
