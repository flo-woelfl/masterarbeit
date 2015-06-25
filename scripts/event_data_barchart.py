# script to make a bar chart of events with the amount of data 

import numpy as np
import matplotlib.pyplot as plt

raw = np.loadtxt('../thesis/images/data_sorted_by_origin_time.txt')

ev = np.loadtxt('../thesis/images/events_sorted_by_origin_time.txt', dtype='string')

# mag = np.loadtxt('../thesis/images/magnitude_by_origin_time.txt')

plt.barh(np.arange(len(raw)), raw) 
plt.yticks(np.arange(len(raw)), ev)
plt.xlabel('Raw seismograms per event') 
plt.tight_layout() # arranges extra space for the ylabel
plt.show()

