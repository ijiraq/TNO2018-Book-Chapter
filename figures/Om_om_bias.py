"""Compute the intrinsic population of objects needed to give 1 detection in a given survey"""

# Take LF as uniform alpha=0.8.  As we have no dependence on angle
# (only thinking about flux bias here) we can asign a single value to
# Om, om, M, i are random.  a and q are distributed on 1 au grid
# between 150-1500au and 30 and 90 au respectively

import ephem
import numpy
import aq_figure1
import os
import sys
from matplotlib import pyplot
from astropy import table
import numpy as np

data = table.Table.read('mpcread.dat', format='ascii')

data['M'] = np.degrees(data['M'])
data['Om'] = np.degrees(data['Om'])
data['om'] = np.degrees(data['om'])
data['i'] = np.degrees(data['i'])
data['q'] = data['a'] * ( 1 - data['e'])


cond = data['a'] > 150
pyplot.plot(data['Om'][cond][:6], data['om'][cond][:6], 'o', ms=5, alpha=0.5)
pyplot.plot(data['Om'][cond][6:12], data['om'][cond][6:12], 'o', ms=5, alpha=0.5)
pyplot.plot(data['Om'][cond][12:], data['om'][cond][12:], 'o', ms=5, alpha=0.5)
pyplot.xlabel('Node Angle (deg)')
pyplot.ylabel('Argument of pericentre (deg)')
pyplot.xlim(0, 360)
pyplot.ylim(0, 360)

mag_limit = 24.0

class KBO(ephem.EllipticalBody):
    
    def __init__(self, orbit):
        print orbit
        super(KBO, self).__init__()
        self.name = orbit['kbo.name']
        self._a = orbit['a']
        self._M = orbit['M']
        self._e = orbit['e']
        self._inc = orbit['i']
        self._Om = orbit['Om']
        self._om = orbit['om']
        self._H = orbit['kbo._H']
        self._epoch_M = orbit['kbo._epoch_M']
        self._epoch = orbit['kbo._epoch']

def kbo(a, q, Om, om, inc, M, H):
    kbo=ephem.EllipticalBody()
    kbo.name = "test"
    kbo._epoch_M=(2018, 10, 1)
    kbo._inc=inc
    kbo._Om=Om
    kbo._om=om
    kbo._epoch=42980.5
    kbo._G=0.15
    kbo._M=M
    kbo._e=1.0-(q/a)
    kbo._a=a
    kbo._H=H
    kbo.compute(kbo._epoch)
    return kbo

def mag(d, H):
    return 2.5*numpy.log10(d**4) + H

def limit(d, mag=mag_limit):
    return mag - 2.5*numpy.log10(d**4)


opp_lon = {'Jan': 100,
           'Feb': 130,
           'Mar': 160,
           'Apr': 190,
           'May': 250,
           'Jun': 277,
           'Jul': 305,
           'Aug': 335,
           'Sep': 5,
           'Oct': 35,
           'Nov': 64,
           'Dec': 95}

i = 20.
a = 250.
q = 40.
H = limit(45.)

scale = None
for Om in numpy.arange(5, 361, 45):
    for om in numpy.arange(5, 361, 45):
        number_detected = 0
        for i in data[cond]['i']:
            a = numpy.random.choice(data[cond]['a'])
            q = numpy.random.choice(data[cond]['q'])
            i = numpy.random.choice(data[cond]['i'])
            for M in numpy.arange(0, 361, 1):
                k = kbo(a, q, Om, om, i, M, H)
                if k.mag < mag_limit+0.5:
                    if ((-np.radians(10) > k.hlat > -np.radians(15) and np.radians(opp_lon['Mar']) > k.hlon > np.radians(opp_lon['Jan'])) 
                        or (-np.radians(10) > k.hlat > -np.radians(15) and np.radians(opp_lon['Dec']) > k.hlon > np.radians(opp_lon['Sep'])) 
                        # or (np.radians(10) < k.hlat < np.radians(15) and np.radians(opp_lon['Jul']) > k.hlon > np.radians(opp_lon['Apr'])) 
                        # or (np.radians(5) < k.hlat < np.radians(15) and np.radians(opp_lon['Sep']) < k.hlon < np.radians(opp_lon['Nov']))
                        ): 
                        number_detected += 1
        if not number_detected > 0:
            continue
        pyplot.text(Om, om, "{:.0f}".format(number_detected), 
                    horizontalalignment='center',
                    verticalalignment='center')



plot_file =  "{}.pdf".format(os.path.splitext(sys.argv[0])[0])
pyplot.savefig(plot_file)

