''' Script to plot the instrument responses of all GSN stations to check if they 
can be rotated or a correction has to be applied''' 

import obspy
from obspy import UTCDateTime

filename = "/export/data/fwoelfl/masterarbeit/LASIF/Antarctica/STATIONS/\
StationXML/GSN_stations.txt"                    


with open(filename) as f:
	data = f.read().splitlines()
	for station in data:
		for time in xrange(4,16,2):
			img = obspy.read_inventory(station).plot_response(1E-3, 
				location = '00', 
				starttime=UTCDateTime(year=time + 2000, month=1, day=1), 
				endtime=UTCDateTime(year=time+2002, month=1, day=1), show=False)
			img.savefig('/export/data/fwoelfl/masterarbeit/LASIF/extra_stuff/'
				'GSN_StationXML_analysis/time_steps/%s200%i.png' 
				%(station[0:-4], time))
print 'done'
