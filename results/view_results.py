"""
Module to view the resulting symmetry planes.

Author: Dan Billmann

"""
import os
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

if __name__ in "__main__":
    start_dir = Path(os.getcwd())
    skip_input = False

    if os.getcwd().split("/")[-1] == "pylateral_facial_symmetry":
        os.chdir("results")
    dirs = os.listdir()

    try:
        for dirname in dirs:
            dname = Path(dirname)
            for fname in dname.rglob("*.npy"):
                array = np.load(fname)
                print(f"Symmetry plane for {fname}\n{'-'*60}\n{array}\n")

                fig = plt.figure()
                ax = fig.add_subplot(111, projection="3d")
                zs = ("y", (1, 1, 1), None)
                for i, row in zip(zs, array):
                    x, y, z = np.round(row, 3)
                    ax.scatter(x, y, z)
                    ax.text(x, y, z, f"[{x}, {y}, {z}]", zdir=i)
                ax.set_xlabel("X Label")
                ax.set_ylabel("Y Label")
                ax.set_zlabel("Z Label")

                plt.savefig(
                    start_dir
                    / Path("results")
                    / Path(dirname)
                    / (fname.stem + "_plot.png")
                )

                if skip_input is False:
                    from_kb = input("Press ENTER to continue...")
                    # press any letter or number to skip
                    if from_kb in ("abcderfghijklmnopqrstuvwxyz0123456789 "):
                        skip_input = True

    except KeyboardInterrupt:
        print("Keyboard Exited")
