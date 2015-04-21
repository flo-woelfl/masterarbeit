
# script to check if azimuth and dip are correct in the different stationXML files or if they have to be rotated

from obspy import read, read_inventory

filename = input('Please enter the filename with all stations (normally GSN_stations_15.txt): ')

with open(filename) as f:
    #data = f.readlines()
    data = f.read().splitlines()
    for line in data:
        inv = read_inventory(line)
        station = inv.get_contents().items()
        channel = inv[0][0][0]
        print station[-1][1][0], ', azimuth = ', channel.azimuth, ', dip = ', channel.dip
print 'done'




