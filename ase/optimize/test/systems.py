from math import sin, cos, pi

import numpy as np

from ase import Atoms
from ase.build import fcc111, add_adsorbate
from ase.db import connect
from ase.calculators.emt import EMT
from ase.constraints import FixedPlane, FixAtoms
from ase.lattice.cubic import FaceCenteredCubic


systems = []

cell = (5, 5, 5)
atoms = Atoms('H2', [(0, 0, 0), (0, 0, 1.4)], cell=cell)
atoms.center()
systems.append(atoms)

#
atoms = Atoms('Pd4NH',
              [[5.078689759346383, 5.410678028467162, 4.000000000000000],
               [7.522055777772603, 4.000000000000000, 4.000000000000000],
               [7.522055777772603, 6.821356056934325, 4.000000000000000],
               [6.707600438297196, 5.410678028467162, 6.303627574066606],
               [4.807604264052752, 5.728625577716107, 5.919407072553396],
               [4.000000000000000, 5.965167390141987, 6.490469524180266]])
constraint = FixAtoms(mask=[a.symbol == 'Pd' for a in atoms])
atoms.set_constraint(constraint)
atoms.center(vacuum=3.0)
systems.append(atoms)

#
slab = Atoms('Cu32',
             [[-1.028468159509163, -0.432387156877267, -0.202086055768265],
              [0.333333333333333, 0.333333333333333, -2.146500000000000],
              [1.671531840490805, -0.432387156877287, -0.202086055768242],
              [3.033333333333334, 0.333333333333333, -2.146500000000000],
              [4.371531840490810, -0.432387156877236, -0.202086055768261],
              [5.733333333333333, 0.333333333333333, -2.146500000000000],
              [7.071531840490944, -0.432387156877258, -0.202086055768294],
              [8.433333333333335, 0.333333333333333, -2.146500000000000],
              [0.321531840490810, 1.905881433340708, -0.202086055768213],
              [1.683333333333333, 2.671601923551318, -2.146500000000000],
              [3.021531840490771, 1.905881433340728, -0.202086055768250],
              [4.383333333333334, 2.671601923551318, -2.146500000000000],
              [5.721531840490857, 1.905881433340735, -0.202086055768267],
              [7.083333333333333, 2.671601923551318, -2.146500000000000],
              [8.421531840490820, 1.905881433340739, -0.202086055768265],
              [9.783333333333335, 2.671601923551318, -2.146500000000000],
              [1.671531840490742, 4.244150023558601, -0.202086055768165],
              [3.033333333333334, 5.009870513769302, -2.146500000000000],
              [4.371531840490840, 4.244150023558694, -0.202086055768265],
              [5.733333333333333, 5.009870513769302, -2.146500000000000],
              [7.071531840490880, 4.244150023558786, -0.202086055768352],
              [8.433333333333335, 5.009870513769302, -2.146500000000000],
              [9.771531840491031, 4.244150023558828, -0.202086055768371],
              [11.133333333333335, 5.009870513769302, -2.146500000000000],
              [3.021531840490714, 6.582418613776583, -0.202086055768197],
              [4.383333333333334, 7.348139103987287, -2.146500000000000],
              [5.721531840490814, 6.582418613776629, -0.202086055768203],
              [7.083333333333333, 7.348139103987287, -2.146500000000000],
              [8.421531840490985, 6.582418613776876, -0.202086055768357],
              [9.783333333333335, 7.348139103987287, -2.146500000000000],
              [11.121531840490929, 6.582418613776676, -0.202086055768221],
              [12.483333333333334, 7.348139103987287, -2.146500000000000]])
mask = [a.position[2] < -1 for a in slab]
slab.set_constraint(FixAtoms(mask=mask))

h = 1.85
d = 1.10

molecule = Atoms('2N', positions=[(0., 0., h),
                                  (0., 0., h + d)])
slab.extend(molecule)
systems.append(slab)

#
atoms = FaceCenteredCubic(
    directions=[[1, -1, 0], [1, 1, 0], [0, 0, 1]],
    size=(3, 3, 3),
    symbol='Cu',
    pbc=(1, 1, 1))
atoms.rattle(stdev=0.1, seed=42)
systems.append(atoms)

#
a = 2.70
c = 1.59 * a

slab = Atoms('2Cu', [(0., 0., 0.), (1 / 3., 1 / 3., -0.5 * c)],
             tags=(0, 1),
             pbc=(1, 1, 0))
slab.set_cell([(a, 0, 0),
               (a / 2, 3**0.5 * a / 2, 0),
               (0, 0, 1)])
slab.center(vacuum=3, axis=2)
mask = [a.tag == 1 for a in slab]
slab.set_constraint(FixAtoms(mask=mask))
systems.append(slab)

#
zpos = cos(134.3 / 2.0 * pi / 180.0) * 1.197
xpos = sin(134.3 / 2.0 * pi / 180.0) * 1.19
co = Atoms('CO', positions=[(-xpos + 1.2, 0, -zpos),
                            (-xpos + 1.2, -1.1, -zpos)])
slab = fcc111('Au', size=(2, 2, 4), vacuum=5, orthogonal=True)
slab.center()
add_adsorbate(slab, co, 1.5, 'bridge')
slab.set_pbc((True, True, False))
constraint = FixAtoms(mask=[(a.tag == 4) or (a.tag == 3) or (a.tag == 2)
                            for a in slab])
slab.set_constraint(constraint)
systems.append(slab)

#
atoms = Atoms(symbols='C5H12',
              pbc=[False, False, False],
              cell=[16.83752497, 12.18645905, 11.83462179],
              positions=[[5.90380523, 5.65545388, 5.91569796],
                         [7.15617518, 6.52907738, 5.91569796],
                         [8.41815022, 5.66384716, 5.92196554],
                         [9.68108996, 6.52891016, 5.91022362],
                         [10.93006206, 5.65545388, 5.91569796],
                         [5.00000011, 6.30002353, 5.9163716],
                         [5.88571848, 5.0122839, 6.82246859],
                         [5.88625613, 5.01308931, 5.01214155],
                         [7.14329342, 7.18115393, 6.81640316],
                         [7.14551332, 7.17200869, 5.00879027],
                         [8.41609966, 5.00661165, 5.02355167],
                         [8.41971183, 5.0251482, 6.83462168],
                         [9.69568096, 7.18645894, 6.8078633],
                         [9.68914668, 7.16663649, 5.00000011],
                         [10.95518898, 5.02163182, 6.8289018],
                         [11.83752486, 6.29836826, 5.90274952],
                         [10.94464142, 5.00000011, 5.01802495]])
systems.append(atoms)

#
srf = Atoms('Cu64',
            [(1.2763, 1.2763, 4.0000),
             (3.8290, 1.2763, 4.0000),
             (6.3816, 1.2763, 4.0000),
             (8.9343, 1.2763, 4.0000),
             (1.2763, 3.8290, 4.0000),
             (3.8290, 3.8290, 4.0000),
             (6.3816, 3.8290, 4.0000),
             (8.9343, 3.8290, 4.0000),
             (1.2763, 6.3816, 4.0000),
             (3.8290, 6.3816, 4.0000),
             (6.3816, 6.3816, 4.0000),
             (8.9343, 6.3816, 4.0000),
             (1.2763, 8.9343, 4.0000),
             (3.8290, 8.9343, 4.0000),
             (6.3816, 8.9343, 4.0000),
             (8.9343, 8.9343, 4.0000),
             (0.0000, 0.0000, 5.8050),
             (2.5527, 0.0000, 5.8050),
             (5.1053, 0.0000, 5.8050),
             (7.6580, 0.0000, 5.8050),
             (0.0000, 2.5527, 5.8050),
             (2.5527, 2.5527, 5.8050),
             (5.1053, 2.5527, 5.8050),
             (7.6580, 2.5527, 5.8050),
             (0.0000, 5.1053, 5.8050),
             (2.5527, 5.1053, 5.8050),
             (5.1053, 5.1053, 5.8050),
             (7.6580, 5.1053, 5.8050),
             (0.0000, 7.6580, 5.8050),
             (2.5527, 7.6580, 5.8050),
             (5.1053, 7.6580, 5.8050),
             (7.6580, 7.6580, 5.8050),
             (1.2409, 1.2409, 7.6081),
             (3.7731, 1.2803, 7.6603),
             (6.3219, 1.3241, 7.6442),
             (8.8935, 1.2669, 7.6189),
             (1.2803, 3.7731, 7.6603),
             (3.8188, 3.8188, 7.5870),
             (6.3457, 3.8718, 7.6649),
             (8.9174, 3.8340, 7.5976),
             (1.3241, 6.3219, 7.6442),
             (3.8718, 6.3457, 7.6649),
             (6.3945, 6.3945, 7.6495),
             (8.9576, 6.3976, 7.6213),
             (1.2669, 8.8935, 7.6189),
             (3.8340, 8.9174, 7.5976),
             (6.3976, 8.9576, 7.6213),
             (8.9367, 8.9367, 7.6539),
             (0.0582, 0.0582, 9.4227),
             (2.5965, -0.2051, 9.4199),
             (5.1282, 0.0663, 9.4037),
             (7.6808, -0.0157, 9.4235),
             (-0.2051, 2.5965, 9.4199),
             (2.1913, 2.1913, 9.6123),
             (5.0046, 2.5955, 9.4873),
             (7.5409, 2.5336, 9.4126),
             (0.0663, 5.1282, 9.4037),
             (2.5955, 5.0046, 9.4873),
             (5.3381, 5.3381, 9.6106),
             (7.8015, 5.0682, 9.4237),
             (-0.0157, 7.6808, 9.4235),
             (2.5336, 7.5409, 9.4126),
             (5.0682, 7.8015, 9.4237),
             (7.6155, 7.6155, 9.4317)])
c2 = Atoms('C2', [(3.2897, 3.2897, 10.6627),
                  (4.2113, 4.2113, 10.6493)])
srf.extend(c2)
srf.pbc = (1, 1, 0)
srf.set_cell([10.2106, 10.2106, 20.6572], scale_atoms=False)

mask = [a.index < 32 for a in srf]
c1 = FixedPlane(-1, (1 / np.sqrt(2), 1 / np.sqrt(2), 1))
c2 = FixedPlane(-2, (1 / np.sqrt(2), 1 / np.sqrt(2), 1))
constraint = FixAtoms(mask=mask)
srf.set_constraint([constraint, c1, c2])
systems.append(srf)


def create_database():
    db = connect('systems.db', append=False)
    for atoms in systems:
        atoms.calc = EMT()
        db.write(atoms)


if __name__ == '__main__':
    create_database()
