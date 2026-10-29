# pyvista_example.py - view pyvista example outputs coloured buy voxel visibility scores 
# date: 28-10-2026
# author: Archie Benn sj19031@bristol.ac.uk 

import numpy as np
import time
import pyvista as pv
from pathlib import Path
from wise_pears.ray_occlusion_cpp import visible_pairs

# get data directory  
data_dir = Path(__file__).resolve().parent / "volumes"

# load in generated example nest volume .npys
small_20_nest = np.load(data_dir / "nest_small.npy")
medium_100_nest = np.load(data_dir / "nest.npy")
large_150_nest = np.load(data_dir / "nest_large.npy")


def visibility_visualiser(vol):
    """
    Takes a volume in .npy format with binary voxel values of 0 or 1 (0 = solid, 1 = open).  

    Runs the visible_pairs function (written in C++ for efficiency) and computes visibility scores for every open voxel in the volume.

    Visibility scores of open voxels are then visualised in 3D on the volume using pyvista.
    """

    t0_build = time.perf_counter()

    # run main C++ Amanatides & Woo algorithm for ray tracing all open voxel pairs  
    t0_cpp = time.perf_counter()
    coords, edges = visible_pairs(vol)
    t_cpp = time.perf_counter() - t0_cpp

    n = len(coords)
    n_rays = n * (n - 1) // 2

    # count visible connections per voxel (each edge contributes to both endpoints)
    counts = np.bincount(edges[:, 0], minlength=n) + np.bincount(edges[:, 1], minlength=n)
    scores = counts  #/ (n - 1)  # normalises to 0-1 if un-hashed

    p = pv.Plotter()

    # create 3D grid with dimensions defined by .npy volume size (+ 1 cell in each dimension for pyvista)
    grid = pv.ImageData(dimensions=np.array(vol.shape) + 1)

    # flatten cells for pyvista, and attach 0/1 voxel values to the volume grid  
    grid.cell_data["open"] = vol.flatten(order="F")

    # start with every cell in volume as NaN 
    score_volume = np.full(vol.shape, np.nan, dtype=float)

    # access summed open voxel visibility scores from np.bincount on the visible_pairs() output and apply to the cells in volume
    score_volume[tuple(coords.T)] = scores
    grid.cell_data["visibility_score"] = score_volume.flatten(order="F")

    # transparent outline of the full volume bounds for spatial context  
    p.add_mesh(grid.outline(), color="black", line_width=1)

    # render each open voxel as a cell colored by its visibility score
    voxel_mesh = grid.threshold(0.5, scalars="open")
    p.add_mesh(voxel_mesh, 
            scalars="visibility_score",
                cmap="turbo", 
                opacity=0.5,
                show_edges=False)

    t_build = time.perf_counter() - t0_build

    print(f"Open voxels: {n}, rays cast: {n_rays:,}, visible pairs: {len(edges):,}")
    print(f"Time in C++ 'hot loop': {t_cpp:.5f}s")
    print(f"Average time per ray: {t_cpp / n_rays * 1e6:.5f} µs")
    print(f"Total time before render: {t_build:.3f}s")

    p.show()


visibility_visualiser(large_150_nest)
