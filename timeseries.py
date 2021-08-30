import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import pearsonr
import pickle
from statistics import mean

def read_data(file, start=13000, total_value=600000):
    """
    :param total_value: how long segment is selected [ms]
    :param file: data file
    :param start: starting index along the time series

    Read ECG data and plot time series of given segment
    """
    with open(file, mode='rb') as f:
        data = pickle.load(f)

    rr = data[0][:, 1]

    time, total, j = [], 0, 0
    for i in rr[start:]:
        total += i
        time.append(total*10**(-3))
        j += 1
        if total > total_value: break
    end = start+j

    # Separate the columns
    qt, rr, qtc = data[0][:, 0][start:end], data[0][:, 1][start:end], data[0][:, 2][start:end]

    # Pearson's correlation
    corr, _ = pearsonr(rr, qt)
    print("Pearson:", corr)

    # Normalized cross correlation
    qt_n = (qt-np.mean(qt)) / (np.std(qt))
    rr_n = (rr-np.mean(rr)) / (np.std(rr))

    print("Normalized cross correlation:", np.correlate((rr/np.linalg.norm(rr)), (qt/np.linalg.norm(qt))))
    print("Cross correlation:", np.correlate(qt_n, rr_n))

    _, ax = plt.subplots(figsize=(15,6))

    red = ax.plot(time, rr, 'red', label='RR', linewidth=1)
    blue = ax.plot(time, qt, 'dodgerblue', label='QT', linewidth=1)
    mean_rr = plt.axhline(mean(rr), color='black', linestyle="dashed")
    mean_qt = plt.axhline(mean(qt), color='black', linestyle="dotted")
    ax.set_xlabel('Time [s]', fontsize=9)
    ax.set_ylabel('Interval duration [ms]', fontsize=9)
    ax.set_xlim(0, total_value/1000)
    ax.set_ylim(250, 1000)
    plt.xticks(fontsize=20)
    plt.yticks(fontsize=20)
    plt.setp(ax.get_xticklabels(), fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)

    ax.legend([red[0], blue[0], mean_rr, mean_qt],
               ["RR", "QT", r'$\mu_{\mathrm{RR}}$', r'$\mu_{\mathrm{QT}}$'],
               loc=2)
    plt.show()

def main():
    # Variable datafile is a path, where the file is stored
    read_data(datafile)
main()
