#!/usr/bin/env python3

import argparse
import os

__author__ = 'Pavel Polishchuk'


def get_coord_range(mol2_fname):
    x = []
    y = []
    z = []
    with open(mol2_fname) as f:
        line = f.readline()
        while line.strip() != "@<TRIPOS>ATOM":
            line = f.readline()
        line = f.readline()
        while not line.strip() or line[0] != "@":
            coords = line.strip().split()[2:5]
            coords = tuple(map(float, coords))
            x.append(coords[0])
            y.append(coords[1])
            z.append(coords[2])
            line = f.readline()
    return min(x), max(x), min(y), max(y), min(z), max(z)


def main(protein_fname, ligand_fname, output_dir, radius, step):

    coords = get_coord_range(protein_fname)
    coords = tuple(map(int, coords))

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    constant_params = '# input\nprotein_file %s\n' % os.path.relpath(protein_fname, output_dir)
    constant_params += '\nligand_file %s\n\n' % os.path.relpath(ligand_fname, output_dir)
    constant_params += '# scoring function and search settings\nscoring_function chemplp\nsearch_speed speed1\n\n'
    constant_params += '# write single mol2 files (e.g. for RMSD calculation)\nwrite_multi_mol2 0\n\n'
    constant_params += '# cluster algorithm\ncluster_structures 1\ncluster_rmsd 1.0\n\n'

    for x in range(coords[0], coords[1], step):
        for y in range(coords[2], coords[3], step):
            for z in range(coords[4], coords[5], step):
                coord = (int(x), int(y), int(z))
                with open(output_dir + '/plantsconfig_x%i_y%i_z%i' % coord, 'wt') as f:
                    f.write(constant_params)
                    f.write('# output\noutput_dir dock_x%i_y%i_z%i\n\n' % coord)
                    f.write('# binding site definition\nbindingsite_center %i %i %i\n' % coord)
                    f.write('bindingsite_radius %f\n' % step)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create plantsconfig files for grid search.')
    parser.add_argument('-p', '--protein', metavar='protein.mol2', required=True,
                        help='input protein MOL2 file.')
    parser.add_argument('-l', '--ligand', metavar='ligand.mol2', required=True,
                        help='input ligand MOL2 file.')
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


