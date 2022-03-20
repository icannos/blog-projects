import pandas as pd
import numpy as np
from sys import argv
import datetime
import time

from geopy import distance
from mpl_toolkits.basemap import Basemap
import matplotlib

if len(argv) != 2:
    print("Usage: ./solve_dinners.py <csv file>")
    exit(1)

data = pd.read_csv(argv[1], sep=";", header=0)

tuples = [
    (
        city,
        datetime.datetime.strptime(tb, "%H:%M"),
        datetime.datetime.strptime(te, "%H:%M"),
        lat,
        lon,
        tb,
        te,
    )
    for city, tb, te, lat, lon in data.itertuples(index=False, name=None)
]


def config(speed=750):
    def d(t1, t2):
        return datetime.timedelta(
            hours=distance.distance((t1[3], t1[4]), (t2[3], t2[4])).km / speed
        )

    def maxdinners(current_path, left):
        bpath = []
        path = []

        for i in left:
            if len(current_path) == 0:
                current_path.append(i)
                path = maxdinners(current_path, left - {i})
                current_path.pop()
            else:
                if tuples[i][1] >= tuples[current_path[-1]][2] + d(
                    tuples[i], tuples[current_path[-1]]
                ):
                    current_path.append(i)
                    path = maxdinners(current_path, left - {i})
                    current_path.pop()

            if len(path) > len(bpath):
                bpath = path

        return bpath if len(bpath) > len(current_path) else [i for i in current_path]

    return maxdinners, d


paths = []
speeds = [750, 2000, 10000]
for speed in speeds:
    maxdinners, d = config(speed)
    path = maxdinners([], {i for i in range(len(tuples))})
    paths.append(path)


import matplotlib.pyplot as plt

cmap = matplotlib.cm.get_cmap("jet")
for speed, path in zip(speeds, paths):
    fig, ax = plt.subplots(figsize=(15, 15))

    ax.annotate(f"Speed {speed} km/h", xy=(500000, 3000000), fontsize=20)
    map = Basemap(
        projection="lcc",
        lat_0=59.9133301,
        lon_0=10.7389701,
        width=5000000,
        height=5000000,
    )
    map.drawcountries(linewidth=0.25)
    map.drawcoastlines(linewidth=0.25)
    visited = set([i for i in path])
    for i in visited:
        c, _, _, x, y, tb, te = tuples[i]
        ax.annotate(f"{c} \n {tb} - {te}", map(y, x), fontsize=11)
    print(len(path))
    for i in range(len(path) - 1):
        c1, _, _, x, y, tb1, te1 = tuples[path[i]]
        c2, _, _, u, v, tb2, te2 = tuples[path[i + 1]]
        map.drawgreatcircle(y, x, v, u, c=cmap(speed / max(speeds)))

    plt.tight_layout()
    plt.savefig(f"{speed}.png")
