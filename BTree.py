class BNode(object):
	def __init__(self, char):
		self.index = char
		self.isWord = 0
		self.next = dict()

class BTree(object):
	def __init__(self):
		self.root = BNode("")
	def insert(self,word):
		current = self.root
		i = 0 
		while i < len(word) and word[i] in current.next:
			current = current.next[word[i]]
			i += 1
		if i == len(word):
			current.isWord = 1
		else:
			while i < len(word):
				node = BNode(word[i])
				current.next[word[i]] = node
				current = current.next[word[i]]
				i += 1
			current.isWord = 1
