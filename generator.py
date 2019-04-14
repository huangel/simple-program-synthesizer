import string

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

	def execute(self, string):
		return self.constantString

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

	def execute(self, string):
		return self.num

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

	def execute(self, string):
		return self.left.execute(string) + self.right.execute(string) 

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

	def execute(self, string):
		return string[self.left.execute(string):self.right.execute(string)+1]

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

def generateVSConcat(input, output):
	"""
	abc
	bc
	left/right ==> Concats or ConstantString
	"""
	if len(output) == 0:
		return [ConstantString("")]
	elif len(output) == 1:
		return [ConstantString(output)]
	totalConcat = []
	for i in range(1, len(output)):
		left = output[:i]
		right = output[i:]
		totalConcat.append(ConcatVS(generateVSConcat(input, left), generateVSConcat(input, right)))
	totalConcat.append(ConstantString(output))
	return totalConcat

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
		total.append(SubstringVS(getProgram(input, output, curStart), getProgram(input, output, curEnd)))
	return total

def getProgram(input, output, number): 
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

def generateVS(input, output):
	totalVS = [] 
	for i in range(1, len(output)):
		left = output[:i]
		right = output[i:]
		totalVS.append(ConcatVS(generateVS(input, left), generateVS(input, right)))
		# totalVS.append(SubstringVS(generateVS(input, left), generateVS(input, right)))
	totalVS += generateVSConstStr(input, output)
	totalVS += generateVSConcat(input, output)
	totalVS += generateVSSubstring(input, output)
	return totalVS

def checkExist(cur, final):
	for i in final:
		if i == cur:
			return True
	return False

def generateOverlapPrograms(inputs, outputs):
	"""
	lists of inputs and list of outputs 
	"""
	list1 = generateVS(inputs[0], outputs[0])
	list2 = generateVS(inputs[1], outputs[1])

	final = []
	compare = []
	for indx, ele in enumerate(list1):
		for index2, ele2 in enumerate(list2):
			if isinstance(ele, ConstantString):
				if ele == ele2:
					final.append(ele)
			elif (isinstance(ele, ConcatVS) or isinstance(ele, SubstringVS)) and (isinstance(ele2, ConcatVS) or isinstance(ele2, SubstringVS)):
				curList = ele.getOverlap(ele2)
				if curList != None:
					if (curList.left != [] and curList.right != [] and not checkExist(curList, final)):
						final.append(curList)
	
	compare = final[:]
	for index in range(2, len(inputs)):
		final = []
		allPrograms = generateVS(inputs[index], outputs[index])
		for indx, ele in enumerate(compare):
			for index2, ele2 in enumerate(allPrograms):
				if isinstance(ele, ConstantString):
					if ele == ele2:
						final.append(ele)
				elif (isinstance(ele, ConcatVS) or isinstance(ele, SubstringVS)) and (isinstance(ele2, ConcatVS) or isinstance(ele2, SubstringVS)):
					curList = ele.getOverlap(ele2)
					if curList != None:
						if (curList.left != [] and curList.right != [] and curList not in final):
							final.append(curList)
		compare = final[:]

	if final == []:
		return ["No possible programs"]
	return final


if __name__ == '__main__':
	# generateVSConcat('abc', 'bc')
	# print(ConcatVS(, generateVSConcat('abc', 'bc')))
	# print(FindPrefix('a') == FindPrefix('a'))
	# print(Substring(FindPrefix('a'), FindSuffix('b')) == Substring(FindPrefix('a'), FindSuffix('b')))
	x = generateOverlapPrograms(["Angel H", "Jimmy K", "Jeana C"], ['A. H', "J. K", "J. C"])
	# print(program.execute("James G"))
	# print(x)
	program = x[-1]
	print(program.toAST())
	for i in program.toAST():
		print(i)
		print(i.execute("James G"))

	# for i in generateOverlapPrograms(["ab C", "de F", "ghe P"], ['aCb', "dFe", "gPhe"]):
	# 	print(i)
	# for i in generateVSSubstring("ac b", "abc"):
	# 	print(i)
	# generateOverlapPrograms(["Angel H", "Jimmy K"], ['AngHel', "JimKmy"])

	# left = [SubstringVS(FindPrefix('a'), FindSuffix('a'))]
	# right = [ConstantString("bc")]
	# left1 = [SubstringVS(FindPrefix('a'), FindSuffix('a'))]
	# right1 = [ConstantString("bc")]
	# print(ConcatVS(left, right) == ConcatVS(left1, right1))
	# # print(Substring(FindPrefix('a'), FindSuffix('a')))
	# # print(ConcatVS(left, right).toAST())
	# for i in ConcatVS(left, right).toAST():
	#   print(i)
	#   print(i.execute('abc'))
	# print(FindPrefix('m').toAST()[0])
	# print(Substring(FindPrefix(''), FindSuffix('my n')).execute("my name is angel"))



