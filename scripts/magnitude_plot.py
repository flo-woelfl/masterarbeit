"""
Hexbin plot with marginal distributions
=======================================
# docu http://stanford.edu/~mwaskom/software/seaborn/generated/seaborn.jointplot.html
_thumb: .45, .4
"""
import numpy as np
from scipy.stats import kendalltau
import seaborn as sns
from numpy import loadtxt

import pandas as pd

#tips = sns.load_dataset("tips")

depths = loadtxt('../thesis/images/depth_data.txt')
magnitude = loadtxt('../thesis/images/magnitude_data.txt')

# dep_vs_mag = pd.DataFrame(data=[depths, magnitude], columns=["Depth", "Magnitude"])

#dep_vs_mag = loadtxt('../thesis/images/depth_magnitude.txt')

sns.set(style="ticks")

# "Depth in km", "Moment Magnitude",

sns.jointplot(depths, magnitude, kind="scatter", stat_func=None, color="blue")  # original color #4CB391

# sns.jointplot(depths, magnitude, kind="scatter", stat_func=None, color="blue")  # original color #4CB391

sns.axlabel(xlabel='Depth in km', ylabel='Moment Magnitude')

sns.plt.show()