# pyvista_output.py - colouring voxels on pyvista by their visibility from pairwise occlusion calculations  
# date: 28-10-2026
# author: Archie Benn sj19031@bristol.ac.uk 

import numpy as np
import time
import pyvista as pv
from pathlib import Path
from wise_pears.ray_occlusion_cpp import visible_pairs

# get data directory  
data_dir = Path(__file__).resolve().parent / "data"

# small test volumes 
vol = np.ones((5, 5, 5), dtype=np.uint8)
vol2 = vol.copy(); vol2[0:2, 0:2, 0:2] = 0 

# load in nest volume .npys
# 15^3 test
small_15_nest = np.load(data_dir / "nest_small.npy")
medium_100_nest = np.load(data_dir / "nest.npy")
large_200_nest = np.load(data_dir / "nest_large.npy")


def visibility_visualiser(vol):

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

    grid.cell_data["open"] = vol.flatten(order="F")
    score_volume = np.full(vol.shape, np.nan, dtype=float)
    score_volume[tuple(coords.T)] = scores
    grid.cell_data["visibility_score"] = score_volume.flatten(order="F")

    # transparent outline of the full volume bounds (cheap wireframe, gives spatial context)
    p.add_mesh(grid.outline(), color="black", line_width=1)

    # render each open voxel as a cell colored by its visibility score
    voxel_mesh = grid.threshold(0.5, scalars="open")

    p.add_mesh(voxel_mesh, 
            scalars="visibility_score",
                cmap="turbo", 
                opacity=0.5,
                show_edges=False)

    t_build = time.perf_counter() - t0_build

    print(f"open voxels: {n}, rays: {n_rays:,}, visible pairs: {len(edges):,}")
    print(f"time in C++ 'hot loop': {t_cpp:.5f}s")
    print(f"average time per ray: {t_cpp / n_rays * 1e6:.5f} µs")
    print(f"total before render: {t_build:.3f}s")

    p.show()


visibility_visualiser(small_15_nest)
