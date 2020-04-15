class Document:

	def __init__(self, docID, docTitle, docContent, docAll):
		self.docID = docID
		self.docTitle = docTitle
		self.docContent = docContent
		self.docAll = docAll

	def get_docID(self):
		return self.docID

	def get_docTitle(self):
		return self.docTitle

	def get_docContent(self):
		return self.docContent

	def get_docAll(self):
		return self.docAll

	def set_docAll(self, newAll):
		self.docAll = newAll