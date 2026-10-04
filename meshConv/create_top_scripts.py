#!/usr/bin/env python3
import os

base_dir = "/home/lavender/OpenFoamUbu/offProjects/solarPanel/meshConv/try2"

allmesh_top = """#!/bin/bash
#----------------------------------*-sh-*--------------------------------------
# =========                 |                                                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
#  \\    /   O peration     | Version:  v2412                                 |
#   \\  /    A nd           | Website:  www.openfoam.com                      |
#    \\/     M anipulation  |                                                 |
#------------------------------------------------------------------------------

cd "${0%/*}" || exit 1
echo "======================================================================"
echo "  Starting Parallel Mesh Generation for Mesh Convergence Levels 0 to 14"
echo "======================================================================"
for case_dir in level0 level1 level2 level3 level4 level5 level6 level7 level8 level9 level10 level11 level12 level13 level14; do
    if [ -d "$case_dir" ]; then
        echo ""
        echo ">>> Meshing $case_dir..."
        (
            cd "$case_dir" || exit 1
            if [ -f "./allMesh" ]; then
                ./allMesh
            elif [ -f "./Allmesh" ]; then
                ./Allmesh
            fi
            rm -rf processor*
            rm -f 0/cellLevel 0/pointLevel
        )
        echo ">>> $case_dir meshing finished."
    fi
done
echo "======================================================================"
echo "  All 15 Mesh Convergence Levels Generated Successfully!"
echo "======================================================================"
"""

allrun_top = """#!/bin/bash
#----------------------------------*-sh-*--------------------------------------
# =========                 |                                                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
#  \\    /   O peration     | Version:  v2412                                 |
#   \\  /    A nd           | Website:  www.openfoam.com                      |
#    \\/     M anipulation  |                                                 |
#------------------------------------------------------------------------------

cd "${0%/*}" || exit 1
echo "======================================================================"
echo "  Starting CFD Solver Execution (5k iters, 8 ranks) for Levels 0 to 14"
echo "======================================================================"
for case_dir in level0 level1 level2 level3 level4 level5 level6 level7 level8 level9 level10 level11 level12 level13 level14; do
    if [ -d "$case_dir" ]; then
        echo ""
        echo ">>> Running Solver for $case_dir..."
        (
            cd "$case_dir" || exit 1
            if [ ! -d "constant/polyMesh" ] || [ ! -f "constant/polyMesh/points" ]; then
                echo "  No mesh found in $case_dir. Running mesh generation first..."
                if [ -f "./allMesh" ]; then ./allMesh; elif [ -f "./Allmesh" ]; then ./Allmesh; fi
            fi
            if [ -f "./allrun" ]; then
                ./allrun
            elif [ -f "./Allrun" ]; then
                ./Allrun
            fi
        )
        echo ">>> $case_dir solver run finished."
    fi
done
echo "======================================================================"
echo "  All 15 Mesh Convergence Solver Runs Completed!"
echo "======================================================================"
"""

allsolve_top = """#!/bin/bash
#----------------------------------*-sh-*--------------------------------------
# =========                 |                                                 |
# \\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox           |
#  \\    /   O peration     | Version:  v2412                                 |
#   \\  /    A nd           | Website:  www.openfoam.com                      |
#    \\/     M anipulation  |                                                 |
#------------------------------------------------------------------------------

cd "${0%/*}" || exit 1
echo "======================================================================"
echo "  Starting AllSolve (Check Mesh + Run Solver) for Levels 0 to 14"
echo "======================================================================"
for case_dir in level0 level1 level2 level3 level4 level5 level6 level7 level8 level9 level10 level11 level12 level13 level14; do
    if [ -d "$case_dir" ]; then
        echo ""
        echo ">>> Processing $case_dir..."
        (
            cd "$case_dir" || exit 1
            if [ -f "./allsolve" ]; then
                ./allsolve
            elif [ -f "./Allsolve" ]; then
                ./Allsolve
            else
                if [ ! -d "constant/polyMesh" ] || [ ! -f "constant/polyMesh/points" ]; then
                    echo "  No mesh found in $case_dir. Running meshing..."
                    if [ -f "./allMesh" ]; then ./allMesh; elif [ -f "./Allmesh" ]; then ./Allmesh; fi
                else
                    echo "  Mesh already exists in $case_dir. Skipping meshing."
                fi
                if [ -f "./allrun" ]; then ./allrun; elif [ -f "./Allrun" ]; then ./Allrun; fi
            fi
        )
        echo ">>> $case_dir completed."
    fi
done
echo "======================================================================"
echo "  AllSolve Execution Completed for All 15 Levels!"
echo "======================================================================"
"""

# Write to try2/meshes, try2/runs, and try2/
target_dirs = [
    os.path.join(base_dir, "meshes"),
    os.path.join(base_dir, "runs")
]

for d in target_dirs:
    for name, content in [
        ("allMesh", allmesh_top), ("Allmesh", allmesh_top),
        ("allrun", allrun_top), ("Allrun", allrun_top),
        ("allsolve", allsolve_top), ("Allsolve", allsolve_top)
    ]:
        p = os.path.join(d, name)
        with open(p, 'w') as f:
            f.write(content)
        os.chmod(p, 0o755)

# For try2 root, script that enters runs/ or runs all
allmesh_root = """#!/bin/bash
cd "${0%/*}" || exit 1
echo "=== Running allMesh in meshes/ ==="
( cd meshes && ./allMesh )
"""

allrun_root = """#!/bin/bash
cd "${0%/*}" || exit 1
echo "=== Running allrun in runs/ ==="
( cd runs && ./allrun )
"""

allsolve_root = """#!/bin/bash
cd "${0%/*}" || exit 1
echo "=== Running allsolve in runs/ ==="
( cd runs && ./allsolve )
"""

for name, content in [
    ("allMesh", allmesh_root), ("Allmesh", allmesh_root),
    ("allrun", allrun_root), ("Allrun", allrun_root),
    ("allsolve", allsolve_root), ("Allsolve", allsolve_root)
]:
    p = os.path.join(base_dir, name)
    with open(p, 'w') as f:
        f.write(content)
    os.chmod(p, 0o755)

print("Top-level scripts created successfully.")
