#!/usr/bin/env python3

__author__ = 'Pavel Polishchuk'

import os

plants_grid_dir = '/home/pavlo/IMTM/RAGE/dock/PLANTS/4OF5/grid_dock_01'
plants_grid_dir = '/home/pavlo/IMTM/eEF2/eef2/dock_plants/grid_dock_01'
plants_grid_dir = '/home/pavlo/IMTM/eEF2/u2a/dock_plants/grid_dock_01'
plants_grid_dir = '/home/pavlo/IMTM/eEF2/u5/dock_plants/grid_dock_01'

if not os.path.exists(plants_grid_dir):
    os.makedirs(plants_grid_dir)

protein_file = '../../protein.mol2'
ligand_file = '../../../05-0777_complete.mol2'

constant_params = '# input\nprotein_file ' + protein_file + '\nligand_file ' + ligand_file + '\n'
constant_params += '# scoring function and search settings\nscoring_function chemplp\nsearch_speed speed1\n'
constant_params += '# write single mol2 files (e.g. for RMSD calculation)\nwrite_multi_mol2 0\n'
constant_params += '# cluster algorithm\ncluster_structures 10\ncluster_rmsd 1.0\n'
# constant_params += '# flexible side chains\nflexible_protein_side_chain_string ARG38\nflexible_protein_side_chain_string ASN54\nflexible_protein_side_chain_string ASP2\nflexible_protein_side_chain_string ASP62\nflexible_protein_side_chain_string GLN16\nflexible_protein_side_chain_string GLU104\nflexible_protein_side_chain_string GLU4\nflexible_protein_side_chain_string GLU61\nflexible_protein_side_chain_string GLU66\nflexible_protein_side_chain_string GLU69\nflexible_protein_side_chain_string GLU89\nflexible_protein_side_chain_string GLU90\nflexible_protein_side_chain_string GLY1\nflexible_protein_side_chain_string ILE11\nflexible_protein_side_chain_string ILE81\nflexible_protein_side_chain_string LYS100\nflexible_protein_side_chain_string LYS13\nflexible_protein_side_chain_string LYS22\nflexible_protein_side_chain_string LYS25\nflexible_protein_side_chain_string LYS27\nflexible_protein_side_chain_string LYS39\nflexible_protein_side_chain_string LYS5\nflexible_protein_side_chain_string LYS53\nflexible_protein_side_chain_string LYS55\nflexible_protein_side_chain_string LYS7\nflexible_protein_side_chain_string LYS72\nflexible_protein_side_chain_string LYS73\nflexible_protein_side_chain_string LYS79\nflexible_protein_side_chain_string LYS8\nflexible_protein_side_chain_string LYS86\nflexible_protein_side_chain_string LYS87\nflexible_protein_side_chain_string LYS88\nflexible_protein_side_chain_string LYS99\nflexible_protein_side_chain_string MET12\nflexible_protein_side_chain_string SER47\nflexible_protein_side_chain_string THR28\nflexible_protein_side_chain_string VAL83\n'

x_range = (-78, 24)
y_range = (-5, 86)
z_range = (-110, 5)

x_range = (176, 214)
y_range = (200, 244)
z_range = (340, 396)

x_range = (211, 267)
y_range = (240, 295)
z_range = (178, 225)

for x in range(x_range[0], x_range[1], 5):
    for y in range(y_range[0], y_range[1], 5):
        for z in range(z_range[0], z_range[1], 5):
            coord = (round(x, 1), round(y, 1), round(z, 1))
            with open(plants_grid_dir + '/plantsconfig_x%f_y%f_z%f' % coord, 'wt') as f:
                f.write(constant_params)
                f.write('# output\noutput_dir rigid_dock_x%f_y%f_z%f\n' % coord)
                f.write('# binding site definition\nbindingsite_center %f %f %f\nbindingsite_radius 20.0\n' % coord)



