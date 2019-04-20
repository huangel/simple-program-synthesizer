class DAG():

	def __init__(self, states, delta, start, accept):
		# an iterable containing the states of the DFA --> ie the nodes of the DFA
		self.states = set(states)
		# the state at which the DFA begins operation
		self.start = start
		# the state at which the DFA ends
		self.accept = accept
		# an iterable containing the alphabets (ie/ the edges/the programs)
		# self.alphabet = set(alphabet)
		# a transition table mapping state to states through alphabet
		self.delta = delta
		# the current state 
		self.current_state = start

	def __str__(self):
		return str(self.delta)

	def find_all_paths_bw(self, start, end, path=[]):
		path = path + [start]
		if start == end:
			return [path]
		paths = []
		for i in self.delta[start]:
			if self.delta[start][i] not in path:
				newpaths = self.find_all_paths_bw(self.delta[start][i], end, path+[i])
				for newpath in newpaths:
					if isinstance(self.accept, int):
						if len(newpath) == self.accept*2+1:
							paths.append(newpath)	
					else:
						if len(newpath) == find_max(self.accept)*2+1:
							paths.append(newpath)
					paths.append(newpath)
		return paths

	def getUniquePaths(self):
		newList = []
		hi = self.find_all_paths_bw(self.start, self.accept)
		hi.sort(key=lambda x: len(x))
		for i in range(5):
			li = hi[i]
			tup = tuple(li[1::2])
			newList.append(tup)
		return newList

	def copy(self):
		return DAG(self.states, self.delta, self.start, self.accept)


def intersect(D1, D2):
	start_node = (D1.start, D2.start)
	accept_node = (D1.accept, D2.accept)
	new_delta = {}
	all_states = set()
	for D1key in D1.delta:
		for D2key in D2.delta:
			all_states.add((D1key, D2key))
			new_delta[(D1key, D2key)] = {}
			for D1op in D1.delta[D1key]:
				if D1op in D2.delta[D2key]:
					new_delta[(D1key, D2key)][D1op] = (D1.delta[D1key][D1op], D2.delta[D2key][D1op])
					
	return DAG(all_states, new_delta, start_node, accept_node)


def find_max(test):
	a, b = test
	if isinstance(a, int):
		return max(a, b)
	return max(find_max(a), b)
if __name__ == '__main__':
	states = [0, 1]
	alphabet = ['a', 'b']
	delta = {0:{'b': 1}, 1:{'a': 1, 'b':1}}
	start = 0 
	accept = 1
	dag = DAG(states, delta, start, accept)
	# print(dag.getUniquePaths())
	# states = [0, 1, 2, 3]
	# alphabet = ['a', 'b', 'c', 'd', 'e']
	# delta = {0:{'a':1, 'b': 1, 'd':3, 'e':2}, 1:{'c':2}, 2:{}, 3:{}} 
	# start = 0 
	# accept = 2
	# dag2 = DAG(states, delta, start, accept)
	# print(dag2.getUniquePaths())

	# combined = intersect(dag, dag2)
	# print(combined.getUniquePaths())


