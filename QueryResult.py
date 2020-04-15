class QueryResult:

	def __init__(self):
		self.listOfDocIDsGiven = []
		self.listOfDocIDsRetrieved = []
		self.listOfScores = []

	def get_listOfDocIDsGiven(self):
		return self.listOfDocIDsGiven

	def get_listOfDocIDsRetrieved(self):
		return self.listOfDocIDsRetrieved

	def get_listOfScores(self):
		return self.listOfScores

	def add_docIDGiven(self, docIDGiven):
		self.listOfDocIDsGiven.append(docIDGiven)

	def add_docIDRetrieved(self, docIDRetrieved):
		self.listOfDocIDsRetrieved.append(docIDRetrieved)

	def add_score(self, score):
		self.listOfScores.append(score)