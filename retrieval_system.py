import os
import sys
import shutil
import re
import nltk
from whoosh.index import create_in
from whoosh.index import open_dir
from whoosh.fields import Schema, TEXT, NUMERIC
from whoosh import qparser
from whoosh.qparser import QueryParser
from whoosh import scoring
from whoosh.index import open_dir
from nltk.corpus import stopwords

from Document import Document
from Query import Query
from QueryResult import QueryResult

fp_allDocs = "/home/beatriz/Documents/TIS/health_informatics_project2/med/MED.ALL"
fp_allQueries = "/home/beatriz/Documents/TIS/health_informatics_project2/med/MED.QRY"
fp_allResults = "/home/beatriz/Documents/TIS/health_informatics_project2/med/MED.REL"

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
				queryResult = QueryResult()
				query = Query(int(queryID), queryContent, queryResult)
				allQueries.append(query)
				continue
			line = fp.readline()
		queryResult = QueryResult()
		query = Query(int(queryID), queryContent, queryResult)
		allQueries.append(query)
	fp.close()
	return allQueries

def parseAllResults(allQueries):
	with open(fp_allResults) as fp:
		line = fp.readline()
		while line:
			parsedLine = line.split()
			for query in allQueries:
				if (int(parsedLine[0]) == query.get_queryID()):
					query.get_queryResult().add_docIDGiven(int(parsedLine[2]))
			line = fp.readline()
	return

def preprocessingForDocsAndQueries(allDocs, allQueries, removePonctuation, removeStopwords, tokenizationAndStemmer):
	if (removePonctuation == True):
		for doc in allDocs:
			new = doc.get_docAll()
			new = re.sub("([0-9]+\.)", "", new)
			new = re.sub("([0-9]+\))", "", new)
			new = re.sub("[\?|\.!:,;-]", "", new)
			new = re.sub("(\n)", " ", new)
			new = re.sub("[ ]{2,}", "", new)
			new = re.sub("[\"\'\(\)]", "", new)
			new = new.strip()
			doc.set_docAll(new)
			# print(new)
		for query in allQueries:
			new = query.get_queryContent()
			new = re.sub("([0-9]+\.)", "", new)
			new = re.sub("([0-9]+\))", "", new)
			new = re.sub("[\?|\.!:,;-]", "", new)
			new = re.sub("(\n)", " ", new)
			new = re.sub("[ ]{2,}", "", new)
			new = re.sub("[\"\'\(\)]", "", new)
			new = new.strip()
			query.set_queryContent(new)
			# print(new)
	if (removeStopwords == True):
		stopWords = list(stopwords.words('english'))
		for doc in allDocs:
			new = doc.get_docAll()
			listWithAllWordsBefore = new.split()
			listWithAllWordsAfter = []
			for word in listWithAllWordsBefore:
				if word not in stopWords:
					listWithAllWordsAfter.append(word)
				new = ' '.join(listWithAllWordsAfter)
			doc.set_docAll(new)
			# print(new)
		for query in allQueries:
			new = query.get_queryContent()
			listWithAllWordsBefore = new.split()
			listWithAllWordsAfter = []
			for word in listWithAllWordsBefore:
				if word not in stopWords:
					listWithAllWordsAfter.append(word)
				new = ' '.join(listWithAllWordsAfter)
			query.set_queryContent(new)
			# print(new)
	if (tokenizationAndStemmer == True):
		stemmer = nltk.stem.PorterStemmer()
		for doc in allDocs:
			new = doc.get_docAll()
			listWithAllWordsTokenized = nltk.word_tokenize(new)
			listWithAllWordsStemmed = []
			for word in listWithAllWordsTokenized:
				word = stemmer.stem(word)
				listWithAllWordsStemmed.append(word)
			new = ' '.join(listWithAllWordsStemmed)
			doc.set_docAll(new)
			# print(new)
		for query in allQueries:
			new = query.get_queryContent()
			listWithAllWordsTokenized = nltk.word_tokenize(new)
			listWithAllWordsStemmed = []
			for word in listWithAllWordsTokenized:
				word = stemmer.stem(word)
				listWithAllWordsStemmed.append(word)
			new = ' '.join(listWithAllWordsStemmed)
			query.set_queryContent(new)
			# print(new)
	return

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

def querySearch(allQueries):
	for query in allQueries:
		queryPrepared = query.get_queryContent()
		ix = open_dir('indexdir')
		with ix.searcher(weighting = scoring.Frequency) as searcher:
			queryString = QueryParser("docAll", ix.schema, group = qparser.OrGroup.factory(0.9)).parse(queryPrepared)
			# queryString = QueryParser("docAll", ix.schema).parse(queryPrepared)
			results = searcher.search(queryString, limit = None)
			# print(results)
			for i in results:
				query.get_queryResult().add_docIDRetrieved_frequency(i["docID"])
				query.get_queryResult().add_score_frequency(i.score)
		with ix.searcher(weighting = scoring.TF_IDF) as searcher:
			queryString = QueryParser("docAll", ix.schema, group = qparser.OrGroup.factory(0.9)).parse(queryPrepared)
			# queryString = QueryParser("docAll", ix.schema).parse(queryPrepared)
			results = searcher.search(queryString, limit = None)
			# print(results)
			for i in results:
				query.get_queryResult().add_docIDRetrieved_TFIDF(i["docID"])
				query.get_queryResult().add_score_TFIDF(i.score)
		with ix.searcher(weighting = scoring.BM25F) as searcher:
			queryString = QueryParser("docAll", ix.schema, group = qparser.OrGroup.factory(0)).parse(queryPrepared)
			# queryString = QueryParser("docAll", ix.schema).parse(queryPrepared)
			results = searcher.search(queryString, limit = None)
			# print(results)
			for i in results:
				query.get_queryResult().add_docIDRetrieved_BM25F(i["docID"])
				query.get_queryResult().add_score_BM25F(i.score)
	return

def assessSystemPerformance(allQueries):
	TOTAL_precisions_frequency = 0
	TOTAL_precisions_TFID = 0
	TOTAL_precisions_BM25F = 0
	TOTAL_recalls_frequency = 0
	TOTAL_recalls_TFID = 0
	TOTAL_recalls_BM25F = 0
	for query in allQueries:
		listOftop10_retrieved_frequency = query.get_queryResult().get_listOfDocIDsRetrieved_frequency()[:10]
		listOftop10_retrieved_TFIDF = query.get_queryResult().get_listOfDocIDsRetrieved_TFIDF()[:10]
		listOftop10_retrieved_BM25F = query.get_queryResult().get_listOfDocIDsRetrieved_BM25F()[:10]
		listOf_relevant = query.get_queryResult().get_listOfDocIDsGiven()
		print('\nrelevant:', listOf_relevant)
		print('top 10 retrieved by frequency:', listOftop10_retrieved_frequency)
		print('top 10 retrieved by TF-IDF:', listOftop10_retrieved_TFIDF)
		print('top 10 retrieved by BM25F:', listOftop10_retrieved_BM25F)
		relevant_retrieved_frequency = 0
		relevant_retrieved_TFIDF = 0
		relevant_retrieved_BM25F = 0

		for retrieved in listOftop10_retrieved_frequency:
			if retrieved in listOf_relevant:
				relevant_retrieved_frequency += 1
		precision_at_10_frequency = (relevant_retrieved_frequency / len(listOftop10_retrieved_frequency)) * 100
		print("Precision @ 10:", precision_at_10_frequency)
		recall_at_10_frequency = (relevant_retrieved_frequency / len(listOf_relevant)) * 100
		print("Recall @ 10:", recall_at_10_frequency)
		TOTAL_precisions_frequency += precision_at_10_frequency
		TOTAL_recalls_frequency += recall_at_10_frequency

		for retrieved in listOftop10_retrieved_TFIDF:
			if retrieved in listOf_relevant:
				relevant_retrieved_TFIDF += 1
		precision_at_10_TFIDF = (relevant_retrieved_TFIDF / len(listOftop10_retrieved_frequency)) * 100
		print("Precision @ 10:", precision_at_10_TFIDF)
		recall_at_10_TFIDF = (relevant_retrieved_TFIDF / len(listOf_relevant)) * 100
		print("Recall @ 10:", recall_at_10_TFIDF)
		TOTAL_precisions_TFID += precision_at_10_TFIDF
		TOTAL_recalls_TFID += recall_at_10_TFIDF

		for retrieved in listOftop10_retrieved_BM25F:
			if retrieved in listOf_relevant:
				relevant_retrieved_BM25F += 1
		precision_at_10_BM25F = (relevant_retrieved_BM25F / len(listOftop10_retrieved_frequency)) * 100
		print("Precision @ 10:", precision_at_10_BM25F)
		recall_at_10_BM25F = (relevant_retrieved_BM25F / len(listOf_relevant)) * 100
		print("Recall @ 10:", recall_at_10_BM25F)
		TOTAL_precisions_BM25F += precision_at_10_BM25F
		TOTAL_recalls_BM25F += recall_at_10_BM25F

	print('\nMean Precision@10 for frequency:', (TOTAL_precisions_frequency / len(allQueries)), '%')
	print('Mean Precision@10 for TFIDF:', (TOTAL_precisions_TFID / len(allQueries)), '%')
	print('Mean Precision@10 for BM25F:', (TOTAL_precisions_BM25F / len(allQueries)), '%')

	print('\nMean Recall@10 for frequency:', (TOTAL_recalls_frequency / len(allQueries)), '%')
	print('Mean Recall@10 for TFIDF:', (TOTAL_recalls_TFID / len(allQueries)), '%')
	print('Mean Recall@10 for BM25F:', (TOTAL_recalls_BM25F / len(allQueries)), '%')

if __name__ == '__main__':

	# PARSES DOCUMENTS FROM MED.ALL INTO OBJECTS OF TYPE DOCUMENT
	allDocs = parseAllDocs()

	# PARSES QUERIES FROM MED.QRY INTO OBJECTS OF TYPE QUERY
	allQueries = parseAllQueries()

	parseAllResults(allQueries)

	# for query in allQueries:
		# print("QUERY NUMBER:", query.get_queryID(), query.get_queryResult().get_listOfDocIDsGiven())

	# DIFERENT PREPROCESSING TECHNIQUES APPLIED TO BOTH DOCS AND QUERIES
	preprocessingForDocsAndQueries(allDocs, allQueries, True, True, True)

	# INDEXES THE DOCUMENTS WITH RESPECT TO THE SCHEMA DEFINED
	indexMedlineCollection(allDocs)

	# PRINTS THE INDEXATION GENERATED
	# checkDocumentsIndexed()

	querySearch(allQueries)

	# for query in allQueries:
		# print(query.get_queryID(), ':', query.get_queryResult().get_listOfDocIDsGiven(), '\nRETRIEVED BY FREQUENCY:', query.get_queryResult().get_listOfDocIDsRetrieved_frequency(), '\nRETRIEVED BY TF-IDF:', query.get_queryResult().get_listOfDocIDsRetrieved_TFIDF(), '\nRETRIEVED BY BM25F:', query.get_queryResult().get_listOfDocIDsRetrieved_BM25F(), '\n')
		# print('SCORES BY FREQUENCY:', query.get_queryResult().get_listOfScores_frequency(), '\n')
		# print(query.get_queryContent())

	assessSystemPerformance(allQueries)

	# REMOVES THE DIRECTORY CREATED FOR THE INDEXING
	shutil.rmtree("indexdir")
