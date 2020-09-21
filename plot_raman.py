

#Hello!

#This code is very simple to operate.

#Just call it in the terminal as:
#python plot_raman.py filename.txt

#Make sure there are no spaces in your filenames!




import pdb
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import argparse
import pandas as pd
matplotlib.rcParams.update({'font.size': 8})



def main(p):


    with open(p,'r') as f:
        data = f.read().splitlines()

    N = len(data)
    Y = []#This will contain the y values as a list of lists.
    x = np.array(data[0].split('\t')[2:]).astype(float)
    Y = np.zeros((N-1,len(x)))
    for i in range(N-1):
        Y[i]=np.array(data[i+1].split('\t')[2:]).astype(float)



    for i in range(len(Y)):
        plt.plot(x,Y[i],alpha=0.1,color='black')

    plt.plot(x,np.nanmean(Y,axis=0),color='red',linewidth=2.5)
    plt.xlabel('Raman shift (cm$^{-1}$)')
    plt.ylabel('Intensity (counts)')
    # plt.show()
    plt.savefig(p.split('.')[0]+'.png',dpi=400)

    out_matrix = np.vstack((x,Y.astype(int)))
    np.savetxt(p.split('.')[0]+'.csv',out_matrix, delimiter=",")

    print "Complete. %s and %s were written."%(p.split('.')[0]+'.png',p.split('.')[0]+'.csv')





#This just parses the command line input.
parser = argparse.ArgumentParser()
parser.add_argument('filename', metavar='p', type=str)
main(parser.parse_args().filename)
