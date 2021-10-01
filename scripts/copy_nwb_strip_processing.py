#! /usr/bin/env python
import argparse, glob, os
from pynwb import NWBHDF5IO


parser = argparse.ArgumentParser(description='Copies nwb and strips away processing module')
parser.add_argument('src_file', type=str, help='Source nwb file')
parser.add_argument('--dst_file', type=str, default=None,
                    help='Destination nwb file. If not specified, then overwrites source file')

args = parser.parse_args()

src_file = args.src_file
dst_file = args.dst_file
overwrite_flag = False

if (dst_file is None) or (dst_file == src_file):
    dst_file = ''.join(src_file.split('.')[:-1]) + '_tmp.nwb'
    overwrite_flag = True


with NWBHDF5IO(src_file, mode='a') as src_io:
    src_nwb = src_io.read()
    try:
        src_nwb.processing.pop('preprocessing')
    except:
        print('No preprocessing module exisits')

    with NWBHDF5IO(dst_file, mode='w') as dst_io:
        dst_io.export(src_io=src_io, nwbfile=src_nwb)

if overwrite_flag:
    os.remove(src_file)
    os.rename(dst_file, src_file)
