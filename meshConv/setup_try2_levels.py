#!/usr/bin/env python3
import os
import shutil
import re

base_dir = "/home/lavender/OpenFoamUbu/offProjects/solarPanel/meshConv/try2"
base_template = os.path.join(base_dir, "base")

# Update locationInMesh in base snappyHexMeshDict
base_shm = os.path.join(base_template, "system", "snappyHexMeshDict")
if os.path.exists(base_shm):
    with open(base_shm, 'r') as f:
        content = f.read()
    content = re.sub(r"locationInMesh\s+\([-0-9\.\s]+\);", "locationInMesh (0.0 2.0 0.0);", content)
    with open(base_shm, 'w') as f:
        f.write(content)

levels_spec = [
    # level 0 (~50k cells)
    {"block": (30, 10, 20), "top": (3,3), "sides": (3,4), "support": (5,5), "near": 2, "wake": 1},
    # level 1 (~80k cells)
    {"block": (32, 11, 21), "top": (3,3), "sides": (4,4), "support": (5,5), "near": 2, "wake": 1},
    # level 2 (~120k cells)
    {"block": (34, 11, 22), "top": (3,4), "sides": (4,4), "support": (5,5), "near": 2, "wake": 1},
    # level 3 (~170k cells)
    {"block": (36, 12, 24), "top": (3,4), "sides": (4,4), "support": (5,5), "near": 3, "wake": 1},
    # level 4 (~230k cells)
    {"block": (38, 13, 25), "top": (4,4), "sides": (4,4), "support": (5,5), "near": 3, "wake": 1},
    # level 5 (~300k cells)
    {"block": (40, 13, 26), "top": (4,4), "sides": (4,4), "support": (5,5), "near": 3, "wake": 1},
    # level 6 (~380k cells)
    {"block": (41, 14, 27), "top": (4,4), "sides": (4,5), "support": (5,5), "near": 3, "wake": 1},
    # level 7 — BASE SIM (~465k cells)
    {"block": (42, 14, 28), "top": (4,5), "sides": (5,5), "support": (5,5), "near": 3, "wake": 1},
    # level 8 (~650k cells)
    {"block": (45, 15, 30), "top": (4,5), "sides": (5,5), "support": (5,5), "near": 3, "wake": 2},
    # level 9 (~1.0M cells)
    {"block": (48, 16, 32), "top": (4,5), "sides": (5,5), "support": (5,5), "near": 4, "wake": 1},
    # level 10 (~1.5M cells)
    {"block": (51, 17, 34), "top": (5,5), "sides": (5,5), "support": (5,5), "near": 4, "wake": 2},
    # level 11 (~2.2M cells)
    {"block": (54, 18, 36), "top": (5,5), "sides": (5,6), "support": (5,6), "near": 4, "wake": 2},
    # level 12 (~2.9M cells)
    {"block": (58, 19, 38), "top": (5,5), "sides": (5,6), "support": (6,6), "near": 4, "wake": 2},
    # level 13 (~3.7M cells)
    {"block": (63, 21, 42), "top": (5,5), "sides": (5,6), "support": (6,6), "near": 4, "wake": 2},
    # level 14 — MAX REFINEMENT (~4.65M cells)
    {"block": (69, 23, 46), "top": (5,5), "sides": (5,6), "support": (6,6), "near": 4, "wake": 2},
]

def update_block_mesh(file_path, dims):
    with open(file_path, 'r') as f:
        content = f.read()
    pattern = r"hex\s+\(0\s+1\s+2\s+3\s+4\s+5\s+6\s+7\)\s+\(\d+\s+\d+\s+\d+\)"
    replacement = f"hex (0 1 2 3 4 5 6 7) ({dims[0]} {dims[1]} {dims[2]})"
    content = re.sub(pattern, replacement, content)
    with open(file_path, 'w') as f:
        f.write(content)

def update_snappy_mesh(file_path, spec):
    with open(file_path, 'r') as f:
        content = f.read()
    
    top = spec["top"]
    sides = spec["sides"]
    support = spec["support"]
    near = spec["near"]
    wake = spec["wake"]
    
    content = re.sub(r"topSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"topSP      {{ level ({top[0]} {top[1]});", content)
    content = re.sub(r"bottomSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"bottomSP   {{ level ({top[0]} {top[1]});", content)
    content = re.sub(r"frontSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"frontSP    {{ level ({sides[0]} {sides[1]});", content)
    content = re.sub(r"rearSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"rearSP     {{ level ({sides[0]} {sides[1]});", content)
    content = re.sub(r"leftSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"leftSP     {{ level ({sides[0]} {sides[1]});", content)
    content = re.sub(r"rightSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"rightSP    {{ level ({sides[0]} {sides[1]});", content)
    content = re.sub(r"supportSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"supportSP  {{ level ({support[0]} {support[1]});", content)
    content = re.sub(r"stumpSP\s*\{\s*level\s*\(\d+\s+\d+\);", f"stumpSP    {{ level ({support[0]} {support[1]});", content)

    # nearBodyBox
    content = re.sub(r"(nearBodyBox\s*\{\s*mode\s+inside;\s*levels\s*\(\(1E15\s+)\d+(\)\);)", f"\\g<1>{near}\\2", content)
    # wakeBox
    content = re.sub(r"(wakeBox\s*\{\s*mode\s+inside;\s*levels\s*\(\(1E15\s+)\d+(\)\);)", f"\\g<1>{wake}\\2", content)

    # Ensure locationInMesh is robust for parallel meshing
    content = re.sub(r"locationInMesh\s+\([-0-9\.\s]+\);", "locationInMesh (0.0 2.0 0.0);", content)

    with open(file_path, 'w') as f:
        f.write(content)

def make_single_level_scripts(level_dir, idx):
    allmesh_content = f"""#!/bin/bash
cd "${{0%/*}}" || exit 1
echo "=== Meshing Level {idx} ==="
sed -i 's/numberOfSubdomains.*/numberOfSubdomains  8;/' system/decomposeParDict
blockMesh > log.blockMesh 2>&1
decomposePar -force > log.decomposePar 2>&1
mpirun -np 8 snappyHexMesh -parallel -overwrite > log.snappyHexMesh 2>&1
reconstructParMesh -constant > log.reconstructParMesh 2>&1
rm -rf processor*
rm -f 0/cellLevel 0/pointLevel
checkMesh > log.checkMesh 2>&1
NCELLS=$(grep -oP 'cells:\\s*\\K[0-9]+' log.checkMesh | head -1)
echo "=== Level {idx} meshing complete: ${{NCELLS}} cells ==="
"""
    allrun_content = f"""#!/bin/bash
cd "${{0%/*}}" || exit 1
echo "============================================================"
echo "  Level {idx} — CPU mode (MPI rank 8, simpleFoam, 5k iters)"
echo "============================================================"
if [ ! -d "constant/polyMesh" ] || [ ! -f "constant/polyMesh/points" ]; then
    echo "ERROR: No mesh found. Run ./allMesh first."
    exit 1
fi
rm -f 0/cellLevel 0/pointLevel
sed -i 's/numberOfSubdomains.*/numberOfSubdomains  8;/' system/decomposeParDict
decomposePar -force > log.decomposePar 2>&1
mpirun -np 8 simpleFoam -parallel 2>&1 | tee log.simpleFoam
reconstructPar -latestTime > log.reconstructPar 2>&1
echo "============================================================"
echo "  Level {idx} — Complete"
echo "============================================================"
"""
    allsolve_content = f"""#!/bin/bash
cd "${{0%/*}}" || exit 1
if [ ! -d "constant/polyMesh" ] || [ ! -f "constant/polyMesh/points" ] || [ ! -s "constant/polyMesh/points" ]; then
    echo "  No mesh found for Level {idx}. Running mesh step..."
    if [ -f "./allMesh" ]; then ./allMesh; elif [ -f "./Allmesh" ]; then ./Allmesh; fi
else
    echo "  Mesh already exists for Level {idx}. Skipping mesh step."
fi
echo "  Running solver for Level {idx}..."
if [ -f "./allrun" ]; then ./allrun; elif [ -f "./Allrun" ]; then ./Allrun; fi
"""

    for name, text in [
        ("Allmesh", allmesh_content), ("allMesh", allmesh_content),
        ("Allrun", allrun_content), ("allrun", allrun_content),
        ("Allsolve", allsolve_content), ("allsolve", allsolve_content)
    ]:
        p = os.path.join(level_dir, name)
        with open(p, 'w') as f:
            f.write(text)
        os.chmod(p, 0o755)

subdirs = ["meshes", "runs"]
for s in subdirs:
    target_parent = os.path.join(base_dir, s)
    os.makedirs(target_parent, exist_ok=True)
    
    for idx, spec in enumerate(levels_spec):
        level_name = f"level{idx}"
        level_path = os.path.join(target_parent, level_name)
        if os.path.exists(level_path):
            shutil.rmtree(level_path)
        
        shutil.copytree(base_template, level_path)
        
        bm = os.path.join(level_path, "system", "blockMeshDict")
        shm = os.path.join(level_path, "system", "snappyHexMeshDict")
        if os.path.exists(bm):
            update_block_mesh(bm, spec["block"])
        if os.path.exists(shm):
            update_snappy_mesh(shm, spec)
        
        make_single_level_scripts(level_path, idx)

print("Setup of 15 levels updated with rod capturing & fixed p0.")
