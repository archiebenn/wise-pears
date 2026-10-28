# pybind_visible_voxel.py - testing out whether the Amanatides-Woo algorithm works for a single pair of voxels
# date: 28-10-2026
# author: Archie Benn sj19031@bristol.ac.uk 

import numpy as np
from pathlib import Path
from wise_pears.ray_occlusion_cpp import is_visible

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# load in nest volume .npys
#tunnels = np.load(data_dir / "nest.npy")

vol = np.ones((5, 5, 5), dtype=np.uint8)
assert is_visible(vol, 0, 0, 0, 4, 4, 4)
vol[2, 2, 2] = 0  # wall on the diagonal
assert not is_visible(vol, 0, 0, 0, 4, 4, 4)
assert is_visible(vol, 0, 0, 0, 0, 0, 4)  # axis-aligned, avoids the wall
