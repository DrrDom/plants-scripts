#!/usr/bin/env python3

import argparse
import os
import numpy as np

from itertools import product

__author__ = 'Pavel Polishchuk'


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


def binding_site_coords(mol2_fname, step):
    # yield a point if it is close to protein
    m = get_atom_coords(mol2_fname)
    min_values = np.min(m, 0).astype(int)
    max_values = np.max(m, 0).astype(int)
    for x, y, z in product(range(min_values[0], max_values[0], step),
                           range(min_values[1], max_values[1], step),
                           range(min_values[2], max_values[2], step)):
        if min(np.sum((m - [x, y, z]) ** 2, 1) ** 0.5) <= 5:
            yield round(x), round(y), round(z)


def main(protein_fname, ligand_fname, output_dir, radius, step):

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    constant_params = '# input\nprotein_file %s\n' % os.path.abspath(protein_fname)
    constant_params += '\nligand_file %s\n\n' % os.path.abspath(ligand_fname)
    constant_params += '# scoring function and search settings\nscoring_function chemplp\nsearch_speed speed1\n\n'
    constant_params += '# write single mol2 files (e.g. for RMSD calculation)\nwrite_multi_mol2 0\n\n'
    constant_params += '# cluster algorithm\ncluster_structures 1\ncluster_rmsd 1.0\n\n'
    constant_params += 'bindingsite_radius %f\n\n' % radius

    for coord in binding_site_coords(protein_fname, step):
        with open(output_dir + '/plantsconfig_x%i_y%i_z%i' % coord, 'wt') as f:
            f.write(constant_params)
            f.write('# output\noutput_dir %s/dock_x%i_y%i_z%i\n\n' % (os.path.abspath(output_dir), coord[0], coord[1], coord[2]))
            f.write('# binding site definition\nbindingsite_center %i %i %i\n' % coord)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create plantsconfig files for grid search.')
    parser.add_argument('-p', '--protein', metavar='protein.mol2', required=True,
                        help='input protein MOL2 file.')
    parser.add_argument('-l', '--ligands', metavar='ligands.mol2', required=True,
                        help='input MOL2 file with ligands.')
    parser.add_argument('-d', '--output_dir', metavar='output_dir', required=True,
                        help='output dir where plantsconfig files will be stored.')
    parser.add_argument('-r', '--radius', metavar='VALUE', required=False, default=20,
                        help='binding site radius. Default: 20.')
    parser.add_argument('-s', '--step', metavar='INTEGER', required=False, default=5,
                        help='step of the grid search. Default: 5.')

    args = vars(parser.parse_args())
    for o, v in args.items():
        if o == "protein": protein_fname = v
        if o == "ligand": ligand_fname = v
        if o == "radius": radius = float(v)
        if o == "output_dir": output_dir = v
        if o == "step": step = int(v)

    main(protein_fname, ligand_fname, output_dir, radius, step)


