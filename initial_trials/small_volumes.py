# small_volumes.py - testing small .npy volumes  
# date: 26-10-2026  
# author: Archie Benn sj19031@bristol.ac.uk  

import numpy as np  
from pathlib import Path

# tests/data directory
data_dir = Path(__file__).resolve().parent

# box volume 10^3  
# np.zeros fills every cell with '0' (nest data will be binary open or closed so this works fine)  
# 0 here will represent solid space, and 1 will represent an open voxel    
a = np.zeros((512,512,512), dtype=np.uint8)

# box with wall (voxels == 0 across the middle)  
# b[:,:,6] =  0 sets all cells in plane at index 6 (5th layer) to 0 or 'closed' i.e. nothing  
b = a.copy(); b[:,:,6] = 1

# box with a hole to connect two sides at 5,4:6,6
c = b.copy(); c[5,4:6,6] = 0

# saving out the .npy test volumes
np.save(data_dir / "box.npy", a)
np.save(data_dir / "wall.npy", b)
np.save(data_dir / "hole.npy", c)