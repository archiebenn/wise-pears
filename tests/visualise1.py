# visualise1.py - viewing the small .npy volumes with pyvista  
# date: 26-10-2026  
# author: Archie Benn sj19031@bristol.ac.uk  

from pathlib import Path
import numpy as np
import pyvista as pv

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# load .npy volumes
# simple
solid_volume = np.load(data_dir / "box.npy")
wall_volume = np.load(data_dir / "wall.npy")
hole_volume = np.load(data_dir / "hole.npy")
# tunnels
tunnels1 = np.load(data_dir / "nest.npy")
tunnels2 = np.load(data_dir / "nest_small.npy")
tunnels3 = np.load(data_dir / "nest_large.npy")

def viewer(volume):

    p = pv.Plotter()

    # create 3D grid with dimensions defined by .npy volume size (+ 1 cell in each dimension for pyvista)
    grid = pv.ImageData(dimensions=np.array(volume.shape) + 1)

    # attach voxel values to the 3D grid cells and label that data as 'open' 
    grid.cell_data["open"] = volume.flatten(order="F")

    # transparent outline of the full volume bounds (cheap wireframe, gives spatial context)
    p.add_mesh(grid.outline(), color="black", line_width=1)

    # tunnel voxels (1s), rendered with partial transparency so overlapping/winding paths are visible
    tunnel_mesh = grid.threshold(0.5, scalars="open")
    p.add_mesh(tunnel_mesh, scalars="open", opacity=0.5, show_edges=False)

    p.show()

viewer(tunnels1)
viewer(tunnels2)
viewer(tunnels3)
