"""Compute the intrinsic population of objects needed to give 1 detection in a given survey"""

# Take LF as uniform alpha=0.8.  As we have no dependence on angle
# (only thinking about flux bias here) we can asign a single value to
# Om, om, M, i are random.  a and q are distributed on 1 au grid
# between 150-1500au and 30 and 90 au respectively

import ephem
import numpy
from matplotlib import pyplot
import aq_figure1
import os
import sys

kbo=ephem.EllipticalBody()


def _mag(a, q, M, H):
    kbo.name = "test"
    kbo._epoch_M=(2018, 10, 1)
    kbo._inc=0
    kbo._Om=0
    kbo._om=0
    kbo._epoch='2018/10/01'
    kbo._G=0.15
    kbo._M=M
    kbo._e=1.0-(q/a)
    kbo._a=a
    kbo._H=H
    kbo.compute(ephem.date('2018/10/01'))
    return kbo.mag

def mag(d, H):
    return 2.5*numpy.log10(d**4) + H

def limit(d, mag=24.0):
    return mag - 2.5*numpy.log10(d**4)

a = numpy.arange(150., 1500., 150.)
q = numpy.arange(30., 91., 10.)
H_limit = limit(q)
M = numpy.arange(0., 360., 0.01)
H_0 = limit(30)

scale = None
for i in q:
    H = limit(i)
    for k in a:
        for j in M:
            if _mag(k, i, j, H) > 24.5:
                break
        N = 10**(-0.5*(H-H_0))*360./j
        if scale is None:
            scale = N
        pyplot.text(k, i, "{:.0f}".format(N/scale), 
                    horizontalalignment='center',
                    verticalalignment='center')

aq_figure1.plot_data()
aq_figure1.plot_features()
aq_figure1.plot_axis()

pyplot.xlim(50,1550)
pyplot.ylim(25, 95)


plot_file =  "{}.pdf".format(os.path.splitext(sys.argv[0])[0])
pyplot.savefig(plot_file)

