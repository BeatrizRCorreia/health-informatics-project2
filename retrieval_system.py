import os
import sys
import shutil
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from Document import Document
from Query import Query

fp_allDocs = "/home/beatriz/Documents/TIS/health_informatics_project2/med/MED.ALL"
fp_allQueries = "/home/beatriz/Documents/TIS/health_informatics_project2/med/MED.QRY"

def parseAllDocs():
	allDocs = []
	with open(fp_allDocs) as fp:
		line = fp.readline()
		flagInsideDoc = 0
		while line:
			if (flagInsideDoc == 0) and (".I" in line.strip()):
				flagInsideDoc = 1
				docID = ''.join(filter(str.isdigit, line))
				docAll = ''
			elif (line.strip() == ".W"):
				pass
			elif (flagInsideDoc == 1) and (".I" not in line.strip()):
				docAll += line.strip()
				docAll += ' '
			elif (flagInsideDoc == 1) and (".I" in line.strip()):
				flagInsideDoc = 0
				docTitle = ''
				for char in docAll:
					if (char != '.'):
						docTitle += char
					elif (char == '.'):
						break
				docTitle = docTitle + '. '
				docContent = docAll.replace(docTitle, "")
				document = Document(int(docID), docTitle, docContent, docAll)
				allDocs.append(document)
				continue
			line = fp.readline()
		docTitle = ''
		for char in docAll:
			if (char != '.'):
				docTitle += char
			elif (char == '.'):
				break
		docTitle = docTitle + '. '
		docContent = docAll.replace(docTitle, "")
		document = Document(int(docID), docTitle, docContent, docAll)
		allDocs.append(document)
	fp.close()
	return allDocs

def parseAllQueries():
	allQueries = []
	with open(fp_allQueries) as fp:
		line = fp.readline()
		flagInsideQuery = 0
		while line:
			if (flagInsideQuery == 0) and (".I" in line.strip()):
				flagInsideQuery = 1
				queryID = ''.join(filter(str.isdigit, line))
				queryContent = ''
			elif (line.strip() == ".W"):
				pass
			elif (flagInsideQuery == 1) and (".I" not in line.strip()):
				queryContent += line.strip()
				queryContent += ' '
			elif (flagInsideQuery == 1) and (".I" in line.strip()):
				flagInsideQuery = 0
				query = Query(int(queryID), queryContent)
				allQueries.append(query)
				continue
			line = fp.readline()
		query = Query(int(queryID), queryContent)
		allQueries.append(query)
	fp.close()
	return allQueries

def indexMedlineCollection(allDocs):
	schema = Schema(docID = NUMERIC(unique = True, stored = True), docTitle = TEXT(stored = True), docContent = TEXT(stored = True), docAll = TEXT(stored = True))
	if not os.path.exists("indexdir"):
		os.mkdir("indexdir")
	index = create_in("indexdir", schema)
	writer = index.writer()
	for doc in allDocs:
		writer.add_document(docID = doc.get_docID(), docTitle = doc.get_docTitle(), docContent = doc.get_docContent(), docAll = doc.get_docAll())
	writer.commit()

def checkDocumentsIndexed():
	ix = open_dir('indexdir')
	allDocs = ix.searcher().documents()
	for doc in allDocs:
		print(doc)

if __name__ == '__main__':

	# PARSES DOCUMENTS FROM MED.ALL INTO OBJECTS OF TYPE DOCUMENT
	allDocs = parseAllDocs()

	# INDEXES THE DOCUMENTS WITH RESPECT TO THE SCHEMA DEFINED
	indexMedlineCollection(allDocs)

	# PRINTS THE INDEXATION GENERATED
	checkDocumentsIndexed()

	# PARSES QUERIES FROM MED.QRY INTO OBJECTS OF TYPE QUERY
	allQueries = parseAllQueries()

	# REMOVES THE DIRECTORY CREATED FOR THE INDEXING
	shutil.rmtree("indexdir")
