#!/usr/bin/env python3

import argparse
import os
from collections import defaultdict


def main(pdb_fname, remove_na):
    d = defaultdict(list)
    with open(pdb_fname) as pdb:
        for line in pdb:
            if line[:6] in ['ATOM  ', 'TER   ', 'HETATM']:
                if remove_na and line[17:20].strip() in ['U', 'T', 'G', 'C', 'A']:
                    continue
                else:
                    d[line[21]].append(line)
    for name, lines in d.items():
        with open(os.path.splitext(pdb_fname)[0] + "_chain_%s.pdb" % name, 'wt') as f:
            f.write(''.join(lines))
            f.write('END\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Split PDB by chains and save to separate PDB files. '
                                                 'Only ATOM, TER and HETATM sections are stored.')
    parser.add_argument('-i', '--in', metavar='input.pdb', required=True,
                        help='input PDB file.')
    parser.add_argument('-x', '--remove_nucleic_acid', action='store_true',  default=False,
                        help='remove residues with IDs U, T, C, G, A. Default: false.')

    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "in": pdb_fname = v
        if o == "remove_nucleic_acid": remove_na = v

    main(pdb_fname=pdb_fname, remove_na=remove_na)


