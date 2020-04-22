class Query:

	def __init__(self, queryID, queryContent, QueryResult):
		self.queryID = queryID
		self.queryContent = queryContent
		self.QueryResult = QueryResult

	def get_queryID(self):
		return self.queryID

	def get_queryContent(self):
		return self.queryContent

	def get_QueryResult(self):
		return self.QueryResult

	def set_queryContent(self, newContent):
		self.queryContent = newContent

	def set_QueryResult(self, newQueryResult):
		self.QueryResult = newQueryResult
