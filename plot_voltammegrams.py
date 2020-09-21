#This script contains a program that reads xml files that contain CV or DPV
#curves, and does a rudimentary analysis by plotting the curve(s) and determining
# the peak values. These are then written to a csv file for further analysis.
#The first part of the code immediately below is the definition of two functions.
#Below that is a set of instructions on how to operate the input of the script
#correctly, after which the functions are called. So scroll down for the instructions.

#THIS CODE IS DESIGNED TO RUN IN PYTHON 2.7

#Version 2.3 September 21, 2020.


def read_xml(path):
    import xml.etree.ElementTree as ET
    import pdb
    import numpy as np
    import os.path
    import sys

    if os.path.isfile(path) == False:
        print "ERROR: File (%s) does not exist." % path
        sys.exit()

    root = ET.parse(path).getroot()

    curves = root.findall('curves/curve')
    Nc = len(curves)
    if Nc == 0:
        print "ERROR: %s CONTAINS NO CURVES?!" % path
        print "Exiting. Check out this file in your folder,"
        print "remove it and run Boos.py again..."
        print "Boos.py has saved nothing during this run."
        sys.exit()

    type_tag = curves[0]#Change this number to 0 if you want the first curve, or -1 if you want the last.
    for technic in type_tag.findall('technic'):
        filetype=technic.get('id')

    name_str = type_tag.find('name').text+''
    time_str = type_tag.find('points/time').text+''#I HATE POINTERS SO MUCH
    potential_str = type_tag.find('points/potential').text+''
    current_str = type_tag.find('points/i1').text+''
    current2_str = type_tag.find('points/i2').text+''



    time_split = time_str.split(',')
    time_list= [float(x) for x in time_split]
    potential_list= [float(x) for x in potential_str.split(',')]
    n_points=len(potential_list)
    current_split=current_str.split(',')
    current2_split=current2_str.split(',')
    current_list=[]
    for i in range(n_points):
        current_list.append(float(current_split[i])-float(current2_split[i]))
    return(time_list,potential_list,current_list,filetype)


def plot_curve(V,I,labels,type,outfile,textsize=6,unit='uA'):
    import matplotlib.pyplot as plt
    import matplotlib.figure
    import sys
    import csv
    N=len(V)
    if len(I) != N:
        print 'ERROR: V and I should be lists of lists with the same length.'
        sys.exit()
    if len(labels) != N:
        print 'ERROR: V and labels should be lists of lists with the same length.'
        sys.exit()

    if type != 'DPV' and type != 'CV':
        print "ERROR: Type should be either CV or DPV."
        sys.exit()

    if unit not in ['mA','uA','nA']:
        print("ERROR: unit needs to be set to 'mA','uA','nA' (set to %s)"%(unit))

    peak_V = []
    peak_I = []


    w, h = matplotlib.figure.figaspect(0.5)
    fig, ax = plt.subplots(1,1,figsize=(w,h))
    ax=[ax]#This because I reduced the number of subplots by commenting out the
    #second plot below.
    lines=[]
    lw=1.5
    for i in range(N):
        y_label = 'Current ($\mu$A)'
        if unit == 'mA':
            I[i]/=1000.0
            y_label = 'Current (mA)'
        if unit == 'nA':
            I[i]*=1000.0
            y_label = 'Current (nA)'
        void=ax[0].plot(V[i],I[i],label=labels[i])
        colour=void[0].get_color()
        lines.append(void)
        if type == 'DPV':
            # peak_index=I[i].index(min(I[i]))
            peak_index=np.argmin(I[i])
        else:
            # peak_index=I[i].index(max(I[i]))
            peak_index=np.argmax(I[i])
        ax[0].plot(V[i][peak_index],I[i][peak_index],marker='o',color=colour,linewidth=lw)
        peak_V.append(V[i][peak_index])
        peak_I.append(I[i][peak_index])
    xrange = max(V[0]) - min(V[0])
    ax[0].set_xlabel('Potential (V)')
    ax[0].set_ylabel(y_label)
    ax[0].legend(loc='upper left',prop={'size': textsize})
    ax[0].set_xlim([min(V[0])-0.1*xrange,max(V[0])+0.1*xrange])
    x = np.linspace(0,len(peak_I)-1,len(peak_I))


    annot = ax[0].text(0.95,0.05,'',transform=ax[0].transAxes,horizontalalignment='right')

    def hover(event):
        vis = annot.get_visible()
        if event.inaxes == ax[0]:
            for i in range(N):
                cont,ind = lines[i][0].contains(event)
                if cont:
                    hoverover = labels[i]
                    for j in range(N):
                        lines[j][0].set_linewidth(lw)
                    lines[i][0].set_linewidth(4)
                    annot.set_text(labels[i])
                    fig.canvas.draw_idle()

    fig.canvas.mpl_connect("motion_notify_event", hover)
    # ax[1].plot(x,peak_I,marker='o')
    # ax[1].set_xticks(x,labels)
    # ax[1].set_xlim([-0.3,max(x)+0.3])
    # ax[1].set_ylabel('Peak current (uA)')


    with open(outfile, mode='w') as peaks_file:
        peaks_writer = csv.writer(peaks_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        peaks_writer.writerow(['Label','Peak current','Potential of peak'])
        for i in range(N):
            peaks_writer.writerow([labels[i],peak_I[i],peak_V[i]])

    print 'The following peaks were written to %s' % outfile
    for i in range(len(labels)):
        print labels[i]+'   %s' % peak_I[i]
    plt.show()



    return


#==============================================================================
#===========================START OF INSTRUCTIONS++============================
#==============================================================================


#Hello!
#You found the instructions in the script.
#Perfect.
#Things with a '#' sign in front are comments.
#They allow me to talk to you, but python ignores them.
#Very useful to explain what certain pieces of code do.

#So this is the only area in the code where you should change things.
#It's the two variables below. (Variables are things that read like: a = ...)
#Yani we make a variable called 'a', and we put whatever is right of the = sign in it.

#In this case, it's the variable called 'files'.
#files is a list of strings. Strings are pieces of text.
#It's a list of filenames, or file-paths (if the files are in a folder).

#Below are two examples of how files should be defined. Either its a list with
#only one element, like below (but commented out):

#files=['30/A 0PM.mtd']#This is for one file.

#Or, for multiple files located in a folder called '30'. This line is active
#because it has no # in front of it, so it will be executed:
files=['30/A 0PM.mtc','30/B 100PM.mtc','30/B 1000PM.mtc']#This is for multiple files.

#In addition, the code allows you to put custom labels for the different curves.
#By default, I set these to be the same as the filenames:
names = files
#If you want to change the labels of the curves in the plot, you need to specify this
#variable yourself, like follows. Because this line comes later, it *renames* the
#variable 'names' to a new thing. So the fact that the previous line names=files
#is active, makes no difference. In the following line, names is simply set
#to something new:
names = ['0 PM', '100PM','1000 PM']

#The code will output the peaks that it finds to the following CSV file.
#If you don't change this name each time you run this code on different files,
#any existing csv file will be overwritten.
outfile = '20200918-first-curve-nA-dv.csv'

#Finally instead of setting files and names above, you can also choose to set a
#file folder from which *all* CV or DPV files are read at once. This may be more
#efficient if you have many files to work with, and you get tired of manually
#typing their filenames all the time. For this to work, you need to set the 'folder'
#variable below to something else than False. If you set 'folder' to a wrong name,
#for example a path that doesn't exist, or you comment it out, the code will crash.

folder = False
folder = '20200918-GO-AuNP'

#The extension of the file it will gather is set below. In principle you can set this
#to anything you want, but it will only work for xml files that are generated by your
#CV/DPV machine. I.e. normally this will only work if you set it to 'mtd' or 'mtc'.
ext = 'mtd'
#ext = 'mtc'

#If you have specified the folder correctly, but there are no files with extension
#ext in it, the code will generate an error and crash.


legend_textsize=6#This sets the size of the text in the legend.

unit = 'uA'#This is the unit of current you want to plot the data as.
#The input data is assumed to be micro-amps, but the label can be converted to
#something else by multiplying or dividing by 1,000. You can choose between 'mA',
# 'uA' or 'nA' for milli-amp, micro-amp or nano-amp respectively.


#So finally, from here onwards the code will resume to read the files and make the
#plot. You can already save that plot if you like, but later your azizam can make
#a functionality that saves the plots automatically, depending on what you
#want exactly. As you saw above, the peak values are automatically written to an
#excel-compatible csv file, and also the values are printed to the terminal, so you
#can inspect them quickly and easily.

#==============================================================================
#===========================END OF INSTRUCTIONS++==============================
#==============================================================================






import sys
import numpy as np
import os
import pdb


if folder != False:
    if os.path.exists(folder) != True:
        print 'ERROR: Specified folder (%s) does not exist.' % folder
        sys.exit()
    files = []
    for file in os.listdir(folder):
        if file.endswith("."+ext):
            files.append(os.path.join(folder,file))
    names = files
    if len(files) == 0:
        print 'ERROR: No files with extension %s present in %s' % (ext,folder)




N = len(files)
#This checks that the files and names arrays have the same length.
if len(names) != len(files):
    print "ERROR: The names and files variables should have the same number of elements"
    sys.exit()




#This checks that all files have the same extension.
for i in range(0,N):
    if i ==0:
        ext=files[0].split('.')[1]
    if files[i].split('.')[1] != ext:
        print "ERROR: Not all files have the same extension."
        sys.exit()


ts=[]
Vs=[]
Is=[]


for i in range(N):
    t,V,I,type = read_xml(files[i])
    ts.append(np.array(t))
    Vs.append(np.array(V))
    Is.append(np.array(I))

plot_curve(Vs,Is,names,type,outfile,textsize=legend_textsize,unit=unit)#Does all the magic.
