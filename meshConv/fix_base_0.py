#!/usr/bin/env python3
import os
import re

base_0_dir = "/home/lavender/OpenFoamUbu/offProjects/solarPanel/meshConv/try2/base/0"

for fname in ["U", "p", "k", "omega", "nut"]:
    fpath = os.path.join(base_0_dir, fname)
    if not os.path.exists(fpath):
        continue
    with open(fpath, 'r') as f:
        content = f.read()
    
    # Replace patch name "constraint" with "(walls|constraint)"
    content = re.sub(r"^\s*constraint\s*$", "    \"(walls|constraint)\"", content, flags=re.MULTILINE)
    
    # Replace patch name "solarPanel" or "wall" to also include all SP patches and bottom
    content = re.sub(r"^\s*solarPanel\s*$", "    \"(.*SP|bottom|wall|solarPanel)\"", content, flags=re.MULTILINE)

    with open(fpath, 'w') as f:
        f.write(content)

print("Updated 0/ boundary conditions in base successfully.")
