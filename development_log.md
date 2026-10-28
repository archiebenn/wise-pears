# Development Log 

```
Project: wise-pears
Author: Archie Benn sj19031@bristol.ac.uk  
Date started: 26-10-2026
```

## Goal of this project  

- My PhD will involve the use of microCT scanning ant nests to gain a 3D image of their architecture  
- I want to quantify the visibility of different areas within the nests from these scans to investigate the impact of different digging conditions on the 'openness' of ant nests  
- However, I also want to develop a more general tool which can be used by others, be it in ecology or other areas using microCT  
- So this project aims to be as open as possible, utilising `.npy` objects to generate visibility graphs via `networkx` and 3D visualisation of visibility using `pyvista`   

## Tool pipeline goal (as of october 2026)  

- Aim of the tool is as follows:  

```
1. Raw microCT scans converted to volumes  
2. Volumes thresholded to binary (0 = solid/soil, 1 = open/excavated)  
3. Convert these volumes to `.npy` data type  
4. Load into python and tun `wise_pears` on the `.npy`  
5. `wise_pears` will run an occlusion-based pairwise ray-tracing algorithm between open voxels  
6. If a pair is occluded by a closed voxel, pair-wise 'is_visible' == 0 
7. If not occluded, pair-wise 'is_visible' == 1    
8. This algorithm will run using a C++ algorithm, accessed by python via `pybind11`  
9. Output of C++ function will return a visibility score between 0-1 for every open voxel in the volume  
10. From these scores, a visibility visualiser can be formed (coloured by visibility) using `pyvista`  
11. Also, a visibility graph from `networkx` can be formed too  
12. Tool will return both of these as the output for further analysis  
```

## Main issues  

- Scaling issue: as this is currently set to be pairwise, comparisons between voxels will scale as O(n^2)  
- For large scans of nests at high resolution, this will massively increase compute expense   
- Therefore need to implement in a tight loop in C++ and optimise using known solutions (to-do)  
- Already going to use the Amanitides and Woo algorithm, but could think of some pair-wise solutions too  

### 26-10-2026  

- Started development of `wise-pears`
- Set up python project development and learned about how to create these pip-installable tools
- Tested out using `pyvista` with some generated simple 3D binary volumes with 'solid voxel == 0' and 'open voxel == 1'  

### 28-10-26  

- Generated `intricate_volumes.py` which uses `random` module and a set of defined rules to excavate out random volumes from a set full volume size
- The idea is to generate some intricate test volumes which are similar to ant nests for the development of the visibility graph  
- E.g here is an excavated volume, visualised in `pyvista`, from:
  ```
  c = tunnel_excavater(size=200, seed=3, n_steps=200000, branch_prob=0.0001, radius=1)
  ```
  
![alt text](https://github.com/archiebenn/wise-pears/blob/main/tests/data/images/test_200cubed.png "Test 200^3 excavated volume")
