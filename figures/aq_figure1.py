from matplotlib import pyplot
from astropy import table
import numpy as np
import sys
import os


def plot_data():

    data = table.Table.read('mpcread.dat', format='ascii')


    data['q'] = data['a'] * ( 1 - data['e'])
    cond = data['a'] > 150
    pyplot.plot(data['a'][cond], data['q'][cond], 'o', ms=5, alpha=0.5)

def plot_axis():
    pyplot.xlabel('semi-major axis (au)')
    pyplot.ylabel('pericentre distance (au)')

def plot_features():
    # Appriximate outward diffusion bounary.
    a = np.arange(100,2000)
    q = 41 + 3.5 * np.log10(a/100.)
    pyplot.plot(a, q, 'k--', alpha=0.5)

    # Approximate inward diffusion boundary.
    q += 8 
    pyplot.plot(a, q, 'k-.', alpha=0.5)

    a = [1000,1000]
    q = [30,90]
    pyplot.plot(a, q, 'k-', alpha=0.5)

if __name__ == '__main__':

    plot_data()
    plot_axis()
    plot_features()

    plot_file =  "{}.pdf".format(os.path.splitext(sys.argv[0])[0])
    
    pyplot.savefig(plot_file)

