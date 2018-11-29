#!/usr/bin/env python3

import os
import glob
import argparse
import numpy as np


def get_atom_coords(mol2_fname):
    m = []
    with open(mol2_fname) as f:
        line = f.readline()
        while line.strip() != "@<TRIPOS>ATOM":
            line = f.readline()
        line = f.readline()
        while not line.strip() or line[0] != "@":
            coords = line.strip().split()[2:5]
            m.append(tuple(map(float, coords)))
            line = f.readline()
    return np.array(m)


def main(input_dname, output_fname):
    with open(output_fname, 'wt') as fout:
        for fname in glob.iglob('%s/**/bestranking.csv' % input_dname, recursive=True):
            with open(fname) as f:
                f.readline()
                for line in f:
                    mol_name, score = line.split(',', 2)[:2]
                    coords = get_atom_coords(os.path.join(os.path.dirname(fname), mol_name + '.mol2'))
                    center = np.average(coords, 0)
                    item = os.path.dirname(fname).split('/') + [mol_name, score, center[0], center[1], center[2]]
                    fout.write('\t'.join(map(str, item)) + '\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collect data from grid docking with PLANTS (bestranking.csv files).')
    parser.add_argument('-i', '--input', metavar='input_dir', required=True,
                        help='dir from which recursive search of bestranking.csv files will start '
                             'to retrieve docking results.')
    parser.add_argument('-o', '--output', metavar='output.txt', required=True,
                        help='output text file with dock data. Path to docked mol split on dirs, mol name, '
                             'score, coordinates of a centroid of a molecule.')

    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "input": input_dname = v
        if o == "output": output_fname = v

    main(input_dname, output_fname)
