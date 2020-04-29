#!/usr/bin/env python3

import os
import json
import nibabel as nib
import numpy as np
from PIL import Image
import sys
import re

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

with open('config.json', encoding='utf8') as config_json:
    config = json.load(config_json)

errors = []
warnings = []
meta = {}

#enumerate all nifties
meta["rois"] = []
merged_img = None
shape = None
count = 0
roispath=config["rois"]+"/rois"
for file in os.listdir(roispath):
    #TODO - maybe check to make sure all rois are same size?
    print(file)
    img = nib.load(roispath+"/"+file)
    img_data = img.get_fdata()

    count += 1

    if shape == None:
        #first image
        shape = img_data.shape
        meta["shape"] = shape
        print(shape)
        merged_img = img_data

    else:
        #following images
        if shape != img_data.shape:
            print("not the same shape")
        else:
            print("shape looks good")

        #merged_img[merged_img<1] = img_data
        merged_img[img_data==1] = count #replace with roi specific value
        #merged_img = np.where(img_data>0, img_data, merged_img)

    #strip .nii.gz out of filename
    m = re.search('(.+?)(.nii.gz)', file)
    meta["rois"].append({"name": m.group(1), "voxels": np.count_nonzero(img_data)})

#np.set_printoptions(threshold=sys.maxsize)
#print("max merged")
#print(np.min(merged_img))
#print(np.max(merged_img))

meta["roicount"] = len(meta["rois"])
#print(merged_img)

#setup outout
if not os.path.exists("output"):
    os.mkdir("output")
    if os.path.lexists("output/rois"):
        os.remove("output/rois")
    os.symlink("../"+config['rois'], "output/rois")

#now work on secondary!
if not os.path.exists("secondary"):
    os.mkdir("secondary")

#normalize image between 0-255
merged_img /= count #normalize to 0-1
merged_img *= 255

#let's create a 3-axis views of all rois superimposed (to show the relationship)
img_x = np.max(merged_img, axis=0)
img_y = np.max(merged_img, axis=1)
img_z = np.max(merged_img, axis=2)

ix = Image.fromarray(np.flipud(img_x))
ix.convert('L').save("secondary/x.png")

iy = Image.fromarray(np.flipud(img_y))
iy.convert('L').save("secondary/y.jpg")

iz = Image.fromarray(np.flipud(img_z))
iz.convert('L').save("secondary/z.jpg")

with open("product.json", "w") as fp:
    json.dump({"errors": errors, "warnings": warnings, "meta": meta}, fp)
print("done");
