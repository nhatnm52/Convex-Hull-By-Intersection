import Point
import matplotlib.pyplot as plt

#Check intersection
def checkIntersect(A, B, C, D):  # ~6, segment vs straight

    # in case: xA = xB or xC = xD
    if A.x == B.x:
        if C.x == D.x:
            return False
        else:
            A2 = (C.y - D.y)/(C.x - D.x)
            b2 = (C.y-C.x*A2)
            yIntersection = A.x*A2 + b2
            if max(A.y, B.y) > yIntersection and min(A.y, B.y) < yIntersection:
                return True
            else:
                return False
    if C.x == D.x:
        if A.x < C.x:
            if B.x > C.x:
                return True
            else:
                return False
        else:
            if B.x > C.x:
                return False
            else:
                return True

    # Range of value x of intersection
    if A.x > B.x:
        minRange = B.x
        maxRange = A.x
    else:
        minRange = A.x
        maxRange = B.x

    # find intersection

    A1 = (A.y - B.y)/(A.x - B.x)
    A2 = (C.y - D.y)/(C.x - D.x)
    if A1 == A2:
        return False
    # x = (b2 - b1)/(a1 - a2)
    xIntersection = ((C.y-C.x*A2)-(A.y-A.x*A1))/(A1 - A2)

    if xIntersection > minRange and xIntersection < maxRange:
        return True
    else:
        return False

#Find 4 landmarks min x, max x, min y, max y
def minMax(points: list):
    # ~ 4n
    minX = points[0].x
    maxX = points[0].x
    minY = points[0].y
    maxY = points[0].y
    min_x = 0
    max_x = 0
    min_y = 0
    max_y = 0
    # min X, max X
    for i in range(1, len(points)):
      if minX > points[i].x:
        minX = points[i].x
        min_x = i
      elif maxX < points[i].x:
        maxX = points[i].x
        max_x = i
      if minY > points[i].y:
        min_y = i
        minY = points[i].y
      elif maxY < points[i].y:
        maxY = points[i].y
        max_y = i
    return min_x, max_x, min_y, max_y

#Processing data
def reduceData(points: list):  # ~ 19n
    minx, maxx, miny, maxy = minMax(points)     # ~3n
    top = points[maxy]
    bot = points[miny]
    left = points[minx]
    right = points[maxx]
    partI = list()  # data between right and top
    partII = list()  # data between top and left
    partIII = list()  # data between left and bot
    partIV = list()  # data between right and bot
    center = Point((top.y+bot.y)/2, (left.x+right.x)/2)
    for i in points:
        cur = i
        if cur.x > top.x:
            if cur.y > right.y:
                if checkIntersect(cur, center, top, right):
                    partI.append(cur)
                    continue
        else:
            if cur.y > left.y:
                if checkIntersect(cur, center, top, left):
                    partII.append(cur)
                    continue                          # ~8
        if cur.x > bot.x:
            if cur.y < right.y:
                if checkIntersect(cur, center, bot, right):
                    partIV.append(cur)
                    continue
        else:
            if cur.y < left.y:
                if checkIntersect(cur, center, bot, left):
                    partIII.append(cur)
                    continue                           # ~8
    partI.append(top)
    partII.append(left)
    partIII.append(bot)
    partIV.append(right)
    return right, top, left, bot, partI, partII, partIII, partIV

#run convex hull

def convexHull(right, top, left, bot, partI: list, partII: list, partIII: list, partIV: list):  #  3 n *(len(path)+1)
    center = Point((top.y+bot.y)/2, (left.x+right.x)/2)
    path = list()
    path. append(right)
    cur: Point = right
    next = partI[0]
    if next.duplicate(top):
      path.append(top)
    while not next.duplicate(top):
        next = top
        for i in partI:
            if checkIntersect(center, i, next, cur):
                next = i
        path.append(next)
        poplist = list()
        for i in range(len(partI)-1):
          if not checkIntersect( partI[i], center, next, top):
            poplist.append(i)
        poplist.reverse()
        for i in poplist:
          partI.pop(i)
        cur = next

    next = partII[0]
    if next.duplicate(left):
      path.append(left)
    while not next.duplicate(left):
        next = left
        for i in partII:
            if checkIntersect(center, i, next, cur):
                next = i
        path.append(next)
        poplist = list()
        for i in range(len(partII)-1):
          if not checkIntersect( partII[i], center, next, left):
            poplist.append(i)
        poplist.reverse()
        for i in poplist:
          partII.pop(i)
        cur = next

    next = partIII[0]
    if next.duplicate(bot):
      path.append(bot)
    while not next.duplicate(bot):
        next = bot
        for i in partIII:
            if checkIntersect(center, i, next, cur):
                next = i
        path.append(next)
        poplist = list()
        for i in range(len(partIII)-1):
          if not checkIntersect( partIII[i], center, next, bot):
            poplist.append(i)
        poplist.reverse()
        for i in poplist:
          partIII.pop(i)
        cur = next

    next = partIV[0]
    if next.duplicate(right):
      path.append(right)
    while not next.duplicate(right):
        next = right
        for i in partIV:
            if checkIntersect(center, i, next, cur):
                next = i
        path.append(next)
        poplist = list()
        for i in range(len(partIV)-1):
          if not checkIntersect( partIV[i], center, next, right):
            poplist.append(i)
        poplist.reverse()
        for i in poplist:
          partIV.pop(i)
        cur = next

    return path

def plot(points, path, right, top, left, bot):
    plt.figure()
    for i in points:
        plt.plot(i.x, i.y, 'ro')
    x = [right.x, top.x, left.x, bot.x, right.x]
    y = [right.y, top.y, left.y, bot.y, right.y]
    plt.plot(x,y)
    xpath = list()
    ypath = list()
    for i in path:
        xpath.append(i.x)
        ypath.append(i.y)
    plt.plot(xpath ,ypath ,'g--')
    plt.show()
    print("Length of convex hull: "+ str(len(path)))
