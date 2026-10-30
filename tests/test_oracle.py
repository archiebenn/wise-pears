# test_oracle.py - tests C++ function against a brute-force version 
# date: 29-10-2026  
# author: Archie Benn sj19031@bristol.ac.uk (+ Claude for pytest guidance)  

import numpy as np
import pytest
from itertools import combinations, product
from fractions import Fraction
from visivox.ray_occlusion_cpp import visible_pairs

def brute_force_bounds(vol, a, b):
    """
    Exact oracle: returns strict (strict, lenient) visibility between open voxels a <-> b

    Strict -> 
    Lenient -> 

    """

    # work in doubled coordinates so everything stays an integer: centre = 2i+1, voxel = [2i, 2i+2]
    # ray start = centre of voxel a
    A = [2 * i + 1 for i in a]
    # ray direction vector (centre of b - centre of a)
    d = [2 * (j - i) for i, j in zip(a, b)]
    # highest and lowest voxel indices ray can touch for each axis
    lo_v = [min(i, j) for i, j in zip(a, b)]
    hi_v = [max(i, j) for i, j in zip(a, b)]

    # segment touches a solid voxel at all (including corners/edges)
    touches = False   
    # segment passes through a solid voxel's interior 
    crosses = False    

    # loop over every voxel in the bounding box of the two endpoints
    for v in product(*[range(l, h + 1) for l, h in zip(lo_v, hi_v)]):
        if vol[v]:
            continue             
        t0, t1 = Fraction(0), Fraction(1) 
        inside_open = True
        for k in range(3):
            lo, hi = 2 * v[k], 2 * v[k] + 2
            if d[k] == 0:
                if not lo <= A[k] <= hi:
                    t0, t1 = Fraction(1), Fraction(0)
                if not lo < A[k] < hi:
                    inside_open = False
            else:
                ta, tb = Fraction(lo - A[k], d[k]), Fraction(hi - A[k], d[k])
                t0, t1 = max(t0, min(ta, tb)), min(t1, max(ta, tb))
        if t0 <= t1:
            touches = True
            if t0 < t1 and inside_open:
                crosses = True
    return not touches, not crosses  

# pytest: assert that brute force and my C++ function arrive at the same results for visibility  
# run over 20 seeds for random
@pytest.mark.parametrize("seed", range(20))
def test_matches_brute_force(seed):
    """C++ result must lie between the strict and lenient brute-force answers."""

    rng = np.random.default_rng(seed)

    # 6^3 volume with 70% chance per voxel being set to open (1)  
    vol = (rng.random((6, 6, 6)) > 0.3).astype(np.uint8)

    # np.argwhere(vol) returns coordinates of non empty (i.e. open) voxels only  
    # so open_vox is a list of tuples of coords for open voxels in volume  
    open_vox = [tuple(int(v) for v in p) for p in np.argwhere(vol)]

    # every unique voxel pair, only once  
    for a, b in combinations(open_vox, 2):

        # lowest and higehest acceptable answers  
        strict, lenient = brute_force_bounds(vol, a, b)
        cpp = is_visible(vol, *a, *b)
        # assert that C++ result falls between these bounds  
        assert strict <= cpp <= lenient, (
            f"seed={seed} a={a} b={b} C++={cpp} strict={strict} lenient={lenient}"
        )