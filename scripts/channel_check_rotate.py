import collections
import glob
import os
import shutil
import sys

import obspy
from obspy.signal.rotate import rotate2ZNE

from lasif.components.project import Project


with open("/export/data/fwoelfl/masterarbeit/LASIF/Antarctica/GSN_stations/eventlist.txt") as f:
    data = f.read().splitlines()
    for folder in data:
        folder = "/export/data/fwoelfl/masterarbeit/LASIF/Antarctica/GSN_stations/" + folder 

	comm = Project("/export/data/fwoelfl/masterarbeit/LASIF/Antarctica").comm

	output_folder = os.path.join(folder, "output")
	if os.path.exists(output_folder):
	    sys.exit("Output folder already exists")
	os.makedirs(output_folder)

	files = glob.glob(os.path.join(folder, "*.mseed"))

	net_stat = set()
	for filename in files:
	    net, sta = os.path.basename(filename).split('.')[:2]
	    net_stat.add((net, sta))

	for net, sta in net_stat:
	    files = glob.glob(os.path.join(folder, "%s.%s.*.mseed" % (net, sta)))

	    loc_chans = collections.defaultdict(list)
	    for filename in files:
		loc, chan = os.path.basename(filename).split('.')[2:4]
		loc_chans[loc].append(chan)

	    location = sorted(list(loc_chans.keys()))[0]

	    files = glob.glob(os.path.join(folder, "%s.%s.%s.*.mseed" % (net, sta,
									 location)))
	    channels = {os.path.basename(_i).split(".")[3]: _i for _i in files}

	    files_to_copy = []
	    if "BHZ" in channels:
		files_to_copy.append(channels["BHZ"])
	    if "BHN" in channels:
		files_to_copy.append(channels["BHN"])
	    if "BHE" in channels:
		files_to_copy.append(channels["BHE"])

	    for filename in files_to_copy:
		shutil.copy(filename, os.path.join(output_folder,
						   os.path.basename(filename)))

	    if not ("BHN" in channels or "BHE" in channels) and \
		    "BH1" in channels and "BH2" in channels:
		# Read.
		bhz = obspy.read(channels["BHZ"])
		bh1 = obspy.read(channels["BH1"])
		bh2 = obspy.read(channels["BH2"])

		assert len(bhz) == 1
		assert len(bh1) == 1
		assert len(bh2) == 1

		bhz = bhz[0]
		bh1 = bh1[0]
		bh2 = bh2[0]

		args = []
		# Now rotate.
		for tr in (bhz, bh1, bh2):
		    filename = comm.stations.get_channel_filename(
			tr.id, tr.stats.starttime)
		    channel = obspy.read_inventory(filename).select(
			network=tr.stats.network,
			station=tr.stats.station,
			channel=tr.stats.channel,
			location=tr.stats.location,
			time=tr.stats.starttime)[0][0][0]
		    args.extend([tr.data, channel.azimuth, channel.dip])

		z, n, e = rotate2ZNE(*args)

		bh1.data = n
		bh1.stats.channel = "BHN"
		bh2.data = e
		bh2.stats.channel = "BHE"

		bh1.write(os.path.join(output_folder, "%s.mseed" % bh1.id),
			  format="mseed")
		bh2.write(os.path.join(output_folder, "%s.mseed" % bh1.id),
			  format="mseed")
