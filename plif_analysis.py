#!/usr/bin/env python3

__author__ = 'Pavel Polishchuk'

import re
import argparse
from collections import OrderedDict


def simplify_plif(plif_tuple):
    return tuple('0' if plif == '0000000' else '1' for plif in plif_tuple)


def get_items_by_indices(iterable, indices):
    return tuple(iterable[i] for i in indices)


def get_conf_number(mol_name_str):
    try:
        return int(re.search("^.*_conf_([0-9]*)\.mol2$", mol_name_str).group(1))
    except AttributeError:
        return None
    except ValueError:
        return None


def main_params(input_fname, output_fname, keep_number, simplify):

    with open(input_fname) as f:
        aa = f.readline().strip().split()
        ref = f.readline().strip().split()
        ref_name = ref[0]
        ref_plif = tuple(ref[1][0+i:7+i] for i in range(0, len(ref[1]), 7))
        mols = OrderedDict()
        for line in f:
            tmp = line.strip().split()
            conf_num = get_conf_number(tmp[0].split("/")[-1])
            if conf_num <= keep_number:
                plif = tuple(tmp[3][0+i:7+i] for i in range(0, len(tmp[3]), 7))
                mols[tmp[0]] = {'score': float(tmp[1]),
                                'Tc': float(tmp[2]),
                                'plif': plif}

    # omit empty features for all mols
    a = [0] * len(aa)
    for i, item in enumerate(ref_plif):
        if item != '0000000':
            a[i] += 1
    for mol in mols.values():
        for i, item in enumerate(mol['plif']):
            if item != '0000000':
                a[i] += 1
    ids_keep = []
    for i, item in enumerate(a):
        if item > 0:
            ids_keep.append(i)

    with open(output_fname, 'wt') as f:
        plif = get_items_by_indices(aa, ids_keep)
        f.write(',,,' + ','.join(plif) + '\n')
        p = simplify_plif(ref_plif) if simplify else ref_plif
        plif = get_items_by_indices(p, ids_keep)
        f.write(ref_name + ',,,' + ','.join(plif) + '\n')
        for k, v in mols.items():
            p = simplify_plif(v['plif']) if simplify else v['plif']
            plif = get_items_by_indices(p, ids_keep)
            f.write(k + ',' + str(v['score']) + ',' + str(v['Tc']) + ',' + ','.join(plif) + '\n')


def main():
    parser = argparse.ArgumentParser(description='Analysis of PLIF output from PyPLIF.')
    parser.add_argument('-i', '--input', metavar='input.csv', required=True,
                        help='input text file with calculated fingerprints.')
    parser.add_argument('-o', '--output', metavar='output.txt', required=True,
                        help='output text file.')
    parser.add_argument('-k', '--keep_number', metavar='1', required=False, default=1,
                        help='number of best conformations of each ligands.')
    parser.add_argument('-s', '--simplify_plif', action='store_true',  default=False,
                        help='set this flag if simplified output is needed (combine all bits for separate amino acids '
                             'in 1 (if at least one bit is 1) or 0 (if all bits are 0)).')

    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "input": input_fnames = v
        if o == "output": output_fname = v
        if o == "keep_number": keep_number = int(v)
        if o == "simplify_plif": simplify = v

    main_params(input_fnames, output_fname, keep_number, simplify)


if __name__ == '__main__':
    main()
