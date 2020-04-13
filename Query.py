class Query:

	def __init__(self, queryID, queryContent):
		self.queryID = queryID
		self.queryContent = queryContent

	def get_queryID(self):
		return self.queryID

	def get_queryContent(self):
		return self.queryContent
