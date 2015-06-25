
# plot seismograms as obtained from SPECFEM3D GLOBE in the OUTPUT_FILES folder

import matplotlib.pyplot as plt
import numpy as np


filename = input('Please enter the filename with the SPECFEM seismogram: ')

with open(filename) as f:
    lines = f.readlines()
    x1 = []
    y1 = []
    for line in lines:
        p = line.split()
        x1.append(float(p[0]))
        y1.append(float(p[1]))
    xv = np.array(x1)
    yv = np.array(y1)
    plt.plot(xv, yv)
    plt.show()

print('done')
