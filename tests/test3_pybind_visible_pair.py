# pybind_visible_pair.py - testing out whether the Amanatides-Woo algorithm works for a full volume 
# date: 28-10-2026
# author: Archie Benn sj19031@bristol.ac.uk 

import numpy as np
from pathlib import Path
from visivox.ray_occlusion_cpp import visible_pairs

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# load in nest volume .npys
#tunnels = np.load(data_dir / "nest.npy")
vol = np.ones((5, 5, 5), dtype=np.uint8)
vol2 = vol.copy(); vol2[2, 2, 2] = 0 
visibility_results = visible_pairs(vol)
visibility_results2 = visible_pairs(vol2)
# visibility_results 2 has fewer pairs stored in edges (so less visible pair voxels), which is as expected  