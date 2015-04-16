#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Script to split a large MiniSEED into many smaller ones. It will split based on
the full SEED id. It makes the assumption that each channel is contiguous in
the MiniSEED file, e.g. the records belonging to a single channel are next to
each other in the file.

It will cut the file at the record boundaries, thus no information is lost.


Execute

python split_large_mseed_file.py -h

for some help.


:copyright:
    Lion Krischer (krischer@geophysik.uni-muenchen.de), 2015
:license:
    GNU Lesser General Public License, Version 3
    (http://www.gnu.org/copyleft/lesser.html)
"""
import argparse
import io
import obspy
import os
from struct import unpack
import warnings


ENDIAN = {0: '<', 1: '>'}


def get_filename(output_folder, channel_id):
    _i = 0
    while True:
        if _i == 0:
            appendix = ""
        else:
            appendix = "_%i" % (str(_i))
        filename = os.path.join(output_folder,
                                channel_id + appendix + ".mseed")
        if not os.path.exists(filename):
            break
    return filename


def split_file(filename, output_folder):
    file_size = os.path.getsize(filename)
    current_id = None
    current_buffer = None

    with io.open(filename, "rb") as fh:
        while True:
            if fh.tell() >= file_size:
                break
            info = getRecordInformation(fh)
            channel_id = (info["network"], info["station"],
                          info["location"], info["channel"])
            channel_id = ".".join(channel_id)

            if channel_id == current_id:
                current_buffer.write(fh.read(info["record_length"]))
                continue
            else:
                if current_buffer is not None:
                    # Get the best matching filename.
                    filename = get_filename(output_folder, current_id)
                    current_buffer.seek(0, 0)
                    with io.open(filename, "wb") as fh2:
                        fh2.write(current_buffer.read())
                    print("Wrote %s." % filename)
                    current_buffer.close()
                current_buffer = io.BytesIO()
                current_id = channel_id

        filename = get_filename(output_folder, current_id)
        current_buffer.seek(0, 0)
        with io.open(filename, "wb") as fh2:
            fh2.write(current_buffer.read())
        print("Wrote %s." % filename)
        current_buffer.close()


def getRecordInformation(file_or_file_object, offset=0, endian=None):
    """
    Custom version of obspy.mseed.util.getRecordInformation.
    """
    if isinstance(file_or_file_object, basestring):
        with open(file_or_file_object, 'rb') as f:
            info = _getRecordInformation(f, offset=offset, endian=endian)
    else:
        info = _getRecordInformation(file_or_file_object, offset=offset,
                                     endian=endian)
    return info


def _getRecordInformation(file_object, offset=0, endian=None):
    """
    Custom version of obspy.mseed.util.getRecordInformation.

    Contains features not yet in ObsPy stable.

    Searches the first Mini-SEED record stored in file_object at the current
    position and returns some information about it.

    If offset is given, the Mini-SEED record is assumed to start at current
    position + offset in file_object.

    :param endian: If given, the byte order will be enforced. Can be either "<"
        or ">". If None, it will be determined automatically.
        Defaults to None.
    """
    initial_position = file_object.tell()
    record_start = initial_position
    samp_rate = None

    info = {}

    # Apply the offset.
    file_object.seek(offset, 1)
    record_start += offset

    # Get the size of the buffer.
    file_object.seek(0, 2)
    info['filesize'] = int(file_object.tell() - record_start)
    file_object.seek(record_start, 0)

    # check current position
    if info['filesize'] % 256 != 0:
        # if a multiple of minimal record length 256
        record_start = 0
    elif file_object.read(8)[6:7] not in [b'D', b'R', b'Q', b'M']:
        # if valid data record start at all starting with D, R, Q or M
        record_start = 0
    file_object.seek(record_start, 0)

    # check if full SEED or Mini-SEED
    if file_object.read(8)[6:7] == b'V':
        # found a full SEED record - seek first Mini-SEED record
        # search blockette 005, 008 or 010 which contain the record length
        blockette_id = file_object.read(3)
        while blockette_id not in [b'010', b'008', b'005']:
            if not blockette_id.startswith(b'0'):
                msg = "SEED Volume Index Control Headers: blockette 0xx" + \
                      " expected, got %s"
                raise Exception(msg % blockette_id)
            # get length and jump to end of current blockette
            blockette_len = int(file_object.read(4))
            file_object.seek(blockette_len - 7, 1)
            # read next blockette id
            blockette_id = file_object.read(3)
        # Skip the next bytes containing length of the blockette and version
        file_object.seek(8, 1)
        # get record length
        rec_len = pow(2, int(file_object.read(2)))
        # reset file pointer
        file_object.seek(record_start, 0)
        # cycle through file using record length until first data record found
        while file_object.read(7)[6:7] not in [b'D', b'R', b'Q', b'M']:
            record_start += rec_len
            file_object.seek(record_start, 0)

    # Jump to the network, station, location and channel codes.
    file_object.seek(record_start + 8, 0)
    data = file_object.read(12)
    info["station"] = data[:5].strip().decode()
    info["location"] = data[5:7].strip().decode()
    info["channel"] = data[7:10].strip().decode()
    info["network"] = data[10:12].strip().decode()

    # Use the date to figure out the byte order.
    file_object.seek(record_start + 20, 0)
    # Capital letters indicate unsigned quantities.
    data = file_object.read(28)

    def fmt(s):
        return str('%sHHBBBxHHhhBBBxlxxH' % s)

    if endian is None:
        try:
            endian = ">"
            values = unpack(fmt(endian), data)
            starttime = obspy.UTCDateTime(
                year=values[0], julday=values[1],
                hour=values[2], minute=values[3], second=values[4],
                microsecond=values[5] * 100)
        except:
            endian = "<"
            values = unpack(fmt(endian), data)
            starttime = obspy.UTCDateTime(
                year=values[0], julday=values[1],
                hour=values[2], minute=values[3], second=values[4],
                microsecond=values[5] * 100)
    else:
        values = unpack(fmt(endian), data)
        try:
            starttime = obspy.UTCDateTime(
                year=values[0], julday=values[1],
                hour=values[2], minute=values[3], second=values[4],
                microsecond=values[5] * 100)
        except:
            msg = ("Invalid starttime found. The passed byte order is likely "
                   "wrong.")
            raise ValueError(msg)
    npts = values[6]
    info['npts'] = npts
    samp_rate_factor = values[7]
    samp_rate_mult = values[8]
    info['activity_flags'] = values[9]
    # Bit 1 of the activity flags.
    time_correction_applied = bool(info['activity_flags'] & 2)
    info['io_and_clock_flags'] = values[10]
    info['data_quality_flags'] = values[11]
    time_correction = values[12]
    blkt_offset = values[13]

    # Correct the starttime if applicable.
    if (time_correction_applied is False) and time_correction:
        # Time correction is in units of 0.0001 seconds.
        starttime += time_correction * 0.0001

    # Traverse the blockettes and parse Blockettes 100, 500, 1000 and/or 1001
    # if any of those is found.
    while blkt_offset:
        file_object.seek(record_start + blkt_offset, 0)
        blkt_type, next_blkt = unpack(str('%sHH' % endian),
                                      file_object.read(4))
        if next_blkt != 0 and (next_blkt < 4 or next_blkt - 4 <= blkt_offset):
            msg = ('Invalid blockette offset (%d) less than or equal to '
                   'current offset (%d)') % (next_blkt, blkt_offset)
            raise ValueError(msg)
        blkt_offset = next_blkt

        # Parse in order of likeliness.
        if blkt_type == 1000:
            encoding, word_order, record_length = \
                unpack(str('%sBBB' % endian),
                       file_object.read(3))
            if ENDIAN[word_order] != endian:
                msg = 'Inconsistent word order.'
                warnings.warn(msg, UserWarning)
            info['encoding'] = encoding
            info['record_length'] = 2 ** record_length
        elif blkt_type == 1001:
            info['timing_quality'], mu_sec = \
                unpack(str('%sBb' % endian),
                       file_object.read(2))
            starttime += float(mu_sec) / 1E6
        elif blkt_type == 500:
            file_object.seek(14, 1)
            mu_sec = unpack(str('%sb' % endian),
                            file_object.read(1))[0]
            starttime += float(mu_sec) / 1E6
        elif blkt_type == 100:
            samp_rate = unpack(str('%sf' % endian),
                               file_object.read(4))[0]

    # If samprate not set via blockette 100 calculate the sample rate according
    # to the SEED manual.
    if not samp_rate:
        if (samp_rate_factor > 0) and (samp_rate_mult) > 0:
            samp_rate = float(samp_rate_factor * samp_rate_mult)
        elif (samp_rate_factor > 0) and (samp_rate_mult) < 0:
            samp_rate = -1.0 * float(samp_rate_factor) / float(samp_rate_mult)
        elif (samp_rate_factor < 0) and (samp_rate_mult) > 0:
            samp_rate = -1.0 * float(samp_rate_mult) / float(samp_rate_factor)
        elif (samp_rate_factor < 0) and (samp_rate_mult) < 0:
            samp_rate = -1.0 / float(samp_rate_factor * samp_rate_mult)
        else:
            # if everything is unset or 0 set sample rate to 1
            samp_rate = 1

    info['samp_rate'] = samp_rate

    info['starttime'] = starttime
    # Endtime is the time of the last sample.
    info['endtime'] = starttime + (npts - 1) / samp_rate
    info['byteorder'] = endian

    info['number_of_records'] = int(info['filesize'] //
                                    info['record_length'])
    info['excess_bytes'] = int(info['filesize'] % info['record_length'])

    # Reset file pointer.
    file_object.seek(initial_position, 0)
    return info


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Split a large MiniSEED file into smaller ones.')

    parser.add_argument("filename", type=str, help="Name of the MiniSEED file")
    parser.add_argument("output_folder", type=str, help="Output folder")

    args = parser.parse_args()

    if not os.path.exists(args.filename):
        raise ValueError("File '%s' not found." % args.filename)

    if os.path.exists(args.output_folder):
        raise ValueError("Output folder '%s' already exists." %
                         args.output_folder)

    os.makedirs(args.output_folder)

    split_file(args.filename, args.output_folder)
