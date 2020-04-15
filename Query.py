class Query:

	def __init__(self, queryID, queryContent, queryResult):
		self.queryID = queryID
		self.queryContent = queryContent
		self.queryResult = queryResult

	def get_queryID(self):
		return self.queryID

	def get_queryContent(self):
		return self.queryContent

	def get_queryResult(self):
		return self.queryResult

	def set_queryContent(self, newContent):
		self.queryContent = newContent

	def set_queryResult(self, newQueryResult):
		self.queryResult = newQueryResult
