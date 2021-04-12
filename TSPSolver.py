#!/usr/bin/python3

from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))




import time
import numpy as np
from TSPClasses import *
import heapq
import itertools
import copy



class TSPSolver:
	def __init__( self, gui_view ):
		self._scenario = None

	def setupWithScenario( self, scenario ):
		self._scenario = scenario


	''' <summary>
		This is the entry point for the default solver
		which just finds a valid random tour.  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of solution, 
		time spent to find solution, number of permutations tried during search, the 
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''
	
	def defaultRandomTour( self, time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		foundTour = False
		count = 0
		bssf = None
		start_time = time.time()
		while not foundTour and time.time()-start_time < time_allowance:
			# create a random permutation
			perm = np.random.permutation( ncities )
			route = []
			# Now build the route using the random permutation
			for i in range( ncities ):
				route.append( cities[ perm[i] ] )
			bssf = TSPSolution(route)
			count += 1
			if bssf.cost < np.inf:
				# Found a valid route
				foundTour = True
		end_time = time.time()
		results['cost'] = bssf.cost if foundTour else math.inf
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results


	''' <summary>
		This is the entry point for the greedy solver, which you must implement for 
		the group project (but it is probably a good idea to just do it for the branch-and
		bound project as a way to get your feet wet).  Note this could be used to find your
		initial BSSF.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found, the best
		solution found, and three null values for fields not used for this 
		algorithm</returns> 
	'''

	# total time complexity: O(n^3)
	# total space: O(n) because our list cities stores n cities
	def greedy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		ncities = len(cities)
		bssf = None
		count = 0
		start_time = time.time()

		# O(n) time
		# getPath is called n times and takes O(n^2) times resulting in total complexity of O(n^3)
		for city in cities:
			tempTuple = self.getPath(city,cities)
			tempCost = TSPSolution(tempTuple[0])
			if bssf == None or bssf.cost > tempCost.cost:
				bssf = tempCost
				count = tempTuple[1]
		
		end_time = time.time()
		results['cost'] = bssf.cost 
		results['time'] = end_time - start_time
		results['count'] = count
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None

		return results

		pass

	# runs in O(n^2) time (see while loop for more information)
	# space complexity: O(n) because unvisited, visited, and routes hold n objects. This results in
	# O(3n) space which simplifies to O(n).
	def getPath(self, startCity, cities):
		currCity = startCity
		unvisitied = []
		for unv in cities:
			unvisitied.append(unv)
		visited = []
		routes = []
		count = 0
		unvisitied.remove(currCity)
		visited.append(currCity)
		routes.append(currCity)

		#this loop runs n times
		while len(unvisitied) != 0:
			#  findClosestCity() runs n times, and each time takes n time.
			currCity = self.findClosestCity(currCity,unvisitied,routes,visited)	
			count += 1

		return [routes, count]

	# runs in O(n)
	# space complexity: O(n) because unvisited, visited, and routes hold n objects. This results in
	# O(3n) space which simplifies to O(n).
	def findClosestCity(self,currCity,unvisitied,routes,visited):
		if len(unvisitied) == 1:
			minCity = unvisitied[0]
			routes.append(minCity)
			visited.append(minCity)
			unvisitied.remove(minCity)
			return minCity

		#Find closest city
		minCost = 999999999999999
		minCity = None

		#This loop runs n times
		for city in unvisitied:
			if currCity.costTo(city) < minCost:
				minCity = city
				minCost = currCity.costTo(city)

		routes.append(minCity)
		visited.append(minCity)
		if len(unvisitied) == 1:
			unvisitied = []
		else:
			unvisitied.remove(minCity)
		return minCity

	
	
	''' <summary>
		This is the entry point for the branch-and-bound algorithm that you will implement
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number solutions found during search (does
		not include the initial BSSF), the best solution found, and three more ints: 
		max queue size, total number of states created, and number of pruned states.</returns> 
	'''
		
	def branchAndBound( self, time_allowance=60.0 ):
		pass

	''' <summary>
		This is the entry point for the algorithm you'll write for your group project.
		</summary>
		<returns>results dictionary for GUI that contains three ints: cost of best solution, 
		time spent to find best solution, total number of solutions found during search, the 
		best solution found.  You may use the other three field however you like.
		algorithm</returns> 
	'''

	# total time complexity: O(2n^2) which simplifies down to O(n^2)
	# space complexity: O(2n^2) which simplifies down to O(n^2)
	def fancy( self,time_allowance=60.0 ):
		results = {}
		cities = self._scenario.getCities()
		bssf = None
		count = 0
		start_time = time.time()

		#O(n) space (doesn't affect overall space)
		distances = []

		# this nested for loop runs in O(n^2) time
		for city in cities:
			tempDist = []
			for city2 in cities:
				if city == city2:
					tempDist.append(math.inf)
					continue
				tempDist.append(city.costTo(city2))
			distances.append(tempDist)

		# DPTSP is O(n^2) time and space
		optimalPath, optimalCost = self.DPTSP(distances)
		
		routes = []
		for city in optimalPath:
			routes.append(cities[city])

		bssf = TSPSolution(routes)

		end_time = time.time()
		results['cost'] = optimalCost
		results['time'] = end_time - start_time
		results['count'] = 5
		results['soln'] = bssf
		results['max'] = None
		results['total'] = None
		results['pruned'] = None
		return results

	# total time complexity: O(2n^2) which simplifies down to O(n^2)
	# space complexity: O(2n^2) which simplifies down to O(n^2)
	def DPTSP(self,distances):
		n = len(distances)
		totalCities = set(range(n))

		# creating an nxn table below so space is O(n^2)
		dpTable = {(tuple([i]), i): tuple([0, None]) for i in range(n)}
		queue = [(tuple([i]), i) for i in range(n)]

		# for loop below runs O(n) times inside our while loop which runs O(n) times as well. Thus we
		# have a total time complexity of O(n^2)
		while queue: # Iterate through untile queue is empty
			prevVisited, prevLastPoint = queue.pop(0)
			prevDist, _ = dpTable[(prevVisited, prevLastPoint)]
			toVisit = totalCities.difference(set(prevVisited))
			for newLastPoint in toVisit:
				newVisited = tuple(sorted(list(prevVisited) + [newLastPoint]))
				newDist = (prevDist + distances[prevLastPoint][newLastPoint])
				if (newVisited, newLastPoint) not in dpTable:
					dpTable[(newVisited, newLastPoint)] = (newDist, prevLastPoint)
					queue += [(newVisited, newLastPoint)]
				else:
					if newDist < dpTable[(newVisited, newLastPoint)][0]:
						dpTable[(newVisited, newLastPoint)] = (newDist, prevLastPoint)

		# retracing optimal path also costs O(n^2) time and space
		optimalPath, optimalCost = self.retracingOptimalPath(dpTable, n)
		return optimalPath, optimalCost

	# time complexity: O(n^2) because we iterate through the entire table, an nxn matrix
	# space complexity: O(n^2) because we are storing an nxn table
	def retracingOptimalPath(self, dpTable, n):

		# for loop below runs in O(n) time
		citiesToRetrace = tuple(range(n))
		fullPath = dict((k,v) for k,v in dpTable.items() 
						if k[0] == citiesToRetrace)
		pathKey = min(fullPath.keys(), key=lambda x : fullPath[x][0])

		lastCity = pathKey[1]
		optimalCost, nextToLastCity = dpTable[pathKey]
		optimalPath = [lastCity]
		
		citiesToRetrace = tuple(sorted(set(citiesToRetrace).difference({lastCity})))

		# this while loop is O(n^2) because it goes through every element in our dynamic
		#programming table
		while nextToLastCity is not None:
			
			lastCity = nextToLastCity
			pathKey = (citiesToRetrace,lastCity)
			_, nextToLastCity = dpTable[pathKey]
		
			optimalPath = [lastCity] + optimalPath
			citiesToRetrace = tuple(sorted(set(citiesToRetrace).difference({lastCity})))

		return optimalPath, optimalCost

		



