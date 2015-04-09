from obspy import read
""" This script will plot every stream
given in the file """

filename = input('Please enter the filename with all streams: ')

with open(filename) as f:
    #data = f.readlines()
    data = f.read().splitlines()
    for line in data:
        st = read(line)
        print st
        name = line.split('/')
        name = name[1] + '_' + name[3]
        plotname = "seismograms/seismo_" + name[0:-7] + ".png"
        st.plot(outfile = plotname)

print 'done'

