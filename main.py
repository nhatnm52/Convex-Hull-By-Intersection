import Point
import ConvexHullByIntersection as ch
import random
import time

points = list()
for i in range(1000):
  points.append(Point(random.randint(1,20000),random.randint(1,20000)))

start = time.time()
right, top, left, bot, partI, partII, partIII, partIV = ch.reduceData(points)
path = ch.convexHull(right, top, left, bot, partI, partII, partIII, partIV)

runTime = time.time() - start

print("Run time: "+ str(runTime))
ch.plot(points, path, right, top, left, bot)