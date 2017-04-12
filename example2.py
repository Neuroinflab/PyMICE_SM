
import warnings
warnings.simplefilter("ignore")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mpd
import pytz

import pymice as pm

data = pm.Loader('FVB/2016-07-20 10.11.11.zip')

timeline = pm.Timeline('FVB/timeline.ini')

PHASES = ['PP dark',     'PP light',
          'DISC 1 dark', 'DISC 1 light',
          'DISC 2 dark', 'DISC 2 light',
          'DISC 3 dark', 'DISC 3 light',
          'DISC 4 dark', 'DISC 4 light',
          'DISC 5 dark', 'DISC 5 light']

def getPerformanceMatrix():
    return [getPerformanceCurve(mouse) for mouse in data.getMice()]

def getPerformanceCurve(mouse):
    return [getPerformance(mouse, phase) for phase in PHASES]

def getPerformance(mouse, phase):
    start, end = timeline.getTimeBounds(phase)
    visits = data.getVisits(mice=[mouse], start=start, end=end)
    accessibleCornerVisits = filter(isToCorrectCorner, visits)
    return calculatePerformance(accessibleCornerVisits)

def isToCorrectCorner(visit):
    return visit.CornerCondition > 0

def calculatePerformance(visits):
    firstNps = [v.Nosepokes[0] for v in visits if v.Nosepokes]
    successes = [isToCorrectSide(nosepoke) for nosepoke in firstNps]
    return successRatio(successes)

def isToCorrectSide(nosepoke):
    return nosepoke.SideCondition > 0

def successRatio(successes):
    return np.mean(successes)

def getTimeBounds(phases):
  return mpd.date2num(timeline.getTimeBounds(phases))

class DecoratedAxes(object):
    yticks = range(0, 110, 10)

    def __enter__(self):
        fig, ax = plt.subplots(figsize=(13, 8))

        #ax.set_title('C57BL/6 - PLACE PREFERENCE LEARNING')

        self.__ax = ax
        self.__fig = fig
        self.__setUpAxisY()
        self.__setUpAxisX()
        self.__plotDarkPhasesInBackground()
        self.__plotPercentReferenceLines()
        
        ax.plotGroupAverages = plotGroupAverages.__get__(ax, ax.__class__)
        return ax

    def __setUpAxisY(self):
        self.__ax.set_ylabel('% of correct responses')
        self.__ax.set_ylim(min(self.yticks), max(self.yticks))
        self.__ax.yaxis.set_ticks_position('none')
        self.__ax.yaxis.set_major_formatter(mtick.FormatStrFormatter("%.0f%%"))
        self.__ax.set_yticks(self.yticks)
        

    def __setUpAxisX(self):
        tzone = pytz.timezone('CET')
        hours=[7, 19]

        self.__ax.set_xlabel('experiment phase')
        self.__ax.set_xlim(getTimeBounds(PHASES))
        self.__ax.xaxis.set_major_locator(mpd.HourLocator(np.array(hours),tz=tzone))
        self.__ax.xaxis.set_ticks_position('none')

    def __plotPercentReferenceLines(self):
        for y in self.yticks:
            self.__ax.axhline(y, color='#A0A0A0', lw=1)

    def __plotDarkPhasesInBackground(self):
        for phase in PHASES:
            if phase.endswith('dark'):
                start, end = getTimeBounds(phase)
                self.__ax.axvspan(start, end, color='#E0E0E0')

        
    def __exit__(self, type, value, traceback):
        self.__ax.autoscale_view()
        self.__fig.autofmt_xdate()
        plt.show()
    
def getPhaseMidtime(phase):
    return getTimeBounds(phase).mean()

def getSEM(X):
    return X.std(axis=0) / np.sqrt(np.logical_not(X.mask).sum(axis=0))

def getCI95(X):
    return 1.96 * getSEM(X)
  
# It is a good practice to plot error bars as confidence intervals instead of
# SEM\cite{Cumming2014newStat}
def plotGroupAverages(ax, series):
    masked = np.ma.masked_invalid(series)
    mean = masked.mean(axis=0)
    error = getSEM(masked) # Reviewer pointed inconsistency of CI95 with example #3
    midpoints = [getPhaseMidtime(phase) for phase in PHASES]
    ax.errorbar(midpoints, mean * 100, yerr=error * 100,
                linewidth=3, elinewidth=2,
                marker='o', markeredgecolor="blue",
                markersize=10,
                ecolor="black",
                color="blue", linestyle='--',
                dash_capstyle='round',
                alpha=0.69)


with DecoratedAxes() as ax:
    ax.xaxis.set_major_formatter(timeline)
    
    performance = getPerformanceMatrix()
    ax.plotGroupAverages(performance)