# visualise2.py - trying out some very basic ray tracing across simple voxel-volumes  
# date: 26-10-2026  
# author: Archie Benn sj19031@bristol.ac.uk  

from pathlib import Path
import numpy as np
import pyvista as pv

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# load .npy volumes
empty_volume = np.load(data_dir / "box.npy")
wall_volume = np.load(data_dir / "wall.npy")
hole_volume = np.load(data_dir / "hole.npy")

# function to show the voxel path a single ray takes from a -> b on pyvista  
def ray_path(volume, a, b, path):

    # define plotter and grid
    p = pv.Plotter()
    grid = pv.ImageData(dimensions=np.array(volume.shape) + 1)

    # attach voxel values to the 3D grid cells and label that data as 'open' if > 0.5 and set to 0.2 opacity  
    grid.cell_data["open"] = volume.flatten(order="F")

    # render full volume (un hash to see but will likely render slow)
    # p.add_mesh(grid.threshold(0.5, scalars="open"), opacity=0.65)
                # show_edges=True) - adds extra overhead on large renders 

    # render just the surface around open spaces + open spaces
    surface = grid.threshold(0.5, scalars="open").extract_surface(algorithm='dataset_surface')
    p.add_mesh(surface, opacity=1.0)

    # ray line from a -> b (voxel centres = index + 0.5)
    p.add_mesh(pv.Line(np.array(a) + .5, np.array(b) + .5), color="blue", line_width=4)

    # voxels the traversal visited
    p.add_points(np.array(path) + .5, color="yellow", point_size=20)
    p.show()

# test
start = (0, 0, 0)
end = (5, 5, 6)
# path is set of voxel coordinates ray passes through (ray_path just shows path, not calculated)
path_1 = [start, (2, 3, 3), (3, 4, 4), end]

ray_path(hole_volume, start, end, path_1)
