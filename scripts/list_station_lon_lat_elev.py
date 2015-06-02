"""script to list the latitude longitude and elevation to prepare the SPECFEM DATA/STATIONS file
   this file should be run from  ~/SpiderOak Hive/masterarbeit/organisational/GSN_StationXML_from_IRIS_edit """

from obspy import read, read_inventory


filename = input('Please enter the filename with all stations (normally GSN_xml.txt): ')

print 'This script will display the station name, the network name, latitude, longitude and elevation'
print 'The burial will be assumed to be zero'

with open(filename) as f:
    #data = f.readlines()
    data = f.read().splitlines()
    for line in data:
        inv = read_inventory(line)
        station = inv.get_contents().items()
        channel = inv[0][0][0]
        network_name, station_name = station[-1][1][0].split('.')
        print station_name[0:4], network_name, channel.latitude, channel.longitude, channel.elevation, '  0'
print 'done'





