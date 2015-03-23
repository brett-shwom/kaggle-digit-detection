import matplotlib
import numpy
import csv
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
import itertools
from operator import itemgetter
import pylab

def drawVerticalLineThroughCenterAndCountIntersections(m):
	centerColumn = m.shape[1] / 2
	#print (m == 255).sum(axis=0)
	return (m == 255).sum(axis=0)[centerColumn]

def drawHorizontallLineThroughCenterAndCountIntersections(m):
	centerRow = m.shape[1] / 2
	#print (m == 255).sum(axis=0)
	return (m == 255).sum(axis=0)[centerRow]

def paint(m,start):
	toVisit = [start]
	while len(toVisit) > 0:
		p = toVisit.pop()
		row = p[0]
		col = p[1]
		if m[row,col] != 0:
			continue
		m[row,col] = 128
		if row + 1 < m.shape[0]:
			toVisit.append((row+1, col))
		if row - 1 >= 0:
			toVisit.append((row-1, col))
		if col + 1 < m.shape[1]:
			toVisit.append((row, col+1))
		if col - 1 >= 0:
			toVisit.append((row, col-1))
	return m

def paintUnboundedArea(m):
	#find a place on the periphery to start painting
	(i,j) = (0,0)
	starts = []
	directions = [(0,1,m.shape[1]-2), (1,0,m.shape[0]-2),(0,-1,m.shape[1]-2),(-1,0,m.shape[0]-2)]
	while len(directions) > 0:
		# print i,j,directions[0]
		# print m[i,j], m[i,j] == 0
		if m[i,j] == 0:
			# print "setting start"
			starts.append((i,j))
		(i,j) = (directions[0][0] + i, directions[0][1] + j)
		if directions[0][2] is 0:
			directions.pop(0)
		else:
			directions[0] = (directions[0][0], directions[0][1], directions[0][2]-1)
	while len(starts) > 0:
		m = paint(m,starts.pop())
	return m
	

# paintUnboundedArea(numpy.asmatrix([1,0,1,1,0,1]).reshape(2,3))


def removeMargins(m):
	threshold = 10
	m = numpy.delete(m,numpy.nonzero(m.sum(axis=0) <= threshold),axis=1)
	m = numpy.delete(m,numpy.nonzero(m.sum(axis=1) <= threshold),axis=0)
	return m

data = [(nimg[0], nimg[1:]) for nimg in [map(int, img) for img in map(list, csv.reader(open('train.csv')))[1:]]]


proportions = []
intersectionCounts = []

for label, datapoint in data:
	m = numpy.asmatrix(numpy.array(datapoint, dtype=numpy.uint8).reshape((28,28)))
	edgesDetected = cv2.Canny(m,100,100)
	#TODO: probably need to normalize rotation of image
	edgesDetected = removeMargins(edgesDetected)
	unboundedAreaPainted = paintUnboundedArea(edgesDetected)
	perimeter = (edgesDetected > 0).sum()
	unboundedArea = (unboundedAreaPainted == 128).sum()
	perimeterProportion = perimeter / float(unboundedArea) #/ float(edgesDetected.shape[0] * edgesDetected.shape[1])
	proportions.append((1/perimeterProportion,label))
	intersectionCount = drawHorizontallLineThroughCenterAndCountIntersections(edgesDetected)
	intersectionCounts.append((intersectionCount,label))


proportionsGroupedByKey = [map(lambda i: i[0], list(items)) for key, items in itertools.groupby(sorted(proportions, key=itemgetter(1)), itemgetter(1))]
pylab.boxplot(proportionsGroupedByKey[0])

intersectionCountsGroupedByKey = [map(lambda i: i[0], list(items)) for key, items in itertools.groupby(sorted(intersectionCounts, key=itemgetter(1)), itemgetter(1))]
pylab.boxplot(intersectionCountsGroupedByKey)
	
	# plt.matshow(edgesDetected)

plt.ion()
plt.plot(map(lambda d:d[0], proportions), map(lambda d:d[1], proportions),  'o', linestyle='None')

# proportions.sort()
# print proportions

#datapoint = numpy.asmatrix(numpy.array(datapoint, dtype=numpy.float32).reshape((28,28)))

	# datapoint = numpy.asmatrix(numpy.array(datapoint, dtype=numpy.uint8).reshape((28,28)))
	# edgesDetected = cv2.Canny(datapoint,100,100)
	# edgesDetected = removeMargins(edgesDetected)

	# plt.ion()
	# plt.matshow(edgesDetected)





# plt.show()

#numpy.multiply(numpy.asmatrix(numpy.array([1,1,2,2], dtype=numpy.float32).reshape(2,2)),1/255.0)