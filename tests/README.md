# Development Log 

```
Project: wise-pears
Author: Archie Benn sj19031@bristol.ac.uk  
Date started: 26-10-2026
```

## 26-10-2026  

- Started development of `wise-pears`
- Set up python project development and learned about how to create these pip-installable tools
- Tested out using `pyvista` with some generated simple 3D binary volumes with 'solid voxel == 0' and 'open voxel == 1'  

## 28-10-26  

- Generated `intricate_volumes.py` which uses `random` module and a set of defined rules to excavate out random volumes from a set full volume size
- E.g here is an excavated volume, visualised in `pyvista`, from:
  ```
  c = tunnel_excavater(size=200, seed=3, n_steps=200000, branch_prob=0.0001, radius=1)
  ```
  
![alt text](https://github.com/archiebenn/wise-pears/blob/main/tests/data/images/test_200cubed.png "Test 200^3 excavated volume")
