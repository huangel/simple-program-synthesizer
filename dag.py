# Dag(~η, ηs, ηt, ~ξ, W)
# ~η is a set of nodes containing two distinctly marked source and target nodes ηs, ηt
# ηs source node
# ηt target node
# ~ξ is a set of edges over nodes in ~η that induces a DAG
# W maps each edge in ~ξ to a set of atomic expressions

class DAG():

	# def __init__(self, nodes, source, target, edges, mapping):
		# self.nodes = nodes # list of nodes 
		# self.source = source # one node 
		# self.target = target # one node
		# self.edges = edges #list of tuples (from, to)
		# self.mapping = mapping # tuple --> list of programs 
		# self.graph = {} 
		# for edge in edges:
		# 	if edge[0] not in self.graph:
		# 		self.graph[edge[0]] = {edge[1]:None}
		# 	else:
		# 		if edge[1] not in self.graph[edge[0]]:
		# 			self.graph[edge[0]][edge[1]] = None
		# for key in self.mapping:
		# 	self.graph[key[0]][key[1]] = self.mapping[key]

	def __init__(self, states, alphabet, delta, start, accept):
		# an iterable containing the states of the DFA --> ie the nodes of the DFA
		self.states = set(states)
		# the state at which the DFA begins operation
		self.start = start
		# the state at which the DFA ends
		self.accept = accept
		# an iterable containing the alphabets (ie/ the edges/the programs)
		self.alphabet = set(alphabet)
		# a transition table mapping state to states through alphabet
		self.delta = delta
		# the current state 
		self.current_state = start

	def __str__(self):
		return self.delta

	def find_all_paths_bw(self, start, end, path=[]):
		path = path + [start]
		if start == end:
			return [path]
		paths = []
		for i in self.delta[start]:
			if self.delta[start][i] not in path:
				newpaths = self.find_all_paths_bw(self.delta[start][i], end, path+[i])
				for newpath in newpaths:
					paths.append(newpath)
		return paths

	def getUniquePaths(self):
		hashSet = set()
		for li in self.find_all_paths_bw(self.start, self.accept):
			hashSet.add(tuple(li[1::2]))
		return hashSet

	def copy(self):
		return DAG(self.states, self.alphabet, self.delta, self.start, self.accept)


def intersect(D1, D2):
	start_node = (D1.start, D2.start)
	accept_node = (D1.accept, D2.accept)
	all_alphabets = D1.alphabet.union(D2.alphabet)
	new_delta = {}
	all_states = set()

	for D1key in D1.delta:
		for D2key in D2.delta:
			all_states.add((D1key, D2key))
			new_delta[(D1key, D2key)] = {}
			for D1op in D1.delta[D1key]:
				if D1op in D2.delta[D2key]:
					new_delta[(D1key, D2key)][D1op] = (D1.delta[D1key][D1op], D2.delta[D2key][D1op])
				else:
					new_delta[(D1key, D2key)][D1op] = (D1.delta[D1key][D1op], D2key)

			for D2op in D2.delta[D2key]:
				if D2op in D1.delta[D1key]:
					new_delta[(D1key, D2key)][D2op] = (D1.delta[D1key][D2op], D2.delta[D2key][D2op])
				else:
					new_delta[(D1key, D2key)][D2op] = (D1key, D2.delta[D2key][D2op])
		
	return DAG(all_states, all_alphabets, new_delta, start_node, accept_node)



if __name__ == '__main__':
	states = [0, 1]
	alphabet = ['a', 'b']
	delta = {0:{'a':0, 'b': 1}, 1:{'a': 1, 'b':1}}
	start = 0 
	accept = 1
	dag = DAG(states, alphabet, delta, start, accept)

	states = [0, 1, 2, 3]
	alphabet = ['a', 'b', 'c', 'd', 'e']
	delta = {0:{'a':1, 'b': 1, 'c':0, 'd':3, 'e':2}, 1:{'a':1, 'b': 1, 'c':2, 'd':1, 'e':1}, 2:{'a':2, 'b': 2, 'c': 2, 'd':2, 'e':2}, 3:{'a':3, 'b': 3, 'c': 3, 'd':3, 'e':3}} 
	start = 0 
	accept = 2
	dag2 = DAG(states, alphabet, delta, start, accept)
	# print(dag.printAllPaths(start, accept))
	# print(dag2.getUniquePaths(start, accept))

	combined = intersect(dag, dag2)
	print(combined.getUniquePaths())


