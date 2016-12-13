
import warnings
warnings.simplefilter("ignore")

import pymice as pm

data = pm.Loader('C57_AB/2012-08-31 11.58.22.zip')
timeline = pm.Timeline('C57_AB/timeline.ini')

import matplotlib.pyplot as plt
import numpy as np

def setUpAxes(ax):
    setUpAxisX(ax)
    setUpAxisY(ax)
    drawReferenceIntervals(ax)
    addLogHistMethod(ax)


def setUpAxisX(ax):
    ax.set_xscale('log')
    ax.set_xlim(0.05, 5000)
    ax.set_xticks([0.1, 1, 10, 100, 1000])
    ax.xaxis.set_ticks_position('bottom')
    ax.xaxis.set_tick_params(direction='out', which='both')


def setUpAxisY(ax):
    ax.set_ylim(0, 70)
    ax.set_yticks([0, 20, 40, 60])
    ax.yaxis.set_ticks_position('left')
    ax.yaxis.set_tick_params(direction='out', which='both')


def drawReferenceIntervals(ax):
    ax.axvline(1, ls=':', color='k')
    ax.axvline(60, ls=':', color='k')
    ax.axvline(3600, ls=':', color='k')


def addLogHistMethod(ax):
    def logHist(self, xs):
        self.hist(xs, bins=np.logspace(-2, 4, 30))

    ax.logHist = logHist.__get__(ax, ax.__class__)


class DecoratedAxes(object):
    def __enter__(self):
        fig, axes = plt.subplots(4, 2, figsize=(13, 8))

        for axRow in axes:
            for ax in axRow:
                setUpAxes(ax)
        
        for i, axRow in enumerate(axes, 1):
            axRow[0].set_ylabel("corner #{}".format(i))
    
        for i, ax in enumerate(axes[0], 1):
            ax.set_title("cage #{}".format(i))

        for axRow in axes[:-1]:
            for ax in axRow:
                ax.set_xticklabels([])
                ax.xaxis.set_ticks_position('none')
                
        for ax in axes[-1]:
            ax.set_xlabel('intervisit interval [s]')
        
        for axRow in axes:
            for ax in axRow[1:]:
                ax.set_yticklabels([])
                ax.yaxis.set_ticks_position('none')
                
        return axes
        
    def __exit__(self, type, value, traceback):
        plt.show()
        #self.__ax.legend(loc='lower right')
        #self.__ax.autoscale_view()
        #self.__fig.autofmt_xdate()

start, end = timeline.getTimeBounds('Place Pref 3 dark')
visits = data.getVisits(start=start, end=end, order='Start')

def getSubsequence(visits, cage, corner):
    return [v for v in visits
            if v.Cage == cage and v.Corner == corner]

def getIntervisitIntervals(visits):
    return [(b.Start - a.End)
            for (a, b) in zip(visits[:-1], visits[1:])]

def toSeconds(intervals):
    return [x.total_seconds() for x in intervals]

with DecoratedAxes() as axes:
    for corner, axRow in enumerate(axes, 1):
        for cage, ax in enumerate(axRow, 1):
            cornerVisits = getSubsequence(visits, cage, corner)
            intervals = getIntervisitIntervals(cornerVisits)
            ax.logHist(toSeconds(intervals))