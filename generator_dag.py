from dag import DAG, intersect

class AST(object):
	def toAST(self):
		return [self]

class ConstantString(AST):
	# atomic version space 
	def __init__(self, string):
		self.constantString = string

	def __str__(self):
		return "ConstantString(" + self.constantString + ")"

	def __eq__(self, other):
		if isinstance(other, ConstantString):
			return other.constantString == self.constantString
		return False

	def __key(self):
		return (self.constantString,)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return self.constantString

class FindPrefix(AST): 
	# atomic version space 
	def __init__(self, letter):
		self.letter = letter

	def __str__(self):
		return "FindPrefix(" + str(self.letter) + ")"

	def __eq__(self, other):
		if isinstance(other, FindPrefix):
			return other.letter == self.letter
		return False


	def __key(self):
		return (self.letter,)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return string.find(self.letter)

class FindSuffix(AST): 
	# atomic version space 
	def __init__(self, letter):
		self.letter = letter

	def __str__(self):
		return "FindSuffix(" + str(self.letter) + ")"

	def __eq__(self, other):
		if isinstance(other, FindSuffix):
			return other.letter == self.letter
		return False


	def __key(self):
		return (self.letter,)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return string.rfind(self.letter)

class ConcatString(AST):
	def __init__(self, left, right):
		self.left = left
		self.right = right
	def __str__(self):
		return "Concat(" + str(self.left) + str(self.right) + ")"

	def __eq__(self, other):
		if isinstance(other, ConcatString):
			return other.left == self.left and other.right == self.right
		return False


	def __key(self):
		return tuple(self.left) + tuple(self.right)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return self.left.execute(string) + self.right.execute(string) 


class LinearInt(AST):
	# atomic version space 
	def __init__(self, number):
		self.num = number

	def __str__(self):
		return "LinearInt(" + str(self.num) + ")"

	def __eq__(self, other):
		if isinstance(other, LinearInt):
			return other.num == self.num
		return False

	def __key(self):
		return (self.num,)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return self.num

class Substring(AST):
	def __init__(self, left, right):
		self.left = left
		self.right = right

	def __str__(self):
		return "Substring(" + str(self.left) + ", " + str(self.right) + ")"

	def __eq__(self, other):
		if isinstance(other, Substring):
			return other.left == self.left and other.right == self.right
		return False

	def __key(self):
		return tuple(self.left) + tuple(self.right)
		
	def __hash__(self):
		return hash(self.__key())

	def execute(self, string):
		return string[self.left.execute(string):self.right.execute(string)+1]

def getAllSubstrings(input):
	length = len(input)
	dicMap = {} 
	for i in range(length):
		for j in range(i, length):
			if input[i:j+1] in dicMap:
				dicMap[input[i:j+1]].append((i, j))
			else:
				dicMap[input[i:j+1]] = [(i, j)]
	return dicMap


class ConcatVS():
	def __init__(self, left, right):
		"""
		left / right ==> list/set
		"""
		self.left = left
		self.right = right

	def __str__(self):
		leftList = []
		for i in self.left:
			# if i != None and i not in leftList and i != []:
			leftList.append(str(i))
		rightList = []
		for j in self.right:
			# if j != None and j not in rightList and j != []:
			rightList.append(str(j))
		return "Concat({" + str(leftList)+"}, {" + str(rightList) + "})"

	def __eq__(self, other):
		if isinstance(other, ConcatVS):
			return other.left == self.left and other.right == self.right
		return False

	def __key(self):
		return tuple(self.left) + tuple(self.right)
		
	def __hash__(self):
		return hash(self.__key())

	def getOverlap(self, other):
		overlapRight = []
		overlapLeft = [] 

		for i in self.left:
			for j in other.left:
				if (isinstance(i, FindPrefix) or isinstance(i, LinearInt) or isinstance(i, FindSuffix) or isinstance(i, ConstantString)\
					or isinstance(j, FindPrefix) or isinstance(j, LinearInt) or isinstance(j, FindSuffix) or isinstance(j, ConstantString) or j is None or i is None):
					if i == j:
						overlapLeft.append(i)
				else:
					curList = i.getOverlap(j)
					if (curList != None):
						overlapLeft.append(curList)
		for i in self.right:
			for j in other.right:
				if (isinstance(i, FindPrefix) or isinstance(i, LinearInt) or isinstance(i, FindSuffix) or isinstance(i, ConstantString)\
					or isinstance(j, FindPrefix) or isinstance(j, LinearInt) or isinstance(j, FindSuffix) or isinstance(j, ConstantString) or j is None or i is None):
					if i == j:
						overlapRight.append(i)
				else:
					curList = i.getOverlap(j)
					if (curList != None):
						overlapRight.append(curList)
		if overlapLeft != [] and overlapRight != []:			
			return ConcatVS(overlapLeft, overlapRight)

	def toAST(self):
		totalAST = []
		for ele1 in self.left:
			for ele2 in self.right:
				for i in ele1.toAST():
					for j in ele2.toAST():
						totalAST.append(ConcatString(i, j))
		return totalAST

class SubstringVS():
	def __init__(self, left, right):
		"""
		left / right ==> list/set
		"""
		self.left = left
		self.right = right

	def __str__(self):
		leftList = []
		for i in self.left:
			leftList.append(str(i))
		rightList = []
		for j in self.right:
			rightList.append(str(j))
		return "SubString({" + str(leftList)+"}, {" + str(rightList) + "})"

	def __eq__(self, other):
		if isinstance(other, SubstringVS):
			return other.left == self.left and other.right == self.right
		return False

	def __key(self):
		return tuple(self.left) + tuple(self.right)
		
	def __hash__(self):
		return hash(self.__key())

	def getOverlap(self, other):
		overlapRight = []
		overlapLeft = [] 
		for i in self.left:
			for j in other.left:
				if (isinstance(i, FindPrefix) or isinstance(i, LinearInt) or isinstance(i, FindSuffix) or isinstance(i, ConstantString)\
					or isinstance(j, FindPrefix) or isinstance(j, LinearInt) or isinstance(j, FindSuffix) or isinstance(j, ConstantString) or j is None or i is None):
					if i == j:
						overlapLeft.append(i)
				else:
					curList = i.getOverlap(j)
					if (curList != None):
						overlapLeft.append(curList)

		for i in self.right:
			for j in other.right:
				if (isinstance(i, FindPrefix) or isinstance(i, LinearInt) or isinstance(i, FindSuffix) or isinstance(i, ConstantString)\
					or isinstance(j, FindPrefix) or isinstance(j, LinearInt) or isinstance(j, FindSuffix) or isinstance(j, ConstantString) or j is None or i is None):
					if i == j:
						overlapRight.append(i)
				else:
					curList = i.getOverlap(j)
					if (curList != None):
						overlapRight.append(curList)

		if overlapLeft != [] and overlapRight != []:			
			return SubstringVS(overlapLeft, overlapRight)

	def toAST(self):
		totalAST = []
		for ele1 in self.left:
			for ele2 in self.right:
				for i in ele1.toAST():
					for j in ele2.toAST():
						totalAST.append(Substring(i, j))
		return totalAST

def generateVSConstStr(input, output):
	"""
	input: abc
	output: bc
	"""
	return [ConstantString(output)]

def generateVSSubstring(input, output):
	"""
	substrings: -> ints, prefix suffix search
	"""
	indices = [] 
	allSubstrings = getAllSubstrings(input)
	if output in allSubstrings:
		possibleInputs = allSubstrings[output]
	else:
		return []

	total = []
	for interval in possibleInputs:
		curStart = interval[0]
		curEnd = interval[1]
		for i in getSSProgram(input, output, curStart):
			for j in getSSProgram(input, output, curEnd):
				total.append(SubstringVS([i], [j]))
		# total.append(SubstringVS(getSSProgram(input, output, curStart), getSSProgram(input, output, curEnd)))
	return total

def getSSProgram(input, output, number): 
	allPrograms = [LinearInt(number)]
	for i in range(len(output), 0, -1):
		curOutput = output[:i]
		otherOutput = output[i:]
		if len(curOutput) != 0:
			if FindPrefix(curOutput).execute(input) == number:
				allPrograms.append(FindPrefix(curOutput))
			if FindSuffix(curOutput).execute(input) == number:
				allPrograms.append(FindSuffix(curOutput))
		if len(otherOutput) != 0:
			if FindPrefix(otherOutput).execute(input) == number:
				allPrograms.append(FindPrefix(otherOutput))
			if FindSuffix(otherOutput).execute(input) == number:
				allPrograms.append(FindSuffix(otherOutput))

	if " " in input:
		if FindPrefix(" ").execute(input) == number+1:
			allPrograms.append(FindPrefix(" "))
		if FindSuffix(" ").execute(input) == number+1:
			allPrograms.append(FindSuffix(" "))
	return allPrograms

def getPrograms(input, output):
	states = [i for i in range(len(output)+1)]
	delta = getDelta(states, input, output)
	start = 0 
	accept = len(output)
	dag = DAG(states, delta, start, accept)
	return dag

def getDelta(states, input, output):
	delta = {}
	for state in states:
		if state != len(output):
			delta[state] = {ConstantString(output[state:state+1]):state+1}
			for num in states[state:]:
				programs = generateVSSubstring(input, output[state:num])
				for program in programs:
					delta[state][program] = num
		else:
			delta[state] = {}
	return delta


if __name__ == '__main__':
	one = getPrograms("Rob Miller", "R")
	two = getPrograms("Bob Huanga", "B")
	# for key in one.delta.keys():
	# 	for i in one.delta[key].keys():
	# 		print(key, i, one.delta[key][i])

	# for key in two.delta.keys():
	# 	for i in two.delta[key].keys():
	# 		print(key, i, two.delta[key][i])
	# print([i for i in one.delta.keys()])
	for path in intersect(one, two).getUniquePaths():
		check = [str(ele) for ele in path]
		print(check, len(check))





































