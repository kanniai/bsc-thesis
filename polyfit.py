import pickle
import matplotlib.pyplot as plt
import numpy as np
import sympy as sp

def read_data(file):
    """
    :param file: data file

    Return a plot, where a second order polynomial is fitted in QT value cloud
    """

    with open(file, mode='rb') as f:
        data = pickle.load(f)

    qt, rr = np.nan_to_num(data[0][:, 0]), np.nan_to_num(data[0][:, 1])
    # Sort the arrays based on RR
    rr, qt = (list(t) for t in zip(*sorted(zip(rr, qt))))

    fig, ax = plt.subplots(figsize=(10,5))

    # Plot the polyfit
    coefs = np.polyfit(rr, qt, 2)
    p = np.poly1d(coefs)
    sp.printing.latex(p)
    plt.plot(rr, p(rr), c='black')

    plt.scatter(rr, qt, s=4, color='red', marker='o', label='QT')
    ax.set_xlabel('RR [ms]', fontsize=10)
    ax.set_ylabel('QT [ms]', fontsize=10)
    plt.setp(ax.get_xticklabels(), fontsize=8)
    plt.setp(ax.get_yticklabels(), fontsize=8)
    plt.xlim(350, 1000)
    plt.ylim(250, 600)
    fig.tight_layout()
    plt.legend(loc=2)
    plt.title('*DATASET*: subject *FILENAME*')
    plt.show()

def main():
    # Variable datafile is a path, where the file is stored
    read_data(datafile)
main()
