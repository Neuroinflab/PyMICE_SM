
import pymice as pm
data = pm.Loader('demo.zip')
visits = data.getVisits(mice=['Jerry'])
firstNps = [v.Nosepokes[0] for v in visits if v.Nosepokes]
sides = [nosepoke.Door for nosepoke in firstNps]
print sides.count('left'), sides.count('right')