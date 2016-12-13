
import warnings
warnings.simplefilter("ignore")

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import matplotlib.dates as mpd
import pytz

import pymice as pm

data = pm.Loader('C57_AB/2012-08-31 11.58.22.zip')
timeline = pm.Timeline('C57_AB/timeline.ini')

PHASES = ['NPA 2 dark', 'NPA 2 light',
          'Place Pref 1 dark', 'Place Pref 1 light',
          'Place Pref 2 dark', 'Place Pref 2 light',
          'Place Pref 3 dark', 'Place Pref 3 light']

def getGroupPerformanceMatrix(groupName):
    group = data.getGroup(groupName)
    return [getPerformanceCurve(mouse) for mouse in group.Animals]

def getPerformanceCurve(mouse):
    return [getPerformance(mouse, phase) for phase in PHASES]

def getPerformance(mouse, phase):
    start, end = timeline.getTimeBounds(phase)
    visits = data.getVisits(mice=[mouse], start=start, end=end)
    return  calculatePerformance(visits)

def calculatePerformance(visits):
    successes = [isToCorrectCorner(v) for v in visits]
    return successRatio(successes)

def isToCorrectCorner(visit):
    return visit.CornerCondition > 0

def successRatio(successes):
    return np.mean(successes)

def getTimeBounds(phases):
    return mpd.date2num(timeline.getTimeBounds(phases))

class DecoratedAxes(object):
    yticks = range(0, 80, 10)

    def __enter__(self):
        self.init()
        return self.__ax

    def init(self):
        fig, ax = plt.subplots(figsize=(13, 8))

        ax.set_title('C57BL/6 - PLACE PREFERENCE LEARNING')

        self.__ax = ax
        self.__fig = fig
        self.__setUpAxisY()
        self.__setUpAxisX()
        self.__plotDarkPhasesInBackground()
        self.__plotPercentReferenceLines()
        
        ax.plotGroupAverages = plotGroupAverages.__get__(ax, ax.__class__)

    def __setUpAxisY(self):
        self.__ax.set_ylabel('% of visits to sugar corner')
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
        self.__ax.xaxis.set_major_formatter(timeline)

    def __plotPercentReferenceLines(self):
        for y in self.yticks:
            self.__ax.axhline(y, color='#A0A0A0', lw=1)

    def __plotDarkPhasesInBackground(self):
        for phase in PHASES:
            if phase.endswith('dark'):
                start, end = getTimeBounds(phase)
                self.__ax.axvspan(start, end, color='#E0E0E0')

        
    def __exit__(self, type, value, traceback):
        self.finish()

    def finish(self):
        self.__ax.legend(loc='lower right')
        self.__ax.autoscale_view()
        self.__fig.autofmt_xdate()
        plt.show()
    
def getPhaseMidtime(phase):
    return getTimeBounds(phase).mean()

def getSem(X):
    return X.std(axis=0) / np.sqrt(np.logical_not(X.mask).sum(axis=0))
  
GRUOP_COLORS = {'C57 A': '#00c0ff',
                'C57 B': '#00aa00'}

# Although it is a good practice to plot error bars as confidence
# intervals instead of SEM\cite{Cumming2014newStat} we decided to
# reproduce the original plot as close as possible.
def plotGroupAverages(ax, series, group):
    masked = np.ma.masked_invalid(series)
    mean = masked.mean(axis=0)
    sem = getSem(masked)
    midpoints = [getPhaseMidtime(phase) for phase in PHASES]
    color = GRUOP_COLORS[group]
    ax.errorbar(midpoints, mean * 100, yerr=sem * 100,
                linewidth=3, elinewidth=2,
                marker='o', markeredgecolor=color,
                markersize=10,
                ecolor="black",
                color=color, linestyle='--',
                dash_capstyle='round',
                label=group,
                alpha=0.69)

with DecoratedAxes() as ax:
    for group in ['C57 A', 'C57 B']:
        performance = getGroupPerformanceMatrix(group)
        ax.plotGroupAverages(performance, group)