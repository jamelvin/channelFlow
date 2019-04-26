# ----------------------------------------------------------------
# imports
# ----------------------------------------------------------------
# import the simple module from the paraview
from paraview.simple import *

# disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

import os
import glob
import shutil
import argparse
import math

# ----------------------------------------------------------------
# setup
# ----------------------------------------------------------------

parser = argparse.ArgumentParser(description="Post process using paraview")
parser.add_argument(
    "-f", "--folder", help="Folder to post process", type=str, required=True
)
args = parser.parse_args()

# Get file names
fdir = os.path.abspath(args.folder)
pattern = "*.e*"
fnames = sorted(glob.glob(os.path.join(fdir, pattern)))
yname = os.path.join(os.path.dirname(fdir), "channelflow.yaml")

odir = os.path.join(os.path.dirname(fdir), "lineouts")
shutil.rmtree(odir, ignore_errors=True)
os.makedirs(odir)
opfx = os.path.join(odir, "output")

# ----------------------------------------------------------------
# setup the data processing pipelines
# ----------------------------------------------------------------

# create list of fields
fields = ["velocity_", "turbulent_ke"]
blocks = ["unspecified-2-hex"]

# create a new 'ExodusIIReader'
exoreader = ExodusIIReader(FileName=fnames)
exoreader.PointVariables = fields
exoreader.SideSetArrayStatus = []
exoreader.ElementBlocks = blocks

# get active view
renderView1 = GetActiveViewOrCreate("RenderView")

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=exoreader, Source="High Resolution Line Source")
plotOverLine1.Source.Resolution = 100000

# Line out coordinates
xcens = [3.0]
for k, xcen in enumerate(xcens):
    plotOverLine1.Source.Point1 = [xcen, 0.0, math.pi * 0.5]
    plotOverLine1.Source.Point2 = [xcen, 2.0, math.pi * 0.5]

    # ----------------------------------------------------------------
    # save data
    # ----------------------------------------------------------------
    SaveData(
        opfx + "_lineout_{0:d}.csv".format(k),
        proxy=plotOverLine1,
        Precision=5,
        UseScientificNotation=0,
        WriteTimeSteps=1,
        FieldAssociation="Points",
    )
