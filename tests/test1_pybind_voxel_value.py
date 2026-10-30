# pybind_voxel_value.py - testing if C++ module can access numpy array memory by returning same voxel values as accessing via python
# date: 28-10-2026  
# author: Archie Benn sj19031@bristol.ac.uk  

import numpy as np
from pathlib import Path
from visivox.ray_occlusion_cpp import visible_pairs

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# load in nest volume .npys
tunnels = np.load(data_dir / "nest.npy")

# test whether occlusion_cpp module can access voxel value by comparing asserting all values across the array
# note this calls the C++ function for every voxel in the array - for ray tracing would call it once and hot-loop within C++  
for x in range(tunnels.shape[0]):
    for y in range(tunnels.shape[1]):
        for z in range(tunnels.shape[2]):

            # is what C++ module sees identical to accessing straight via python?  
            assert get_voxel_value(tunnels, x, y, z) == tunnels[x, y, z]

print(f"All {tunnels.size} voxels match.")