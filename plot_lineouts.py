#!/usr/bin/env python3

# ========================================================================
#
# Imports
#
# ========================================================================
import argparse
import os
import re
import glob as glob
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import pandas as pd
import utilities


# ========================================================================
#
# Some defaults variables
#
# ========================================================================
plt.rc("text", usetex=True)
plt.rc("figure", max_open_warning=100)
cmap_med = [
    "#F15A60",
    "#7AC36A",
    "#5A9BD4",
    "#FAA75B",
    "#9E67AB",
    "#CE7058",
    "#D77FB4",
    "#737373",
]
cmap = [
    "#EE2E2F",
    "#008C48",
    "#185AA9",
    "#F47D23",
    "#662C91",
    "#A21D21",
    "#B43894",
    "#010202",
]
dashseq = [
    (None, None),
    [10, 5],
    [10, 4, 3, 4],
    [3, 3],
    [10, 4, 3, 4, 3, 4],
    [3, 3],
    [3, 3],
]
markertype = ["s", "d", "o", "p", "h"]


# ========================================================================
#
# Function definitions
#
# ========================================================================


# ========================================================================
#
# Main
#
# ========================================================================
if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(
        description="A simple plot tool for lineout quantities"
    )
    parser.add_argument("-s", "--show", help="Show the plots", action="store_true")
    parser.add_argument(
        "-f",
        "--folders",
        nargs="+",
        help="Folder where files are stored",
        type=str,
        required=True,
    )
    parser.add_argument("-l", "--legend", help="Annotate figures", action="store_true")
    args = parser.parse_args()

    # Constants
    num_figs = 4
    utau = 1
    height = 1

    # Loop on folders
    for i, folder in enumerate(args.folders):

        # Setup
        fdir = os.path.abspath(folder)
        yname = os.path.join(fdir, "channelflow.yaml")

        # simulation setup parameters
        u0, v0, w0, umag0, rho0, mu, flow_angle = utilities.parse_ic(yname)
        nu = mu / rho0
        Retau = utau * height / nu

        # Read in data (all time steps)
        prefix = "output"
        suffix = ".csv"

        # Get time steps
        pattern = prefix + "*" + suffix
        fnames = sorted(glob.glob(os.path.join(fdir, "lineouts", pattern)))
        times = []
        for fname in fnames:
            times.append(int(re.findall(r"\d+", fname)[-1]))
        times = np.unique(sorted(times))

        # Loop over each time step and get the dataframes
        dfs = []
        centerline = np.zeros((len(times), 4))
        for k, time in enumerate(times):
            pattern = prefix + "*." + str(time) + suffix
            fnames = sorted(glob.glob(os.path.join(fdir, "lineouts", pattern)))
            df = utilities.get_merged_csv(fnames)
            df["time"] = time
            renames = utilities.get_renames()
            df.columns = [renames[col] for col in df.columns]
            df["yplus"] = df.y * utau / nu

            idx = (np.fabs(df.y - 1.0)).idxmin()
            centerline[k, 0] = time
            centerline[k, 1] = df.ux.iloc[idx]
            centerline[k, 2] = df.uy.iloc[idx]
            centerline[k, 3] = df.uz.iloc[idx]
            dfs.append(df)

        centerline = pd.DataFrame(centerline, columns=["time", "ux", "uy", "uz"])
        plt.figure("centerline")
        p = plt.plot(centerline.time, centerline.ux, ls="-", lw=1)

        # Plot velocity profiles at the last time
        df = dfs[-1]
        xlocs = np.unique(df.x)
        for k, xloc in enumerate(xlocs):
            subdf = df[np.fabs(df.x - xloc) < 1e-5].copy()

            plt.figure(f"{xloc}_0")
            p = plt.plot(subdf.ux, subdf.y, ls="-", lw=1)

            plt.figure(f"{xloc}_1")
            p = plt.plot(subdf.uy, subdf.y, ls="-", lw=1)

            pdf = subdf[subdf.y <= 1.0].copy()
            plt.figure(f"{xloc}_2")
            p = plt.plot(pdf.yplus, pdf.ux, ls="-", lw=1)

    # Plot DNS data
    dnsdir = os.path.abspath("dns_data")
    dname = os.path.join(dnsdir, "Re5200.txt")
    dns = pd.read_csv(dname, delim_whitespace=True)
    plt.figure("centerline")
    p = plt.plot(
        [centerline.time.min(), centerline.time.max()],
        [dns.U.iloc[-1], dns.U.iloc[-1]],
        ls="-",
        lw=1,
        color=cmap[-1],
    )

    plt.figure(f"3_2")
    plt.plot(dns["y^+"], dns["U"], ls="-", lw=1, color=cmap[-1])

    # Save plots
    fname = "lineouts.pdf"
    with PdfPages(fname) as pdf:

        plt.figure("centerline")
        ax = plt.gca()
        plt.xlabel(r"$t$", fontsize=22, fontweight="bold")
        plt.ylabel(r"$u_x$", fontsize=22, fontweight="bold")
        plt.setp(ax.get_xmajorticklabels(), fontsize=16, fontweight="bold")
        plt.setp(ax.get_ymajorticklabels(), fontsize=16, fontweight="bold")
        plt.tight_layout()
        pdf.savefig(dpi=300)

        for k, xloc in enumerate(xlocs):

            plt.figure(f"{xloc}_0")
            ax = plt.gca()
            plt.xlabel(r"$u_x$", fontsize=22, fontweight="bold")
            plt.ylabel(r"$y$", fontsize=22, fontweight="bold")
            plt.setp(ax.get_xmajorticklabels(), fontsize=16, fontweight="bold")
            plt.setp(ax.get_ymajorticklabels(), fontsize=16, fontweight="bold")
            plt.tight_layout()
            pdf.savefig(dpi=300)

            plt.figure(f"{xloc}_1")
            ax = plt.gca()
            plt.xlabel(r"$u_y$", fontsize=22, fontweight="bold")
            plt.ylabel(r"$y$", fontsize=22, fontweight="bold")
            plt.setp(ax.get_xmajorticklabels(), fontsize=16, fontweight="bold")
            plt.setp(ax.get_ymajorticklabels(), fontsize=16, fontweight="bold")
            plt.tight_layout()
            pdf.savefig(dpi=300)

            plt.figure(f"{xloc}_2")
            ax = plt.gca()
            plt.xlabel(r"$y^{+}$", fontsize=22, fontweight="bold")
            plt.ylabel(r"$u_x$", fontsize=22, fontweight="bold")
            plt.setp(ax.get_xmajorticklabels(), fontsize=16, fontweight="bold")
            plt.setp(ax.get_ymajorticklabels(), fontsize=16, fontweight="bold")
            ax.set_xscale("log")
            plt.tight_layout()
            pdf.savefig(dpi=300)
