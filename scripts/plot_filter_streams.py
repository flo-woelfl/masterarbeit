from obspy import read
import obspy.signal 
""" This script will plot every stream
given in the file """

filename = input('Please enter the filename with all streams: ')
period_low = input('Please enter the corner frequency for the lowpass filter in seconds: ')

with open(filename) as f:
    #data = f.readlines()
    data = f.read().splitlines()
    for line in data:
        st_raw = read(line)
        name = line.split('/')
        name = name[1] + '_' + name[3]
        plotname = "seismograms_filtered/seismo_" + name[0:-7] + "_" + str(period_low) + "sec" + ".png"
        st = st_raw.copy()
        print st
        st.detrend('demean')
        st.taper(max_percentage=0.1, type= 'cosine') # maybe more percentage is needed or another taper? 
        st.filter("lowpass", freq = 1./period_low) 
        st.plot(outfile = plotname)
print 'done'

