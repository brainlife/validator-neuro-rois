#!/usr/bin/env python3

import os
import json

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

errors = []
warnings = []
meta = {}

#enumerate all nifties
meta["rois"] = []
for file in os.listdir(config["rois"]):
    #TODO - maybe check to make sure all rois are same size?
    meta["rois"].append(file)
meta["roicount"] = len(meta["rois"])

#setup outout
if not os.path.exists("output"):
    os.mkdir("output")
    if os.path.lexists("output/rois"):
        os.remove("output/rois")
    os.symlink("../"+config['rois'], "output/rois")

#now work on secondary!
if not os.path.exists("secondary"):
    os.mkdir("secondary")

#TODO - let's create a 3-axis views of all rois superimposed (to show the relationship)

with open("product.json", "w") as fp:
    json.dump({"errors": errors, "warnings": warnings, "meta": meta}, fp)
print("done");
