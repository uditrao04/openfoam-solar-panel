#!/usr/bin/env python3
import os
import subprocess
import re

base_dir = "/home/lavender/OpenFoamUbu/offProjects/solarPanel/meshConv/try2/meshes"

print("==========================================================")
print("  Running Mesh Generation & Measuring Cell Counts (0 to 14)")
print("==========================================================")

for lvl in range(15):
    level_dir = os.path.join(base_dir, f"level{lvl}")
    if not os.path.exists(level_dir):
        print(f"Level {lvl}: directory not found")
        continue

    # Execute allMesh inside level_dir
    res = subprocess.run(["./allMesh"], cwd=level_dir, capture_output=True, text=True)
    
    # Read cell count from log.checkMesh
    check_mesh_log = os.path.join(level_dir, "log.checkMesh")
    ncells = "Unknown"
    if os.path.exists(check_mesh_log):
        with open(check_mesh_log, 'r') as f:
            log_txt = f.read()
        match = re.search(r"cells:\s*(\d+)", log_txt)
        if match:
            ncells = int(match.group(1))
            ncells = f"{ncells:,} cells ({ncells/1e6:.3f} M)"

    print(f"Level {lvl:2d}: {ncells}")

print("==========================================================")
