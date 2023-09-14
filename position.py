import sys
import serial
import numpy as np
from matplotlib import pyplot as plt
from time import sleep
from IPython.display import display, clear_output
from mpl_toolkits.mplot3d import Axes3D

TEST_MODE = True
anchorNum = 4
x_axis = 5
y_axis = 5
z_axis = 5
anchorPos = [   [0,         0,      0],
                [x_axis,    0,      0],
                [0,         y_axis, 0],
                [0,         0,      z_axis] ]

def position_sphere(distances):
    # p1=np.array(distances[0][:3])
    # p2=np.array(distances[1][:3])
    # p3=np.array(distances[2][:3])       
    # p4=np.array(distances[3][:3])  
    # r1=distances[0][-1]
    # r2=distances[1][-1]
    # r3=distances[2][-1]
    # r4=distances[3][-1]
    # ans=[0.0, 0.0, 0.0]
    # d_x = p1[0] - p4[0]
    # ans[0] = (d_x**2 - r1**2 + r4**2) / (2*d_x)
    # d_y = p2[1] - p4[1]
    # ans[1] = (d_y**2 - r2**2 + r4**2) / (2*d_y)
    # d_z = p3[2] - p4[2]
    # ans[2] = (d_z**2 - r3**2 + r4**2) / (2*d_z)
    if (TEST_MODE):
        p = []
        for i in range (anchorNum):
            p.append(np.array(distances[i][:3]))
    else:
        p = anchorPos
    r = []
    d = []
    ans = []
    for i in range (anchorNum):
        r.append(distances[i][-1])
    for i in range (anchorNum - 1):
        d.append(p[i + 1][i] - p[0][i])
        ans.append((d[i]**2 - r[i + 1]**2 + r[0]**2) / (2*d[i]))
    return ans

def position(disances):
    if (TEST_MODE):
        p = []
        for i in range (anchorNum):
            p.append(np.array(distances[i][:3]))
    else:
        p = anchorPos
    r = []
    k = []
    A = []
    b = []
    for i in range (anchorNum):
        r.append(distances[i][-1])
        k.append(p[i][0]**2 + p[i][1]**2 + p[i][2]**2)
    for i in range (anchorNum - 1):
        A.append([p[i + 1][0] - p[0][0], p[i + 1][1] - p[0][1], p[i + 1][2] - p[0][0]])
    det=np.linalg.det(A)
    det=1.0/det
    A=np.array(A)
    A_inv=A*det
    for i in range (anchorNum - 1):
        b.append(r[0]**2-r[i + 1]**2+k[i + 1]-k[0])
    posn2=np.dot(A_inv, b)
    ans=posn2/2.0
    rmse=0
    for i in range (anchorNum):
        dc = np.sqrt((p[i][0]-ans[0])**2 + (p[i][1]-ans[1])**2 + (p[i][2]-ans[2])**2)
        rmse += (r[i] - dc)**2
    rmse = np.sqrt(rmse/float(anchorNum))
    return ans, rmse


if __name__ == "__main__":
    # read from file
    if (TEST_MODE):
        # Retrive file name for input data
        if(len(sys.argv) == 1):
            print("Please enter data file name.")
            exit()
        
        filename = sys.argv[1]

        # Read data
        lines = [line.rstrip('\n') for line in open(filename)]
        distances = []
        for line in range(0, len(lines)):
            distances.append(list(map(float, lines[line].split(' '))))

        # Print out the data
        print("The input four points and distances, in the format of [x, y, z, d], are:")
        for p in range(0, len(distances)):
            print(distances[p])
        location_sphere = position_sphere(distances)
        print("The location (sphere) of the point is: " + str(location_sphere))
        location = position(distances)
        print("The location of the point is: " + str(location))
    #read from serial
    else:
        #Open port with baud rate
        ser = serial.Serial ("/dev/ttyUSB0", 9600)    
        #
        plt.ion()
        fig = plt.figure(figsize=(10, 10))
        ax = fig.add_subplot(111, projection='3d')
        #
        axes = [2, 6, 2]
        data = np.ones(axes)
        ax.voxels(data, alpha=0.1, edgecolors='black')
        #
        while True:
            received_data = ser.read()              #read serial port
            sleep(0.1)
            data_left = ser.inWaiting()             #check for remaining byte
            received_data += ser.read(data_left)
            readData_1=received_data[:10]
            readData_2=received_data[10:20]
            readData_3=received_data[20:30]
            readData_4=received_data[30:40]
            temps_1=[]
            temps_2=[]
            temps_3=[]
            temps_4=[]

            for i in range(0, 10):
                temps_1.append(float(readData_1[i]))
                temps_2.append(float(readData_2[i]))
                temps_3.append(float(readData_3[i]))
                temps_4.append(float(readData_4[i]))
            temps=[]
            temps.append(temps_1)
            temps.append(temps_2)
            temps.append(temps_3)
            temps.append(temps_4)
            distances = temps
            for p in range(0, len(distances)):
                tmp = distances[p][4] * 256 + distances[p][5]
                if (distances[p][-1] == 1): tmp = -tmp
                distances[p].pop()
                distances[p].append((distances[p][2] * 256 + distances[p][3]) / 100)
                if (distances[p][-1] > 1): distances[p][-1] -= 0.6
                else: distances[p][-1] -= 0.2
                distances[p].pop(0)
                distances[p].pop(0)
                distances[p].pop(0)
                distances[p].pop(0)
                distances[p].pop(0)
                distances[p].pop(0)
            for p in range(0, len(distances)):
                print(distances[p])
            # Call the function and compute the location 
            location = position(distances)
            print("The location of the point is: " + str(location))
            #
            temporaryPoints = ax.scatter(location[0], location[1], location[2])
            display(fig)
            plt.pause(0.2)
            temporaryPoints.remove()

#1: 0 0 0
#2: 2 2.5 1
#3: 1 5 1

#4: 2.8 5 1
#5 0 7 1
#6 1.2 7 1
#7 2.5 7 1
#8 3.5 -2.7 1.5