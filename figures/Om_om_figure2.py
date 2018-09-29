from matplotlib import pyplot
from astropy import table
import numpy as np

data = table.Table.read('mpcread.dat', format='ascii')


data['q'] = data['a'] * ( 1 - data['e'])
cond = data['a'] > 150
pyplot.plot(np.degrees(data['Om'][cond]), np.degrees(data['om'][cond]), 'o', ms=5, alpha=0.5)
pyplot.xlabel('Node Angle (deg)')
pyplot.ylabel('Argument of pericentre (deg)')
pyplot.savefig('Om_om_figure2.pdf')

