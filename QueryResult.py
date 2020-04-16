class QueryResult:

	def __init__(self):
		self.listOfDocIDsGiven = []
		self.listOfDocIDsRetrieved_frequency = []
		self.listOfScores_frequency = []
		self.listOfDocIDsRetrieved_TFIDF = []
		self.listOfScores_TFIDF = []
		self.listOfDocIDsRetrieved_BM25F = []
		self.listOfScores_BM25F = []

	def get_listOfDocIDsGiven(self):
		return self.listOfDocIDsGiven

	def get_listOfDocIDsRetrieved_frequency(self):
		return self.listOfDocIDsRetrieved_frequency

	def get_listOfScores_frequency(self):
		return self.listOfScores_frequency

	def get_listOfDocIDsRetrieved_TFIDF(self):
		return self.listOfDocIDsRetrieved_TFIDF

	def get_listOfScores_TFIDF(self):
		return self.listOfScores_TFIDF

	def get_listOfDocIDsRetrieved_BM25F(self):
		return self.listOfDocIDsRetrieved_BM25F

	def get_listOfScores_BM25F(self):
		return self.listOfScores_BM25F

	def add_docIDGiven(self, docIDGiven):
		self.listOfDocIDsGiven.append(docIDGiven)

	def add_docIDRetrieved_frequency(self, docIDRetrieved_frequency):
		self.listOfDocIDsRetrieved_frequency.append(docIDRetrieved_frequency)

	def add_score_frequency(self, score_frequency):
		self.listOfScores_frequency.append(score_frequency)

	def add_docIDRetrieved_TFIDF(self, docIDRetrieved_TFIDF):
		self.listOfDocIDsRetrieved_TFIDF.append(docIDRetrieved_TFIDF)

	def add_score_TFIDF(self, score_TFIDF):
		self.listOfScores_TFIDF.append(score_TFIDF)

	def add_docIDRetrieved_BM25F(self, docIDRetrieved_BM25F):
		self.listOfDocIDsRetrieved_BM25F.append(docIDRetrieved_BM25F)

	def add_score_BM25F(self, score_BM25F):
		self.listOfScores_BM25F.append(score_BM25F)