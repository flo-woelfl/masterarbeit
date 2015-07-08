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
from obspy.xseed import Parser
from scipy import signal
import warnings
from obspy.signal.invsim import c_sac_taper

from lasif import LASIFError


# flo: read also cmtsolution info?
# flo: read also processing info for origin_time
def process_synthetics(st, iteration, processing_info):  # NOQA
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
    # (flo): zerophase_cheby funtion is already defined in
    # preprocessing_function.py, so maybe it should be called from there
    def zerophase_chebychev_lowpass_filter(trace, freqmax):
        """
        Custom Chebychev type two zerophase lowpass filter useful for
        decimation filtering.

        This filter is stable up to a reduction in frequency with a factor of
        10. If more reduction is desired, simply decimate in steps.

        Partly based on a filter in ObsPy.

        :param trace: The trace to be filtered.
        :param freqmax: The desired lowpass frequency.

        Will be replaced once ObsPy has a proper decimation filter.
        """

       # rp - maximum ripple of passband, rs - attenuation of stopband
        rp, rs, order = 1, 96, 1e99
        ws = freqmax / (trace.stats.sampling_rate * 0.5)  # stop band frequency
        wp = ws  # pass band frequency

        while True:
            if order <= 12:
                break
            wp *= 0.99
            order, wn = signal.cheb2ord(wp, ws, rp, rs, analog=0)

        b, a = signal.cheby2(order, rs, wn, btype="low", analog=0, output="ba")

        # Apply twice to get rid of the phase distortion.
        trace.data = signal.filtfilt(b, a, trace.data)


    # =========================================================================
    # Read seismograms and gather basic information.
    # (flo) Cut window of the seismogram (if processing_info is read in this
    # could be done like for the observed data
    # =========================================================================
    starttime = processing_info["event_information"]["origin_time"]
    endtime = starttime + processing_info["process_params"]["dt"] * \
        (processing_info["process_params"]["npts"] - 1)
    duration = endtime - starttime

    st = obspy.read(processing_info["input_filename"])

    if len(st) != 1:
        warnings.warn("The file '%s' has %i traces and not 1. "
                      "Skip all but the first" % (
                          processing_info["input_filename"], len(st)))
    tr = st[0]

    # Trim with a short buffer in an attempt to avoid boundary effects.
    # starttime is the origin time of the event
    # endtime is the origin time plus the length of the synthetics
    tr.trim(starttime - 0.2 * duration, endtime + 0.2 * duration)

    # =========================================================================
    # Some basic checks on the data.
    # =========================================================================
    # Non-zero length
    if not len(tr):
        msg = "No data found in time window around the event. File skipped."
        raise LASIFError(msg)

    # No nans or infinity values allowed.
    if not np.isfinite(tr.data).all():
        msg = "Data contains NaNs or Infs. File skipped"
        raise LASIFError(msg)

    # (flo) decimation like for the observed data is not required for the
    # synthetics

    # the sampling rate has to be in accordance with the observed data
    # 10 Hz is currently used in the preprocessed files in LASIF
    tr.interpolate(sampling_rate=10)

    # CONVOLUTION WITH SOURCE TIME FUNCTION
    # not required as this is a Heaviside function?

    # =========================================================================
    # Step 2: Detrend and taper.
    # =========================================================================
    tr.detrend("linear")
    tr.detrend("demean")
    tr.taper(max_percentage=0.05, type="hann")

    # =========================================================================
    # (flo) Extra step needed for SPECFEM
    # this acts like a bandpass filter when applied in freq. domain
    # Perform a frequency domain taper like during the response removal
    # just without an actual response...
    # =========================================================================
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

    # =========================================================================
    # Save processed data and clean up.
    # =========================================================================
    # Convert to single precision to save some space.
    tr.data = np.require(tr.data, dtype="float32", requirements="C")
    if hasattr(tr.stats, "mseed"):
        tr.stats.mseed.encoding = "FLOAT32"

    # tr.write(processing_info["output_filename"], format=tr.stats._format)

    # maybe only the trace should be returned?
    return tr
