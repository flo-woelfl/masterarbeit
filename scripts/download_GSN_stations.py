# script to download all GSN stations in the domain for all events 

from obspy.fdsn import Client
from obspy.fdsn.header import FDSNException
from obspy import UTCDateTime

from lasif.components.project import Project

comm = Project(".").comm

stations = [
    ("IU", "PMSA"),
    ("IU", "CASY"),
    ("GT", "SBA"),
    ("IU", "QSPA"),
    ("GT", "VNDA"),
    ("II", "HOPE"),
    ("II", "EFI"),
    ("GT", "PLCA"),
    ("IU", "TRQA"),
    ("IU", "TRIS"),
    ("II", "SUR"),
    ("GT", "BOSA"),
    ("GT", "LBTB"),
    ("II", "TAU"),
    ("IU", "NWAO"),
    ("IU", "SNZO")]

c = Client("IRIS")

for event in comm.events.list():
    event = comm.events.get(event)

    starttime = event["origin_time"] - 300
    endtime = event["origin_time"] + 3600

    bulk_list = []
    for station in stations:
        bulk_list.append([station[0], station[1], "*", "BH*",
                          starttime, endtime])


    print "Downloading", event["event_name"], "..."
    try:
        c.get_waveforms_bulk(bulk_list, filename=event["event_name"] + ".mseed")
    except FDSNException as e:
        print "Could not download due to", str(e)
    print "Done"
