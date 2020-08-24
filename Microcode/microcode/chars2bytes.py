#!/bin/python
import argparse
import re
import struct

parser = argparse.ArgumentParser(description='Convert retarded plain text bytes to actual ones.')
parser.add_argument('inputfiles', type=argparse.FileType('r'),
                    nargs='+', help='Input file')
parser.add_argument('-o', '--output-files', nargs='*',
                    required=False, default=[], help='Output file')
args = parser.parse_args()

if len(args.output_files) < len(args.inputfiles):
    print("Not enough output file names. Using default ones.")
    args.output_files = map(lambda file: open(file.name+".bin", "wb"), args.inputfiles)

ins = iter(args.inputfiles)
outs = iter(args.output_files)

for infile in ins:
    outfile = next(outs)

    for char in re.split(r"\s", infile.read()):
        if char != "":
            try:
                byte = int(char, 16)
            except ValueError:
                print(f"File '{infile.name}' contained invalid byte: '{char}'.")
            else:
                outfile.write(struct.pack('B', byte))
    print(f"{outfile.name} saved.")

print("Done!")
