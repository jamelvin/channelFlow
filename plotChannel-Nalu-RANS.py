import os
import sys

sys.path.insert(0,'/h1/jmelvin/.local/lib/python2.7/site-packages')

import netCDF4 as nc
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm

def NALUprocessDS(bname,numPart,var,log,visc,ts,save,plotDNS,dnsDataFile):
    if (plotDNS):
        #get DNS data
        DNSdata = pd.read_csv(dnsDataFile, delim_whitespace=True)

    Retau = 1.0/visc #assumes a channel height of 1 and a utau of 1.0
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    for j in range(0,numPart):
        if (numPart > 1):
            fn = bname + "." + str(numPart) + "." + str(j).zfill(2)
            f = nc.Dataset(fn,"r")

            x = f['coordx']
            y = f['coordy']
            z = f['coordz']

            for i in range(0,f.dimensions["num_nod_var"].size):
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_x"):
                #    avgUx = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_y"):
                #    avgUy = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_z"):
                #    avgUz = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_x"):
                    ux = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_y"):
                    uy = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_z"):
                    uz = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "k_ratio"):
                #    alpha = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "turbulent_ke"):
                    tke = f["vals_nod_var%i" % (i+1)][ts]

            if (j == 0):
                print f["time_whole"][ts]
            #    rawdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'avgUx':avgUx[:],'avgUy':avgUy[:],'avgUz':avgUz[:],'alpha':alpha[:],'tke':tke[:]})
                rawdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'tke':tke[:]})
            else:
                #tmpdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'avgUx':avgUx[:],'avgUy':avgUy[:],'avgUz':avgUz[:],'alpha':alpha[:],'tke':tke[:]})
                tmpdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'tke':tke[:]})
                rawdata = pd.concat([rawdata,tmpdata])

        else:
            fn = bname
            f = nc.Dataset(fn,"r")

            x = f['coordx']
            y = f['coordy']
            z = f['coordz']

            print f["time_whole"][ts]

            for i in range(0,f.dimensions["num_nod_var"].size):
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_x"):
                #    avgUx = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_y"):
                #    avgUy = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "average_velocity_z"):
                #    avgUz = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_x"):
                    ux = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_y"):
                    uy = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "velocity_z"):
                    uz = f["vals_nod_var%i" % (i+1)][ts]
                #if (''.join(f["name_nod_var"][i].data) == "k_ratio"):
                #    alpha = f["vals_nod_var%i" % (i+1)][ts]
                if (''.join(f["name_nod_var"][i].data) == "turbulent_ke"):
                    tke = f["vals_nod_var%i" % (i+1)][ts]

            #rawdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'avgUx':avgUx[:],'avgUy':avgUy[:],'avgUz':avgUz[:],'alpha':alpha[:],'tke':tke[:]})
            rawdata = pd.DataFrame({'x':x[:],'y':y[:],'z':z[:],'ux':ux[:],'uy':uy[:],'uz':uz[:],'tke':tke[:]})

    rawdata = rawdata.round(10)
    yCoords = rawdata.y.unique()
    #rawdata["fluctUx"] = rawdata["ux"] - rawdata["avgUx"]
    #rawdata["fluctUy"] = rawdata["uy"] - rawdata["avgUy"]
    #rawdata["fluctUz"] = rawdata["uz"] - rawdata["avgUz"]
    #rawdata["varUx"] = rawdata["fluctUx"]*rawdata["fluctUx"]
    #rawdata["varUy"] = rawdata["fluctUy"]*rawdata["fluctUy"]
    #rawdata["varUz"] = rawdata["fluctUz"]*rawdata["fluctUz"]

    #print rawdata

    #planarAvg = np.zeros((len(yCoords),12))
    planarAvg = np.zeros((len(yCoords),5))
    index = 0
    for yc in yCoords:
      sliceY = rawdata.loc[(rawdata['y'] == yc)]
      avgUx = sliceY.ux.sum()/len(sliceY)
      avgUy = sliceY.uy.sum()/len(sliceY)
      avgUz = sliceY.uz.sum()/len(sliceY)
      #avgAvgUx = sliceY.avgUx.sum()/len(sliceY)
      #avgAvgUy = sliceY.avgUy.sum()/len(sliceY)
      #avgAvgUz = sliceY.avgUz.sum()/len(sliceY)
      #avgAlpha = sliceY.alpha.sum()/len(sliceY)
      avgTke = sliceY.tke.sum()/len(sliceY)
      #uuVar = sliceY.varUx.sum()/len(sliceY)
      #vvVar = sliceY.varUy.sum()/len(sliceY)
      #wwVar = sliceY.varUz.sum()/len(sliceY)
      #planarAvg[index] = np.array([yc/visc,avgUx,avgUy,avgUz,avgAvgUx,avgAvgUy,avgAvgUz,avgAlpha,avgTke,uuVar,vvVar,wwVar])
      planarAvg[index] = np.array([yc/visc,avgUx,avgUy,avgUz,avgTke])
      index = index + 1

    #pltFrame = pd.DataFrame(planarAvg,columns=['y','ux','uy','uz','avgUx','avgUy','avgUz','alpha','tke','uu','vv','ww'])
    pltFrame = pd.DataFrame(planarAvg,columns=['y','ux','uy','uz','tke'])

    pltFrame = pltFrame.loc[(pltFrame['y'] <= 1.0/visc)]
    pltFrame = pltFrame.sort_values(by=['y'])

    ax.plot(pltFrame.y,pltFrame[var])
    ax.set_xlim(1.0,np.max(pltFrame.y))

    if (plotDNS):
        ax.plot(DNSdata["y^+"],DNSdata["U"])

    if (log):
        ax.set_xscale('log')
    if (save):
        plt.savefig('/workspace/jmelvin/Research/channelFlow/alphaMovies/nalu_' + str(ts).zfill(4))
        plt.close(fig)
    else:
        plt.show()

    return pltFrame


######## MAIN #######
#### NALUproccesDS()
#### NALUprocessDS(exoBasename,numExoParts,variableToPrint,loglogPlot?,viscosity,tsFromExoDBToPlot,SavePlotToDisk?,ComparePlotToDNS?,DNSdataFilePath)
####
#### exoBasename = path to basename of exodus files, i.e 'Channel.e'
#### numExoParts = number of partitions for exodus DB
#### variableToPrint = which variable to print, options are "ux", "uy", "uz", "tke"
#### loglogPlot? = True/False   Do you want to change the axes to a log log plot?
#### viscosity = Enter the value of the viscosity used in Nalu, this is used for normalization
#### tsFromExoDBToPlot = which ts index do you want to plot, -1 would be the last timestep,
####                     0 the first, other indices as they fall in the exo DB
#### savePlotToDisk? = Do you want to save the plot to a file instead of showing it. Right
####                   now this is hardcoded to a path on my computer
#### ComparePlotToDNS? = Would you like to plot the DNS data as a comparison, only works with
####                     "ux" right now...
#### DNSdataFilePath = If you are comparing to DNS you need to pass it the file path to the
####                   DNS data

df = NALUprocessDS('/workspace/jmelvin/meshes/TAMS_KE-Channel-BUGFIX.e',32,"ux",True,0.001,-1,False,True,"/workspace/jmelvin/Research/channelFlow/Re1000.txt")
