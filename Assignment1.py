import heapq

#%%
class Edge(object):
	def __init__(self,weight,endNode):
		self.weight = float(weight)
		self.endNode = endNode
#%%
class Node(object):

	def __init__(self,name):
		self.name = name
		self.connected_to = []
		self.parent = None
		self.cost = float('inf')
		self.wcost = float('inf')
		self.weight = 0
	
	def __cmp__(self,otherVertex):
		if self.cost < otherVertex.cost:
			return -1
		elif self.cost > otherVertex.cost:
			return 1
		else:
			return 0
    
	def __lt__(self,other):
		selfPriority = self.cost
		otherPriority = other.cost
		return selfPriority < otherPriority
	
	def __eq__(self, other):
		return self.name == other.name

	def __str__(self):
		return self.name
#%%
class Algo(object):

	def UniformCostSearch(self,Graph,startNode,targetNode):
		ref = {}
		explored = []
		fringe = []
		heapq.heappush(fringe, startVertex)
		ref[str(startNode)] = startNode
		startNode.cost = 0
		count = 0
		while fringe:
			#print("\n\n*******************************************\n")
			#print("\nLoop number: ",count)#
			#print("Fringe:")#
			self.displayFringe(fringe)#
			#print("\nExplored:")#
			self.displayExplored(explored)#
			currentNode = heapq.heappop(fringe)#pop minimum cost
			count = count + 1#
			#print("\ncurrent node: ",currentNode.name)
			del ref[str(currentNode)]
			if currentNode not in explored:
				explored.append(currentNode)
			if currentNode == targetNode:
				break	
			for edge in currentNode.connected_to:
				child = edge.endNode			
				new_cost = currentNode.cost + edge.weight
				if child not in explored and child not in fringe:
					child.cost = new_cost
					child.parent = currentNode
					child.weight = edge.weight
					ref[str(child)] = child
					heapq.heappush(fringe, child)
				elif child in fringe and ref[str(child)].cost > new_cost:
					child.cost = new_cost
					#print("\nchildName:%s-> fringe:%d, new %d" %(child.name,ref[str(child)].cost,child.cost))
					#print("name: "+child.name+" child: "+str(child.cost)+"ref: "+str(ref[str(child)].cost))
					ref[str(child)].cost = child.cost
					ref[str(child)].parent=currentNode
					ref[str(child)].weight = edge.weight
			
		print("\n\nnodes expanded: %d" %(count))
		
	def AStarSearch(self,Graph,startNode,targetNode,huristic):
		ref = {}
		explored = []
		fringe = []
		heapq.heappush(fringe, startVertex)
		ref[str(startNode)] = startNode
		startNode.cost = 0
		startNode.wcost = 0
		count = 0
		while fringe:
			#print("\n\nLoop number: ",count)#
			#print("Fringe:")#
			#self.displayFringe(fringe)#
			#print("\nExplored:")#
			#self.displayExplored(explored)#
			currentNode = heapq.heappop(fringe)#pop minimum cost
			count = count + 1#
			#print("\ncurrent node: ",currentNode.name)
			del ref[str(currentNode)]
			if currentNode not in explored:
				explored.append(currentNode)
			if currentNode == targetNode:
				break	
			for edge in currentNode.connected_to:
				child = edge.endNode		
				new_cost = currentNode.wcost + edge.weight
				#print('connected to %s,%s'%(child.name,str(new_cost)))
				if child not in explored and child not in fringe:
					child.cost = new_cost+huristic[str(child)]
					child.wcost = new_cost
					child.parent = currentNode
					child.weight = edge.weight
					ref[str(child)] = child
					heapq.heappush(fringe, child)
				elif child in fringe and (ref[str(child)].cost) > (new_cost+huristic[str(child)]):
					child.cost = new_cost
					child.wcost = new_cost
					ref[str(child)].cost = child.cost
					ref[str(child)].parent=currentNode
					ref[str(child)].weight = edge.weight
			
		print("\nnodes expanded: %d" %(count))
	def displayFringe(self,fringe):
		for node in fringe:
			print(str(node)+": "+str(node.cost), end=" ")
	def displayExplored(self,explored):
		for node in explored:
			print(str(node)+": "+str(node.cost), end=" ")
		
	def getShortestPath(self,targetVertex):
		
		if(targetVertex.cost == float('inf')):
			print("distance: infinity\nroute:\nnone")
		else:
			print ("distance: %.1f km" %(targetVertex.cost))
			print ("route: ")
			node = targetVertex
			routes = []
			while node is not None:
				if node.parent:
					routes.append("%s to %s, %.1f km" % (node.parent.name,node.name,node.weight))
				node = node.parent
			for route in routes[::-1]:
				print(route)
			
#%%
#read file
file = open("input1.txt", "r") 
inputs = []
huristic={}
for x in file:   
	if "END OF INPUT" not in x:
		inputs.append(x.replace('\n','').split(' '))
	else:
		break
	
file = open("h_kassel.txt", "r") 
for x in file:   
	if "END OF INPUT" not in x:
		temp = x.replace('\n','').split(' ')
		huristic[temp[0]] = float(temp[1])
	else:
		break
	
#create vertex
vertexList = {}
for x in inputs:
	vertexList[x[0]] = Node(x[0])
	vertexList[x[1]] = Node(x[1])
	
#create edge and add to vertex
for x in inputs:
	vertexList[x[0]].connected_to.append(Edge(x[2], vertexList[x[1]]))
	vertexList[x[1]].connected_to.append(Edge(x[2], vertexList[x[0]]))

startVertex = vertexList["Bremen"]
targetVertex = vertexList["Kassel"]
algo = Algo()
#algo.UniformCostSearch(vertexList, startVertex,targetVertex)
algo.AStarSearch(vertexList, startVertex,targetVertex,huristic)
algo.getShortestPath(targetVertex)