import imagej
import pandas as pd
import os
import numpy
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import pandas as pd

ij = imagej.init('sc.fiji:fiji')
img_name = "RR1.tiff"
macro = """
#@ String name
//MP-ACT (Microplastics Automated Counting Tool) v1.0
//Created by J.C.Prata, V. Reis, J. Matos, J.P.da Costa, A.Duarte, T.Rocha-Santos 2019

macro "MPACT Action Tool - Cd61D32D72D92Da2Db2Dc2D33D43D63D73D93Dd3D34D54D74D94Dd4D35D55D75D95Da5Db5Dc5D36D76D96D37D77D97D3aD4aD5aD7aD8aD9aDbaDcaDdaD3bD5bD7bDcbD3cD4cD5cD7cDccD3dD5dD7dDcdD3eD5eD7eD8eD9eDce"{

open(name);
//8-bit conversion and automatic threshold

run("Invert");
run("8-bit");

run("Threshold...");
setThreshold(0,150);
setOption("BlackBackground", false);
run("Convert to Mask");
run("Set Measurements...", "area shape feret's display redirect=None decimal=3");

//title
title = getTitle();
setBatchMode(true);
mpshape = newArray ("Fibers", "Fragments", "Particles");
for (i = 0; i < mpshape.length; i++) {
    selectWindow(title);
    run("Duplicate...", " ");
    rename(mpshape[i]);
}
run("Tile");

//Analyze Fibers
selectWindow(mpshape[0]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.0-0.3 display");

//Analyze Fragments
selectWindow(mpshape[1]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.3-0.6 display");

//Analyze Particles
selectWindow(mpshape[2]);
run("Analyze Particles...", "size=3-1000000 pixel circularity=0.6-1.0 display");

//Get results and save to excel
for (i = 0; i < mpshape.length; i++) {
    close(mpshape[i]);
}
run("Original Scale");

dir = File.directory; 
name = File.nameWithoutExtension; 
saveAs("results",  name + "_act2_results.csv"); 

}
"""

args =  {'name':img_name}
image = ij.io().open(img_name)

ij.py.run_script("ijm",macro,args)
ij.py.show(image)

result_name = os.path.splitext(args['name'])[0] + "_act2_results.csv"
print(result_name)
data = pd.read_csv(result_name)
ferets = data.loc[:,['FeretX', 'FeretY']]
print(ferets)

# display image
im = Image.open(img_name)
fig, ax = plt.subplots()        # Create figure and axes
for index, row in ferets.iterrows():
    rect = patches.Rectangle((row['FeretX']-3.6, row['FeretY']-3.6), 10, 10, linewidth=1, edgecolor='r', facecolor='none')
    ax.add_patch(rect)
ax.imshow(im)                   # Display the image
plt.show()
