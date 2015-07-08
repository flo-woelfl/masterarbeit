#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Project specific function for modifying synthetics on the fly.

:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2015
:license:
    GNU General Public License, Version 3
    (http://www.gnu.org/copyleft/gpl.html)
"""
import numpy as np
import obspy
from obspy.signal.invsim import c_sac_taper


def process_synthetics(st, iteration):
    """
    This function is called after a synthetic file has been read.

    Do whatever you need to do in here and return a potentially modified
    stream object. Make sure that anything you do works with the
    preprocessing function. LASIF expects data and synthetics to have
    exactly the same length before it can pick windows and calculate adjoint
    sources.

    Potential uses for this function are to shift synthetics in time if
    required or to apply some processing to them which LASIF by default does
    not do.

    Please note that you also got the iteration object here, so if you
    want some parameters to change depending on the iteration, just use
    if/else on the iteration objects.

    >>> iteration.name  # doctest: +SKIP
    '11'
    >>> iteration.get_process_params()  # doctest: +SKIP
    {'dt': 0.75,
     'highpass': 0.01,
     'lowpass': 0.02,
     'npts': 500}

    Use ``$ lasif shell`` to play around and figure out what the iteration
    objects can do.
    """
    # =========================================================================
    # Detrend and taper.
    # =========================================================================
    st.detrend("linear")
    st.detrend("demean")
    st.taper(max_percentage=0.05, type="hann")

    # =========================================================================
    # (flo) Extra step needed for SPECFEM
    # this acts like a bandpass filter when applied in freq. domain
    # Perform a frequency domain taper like during the response removal
    # just without an actual response...
    # =========================================================================

    # (lion) Der pre_filt muss gleich wie in dem normalen Preprocessing sein.
    process_params = iteration.get_process_params()
    freqmin = process_params["highpass"]
    freqmax = process_params["lowpass"]

    f2 = 0.9 * freqmin
    f3 = 1.1 * freqmax
    f1 = 0.8 * f2
    f4 = 1.3 * f3
    pre_filt = (f1, f2, f3, f4)

    for tr in st:
        # smart calculation of nfft dodging large primes
        data = tr.data.astype(np.float64)
        org_length = len(data)
        from obspy.signal.util import _npts2nfft
        nfft = _npts2nfft(org_length)

        fy = 1.0 / (tr.stats.delta * 2.0)
        freqs = np.linspace(0, fy, nfft // 2 + 1)

        # Transform data to Frequency domain
        data = np.fft.rfft(data, n=nfft)
        data *= c_sac_taper(freqs, flimit=pre_filt)
        data[-1] = abs(data[-1]) + 0.0j
        # transform data back into the time domain
        data = np.fft.irfft(data)[0:org_length]
        # assign processed data and store processing information
        tr.data = data

    # the sampling rate has to be in accordance with the observed data
    # 10 Hz is currently used in the preprocessed files in LASIF
    # (lion) Hier sind zwei Sachen wichtig und du musst es eventuell anpassen,
    #        damit es mit deinen synthetics zusammenpasst.
    #   1. Das erste Sample muss zur gleichen Zeit wie bei den echten daten
    #      sein. Bei den ASCII files ist das zeit null. Bei dem SAC output von
    #      SPECFEM bin ich mit nicht sicher. Musst du mal schaun.
    #   2. Gleiche sampling rate und Anzahl an samples wie bei den echten
    #      Daten.
    st.interpolate(sampling_rate=1.0 / process_params["dt"],
                   method="weighted_average_slopes",
                   # NUR WENN es auch wirklich Zeit 0 bei SPECFEM ist. Sonst
                   # eventuell anpassen.
                   starttime=obspy.UTCDateTime(0),
                   npts=process_params["npts"])

    return st
