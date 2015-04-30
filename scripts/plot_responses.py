''' Script to plot the instrument responses of all GSN stations to check if the 
can be rotated or a correction has to be applied''' 

import obspy

filename = "/export/data/fwoelfl/masterarbeit/LASIF/Antarctica/STATIONS/\
StationXML/GSN_stations.txt"                                                          

with open(filename) as f:
    #data = f.readlines()
    data = f.read().splitlines()
    for station in data:
    	img = obspy.read_inventory(station).plot_response(1E-3, location = '00')
    	img.savefig('/export/data/fwoelfl/masterarbeit/LASIF/extra_stuff/\
GSN_StationXML_analysis/location_00/%s.png' %station[0:-4])
    print 'done'
