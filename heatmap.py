import pickle
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from matplotlib.gridspec import GridSpec
import sys
sys.path.append('../accuqt/scripts')
from accuqt.scripts import qt_correctors as corrector

def read_data(file):
    """
    :param file: data file

    Read the ECG data and perform conventional QT correction
    """
    with open(file, mode='rb') as f:
        data = pickle.load(f)
    qt, rr, qtc = np.nan_to_num(data[0][:, 0]), np.nan_to_num(data[0][:, 1]), np.nan_to_num(data[0][:, 2])

    bazett = corrector.bazett_corrector(rr, qt)
    fridericia = corrector.fridericia_corrector(rr, qt)
    framingham = corrector.framingham_corrector(rr, qt)
    hodges = corrector.hodges_corrector(rr, qt)
    methods = [qt, bazett, framingham, qtc, fridericia, hodges]

    # Call the plotting function for different correction methods
    fig = plt.figure(figsize=(20, 13))
    for i, s in enumerate(methods):
        plot(s, i, rr, fig)

def plot(qt, index, rr, fig):
    """
    :param fig: plt figure template
    :param qt: QT/QTc data array
    :param index: index to help organizing the figures
    :param rr: RR data array

    Plot heatmaps of QT correction methods
    """
    row = index % 3
    if index > 2: line = 1
    else: line = 0

    # Calculate the fraction of points in healthy-region
    healthy, short, long = 0, 0, 0
    for x in qt:
        if 450 > x > 320: healthy += 1
        elif x >= 450: long += 1
        elif x <= 320: short += 1

    normal = "{:.1f} %".format(healthy * 100 / len(qt))
    lqt = "{:.1f} %".format(long * 100 / len(qt))
    sqt = "{:.1f} %".format(short * 100 / len(qt))

    # Calculate kernel density estimation
    # NOTE: may take some time if dataset is large
    QTcRR = np.vstack((rr, qt))
    z = stats.gaussian_kde(QTcRR)(QTcRR)

    # Sort the "most dense" points on top of the figure
    idx = z.argsort()
    rr, qt, z = rr[idx], qt[idx], z[idx]

    gs = GridSpec(3, 2)
    ax = fig.add_subplot(gs[row, line])
    plt.scatter(rr, qt, c=z, s=5, edgecolors=None)
    plt.axhline(y=450, color='black', linestyle='--')
    plt.axhline(y=320, color='black', linestyle='--')
    plt.title("Normal: "+normal+" ; LQT: "+lqt+" ; SQT "+sqt, fontsize=9)
    plt.xlim(400, 1050)
    plt.ylim(200, 700)
    ax.set_xlabel('RR [ms]', fontsize=10)
    ax.set_ylabel('QTc [ms]', fontsize=10)
    plt.setp(ax.get_xticklabels(), fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)
    plt.text(410, 660, get_text(index), fontsize=9, backgroundcolor='white')
    fig.tight_layout()
    cbar = plt.colorbar()
    cbar.formatter.set_powerlimits((0, 0))
    cbar.ax.set_ylabel("Density", rotation=270, labelpad=10)
    plt.suptitle("*DATASET*, subject *FILENAME*")

def get_text(index):
    if index == 0: return "(a) QT"
    elif index == 1: return "(c) QTc Bazett"
    elif index == 2: return "(e) QTc Framingham"
    elif index == 3: return "(b) TE QTc"
    elif index == 4: return "(d) QTc Fridericia"
    elif index == 5: return "(f) QTc Hodges"

def main():
    # Variable datafile is a path, where the file is stored
    read_data(datafile)
    plt.show()
main()
