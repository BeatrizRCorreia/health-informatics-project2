# Health Informatics - Project 2

The [Medline collection](http://ir.dcs.gla.ac.uk/resources/test_collections/medl/) is a classical resource in information retrieval research, originally created to assist in the development of evaluation experiments. It is a small subset of MEDLINE, consisting of 1033 documents and 30 queries, for which we have relevance judgements.

Using a Python retrieval library named [Whoosh](https://whoosh.readthedocs.io/), you should:
* **(i)** index the Medline collection considering the documents in the file named MED.ALL,
* **(ii)** use the index to retrieve documents for each query in the file named MED.QRY, and
* **(iii)** assess the performance of the system using the relevance judgements in the file named MED.REL, specifically by computing the Precision@10 metric.

Present the Python code used for solving the exercise, and comment on any decisions that you consider to be relevant.

Notice that the file named MED.ALL contains a numeric identifier for each document (that you can use as the title) together with the document's contents, whereas the file named MED.QRY contains an identifier and a textual description of the information need (that you can use as the query to be submitted to the Woosh index). The file named MED.REL has four columns, with the first one referring to the query identifier, and the third one referring to the document identifier.
___
**Files that solve this question:**\
main file: retrieval_system.py
objects files: Document.py, Query.py and QueryResult.py
Medline collection: med folder with files MED.ALL (documents), MED.QRY (queries) and MED.REL (relevance judgements)
___
**My procedure to solve this question:**\
1. Parse the Medline collection files: the MED.ALL is parsed into a list of objects of type Document; the MED.QRY is parsed into a list of objects of type Query and the MED.REL is parsed into objects of type QueryResult that are part of a Query object.
2. Preprocess all the documents and queries using three techniques: ponctuation removal, removal of stopwords and tokenization and stemming.
3. Index all the documents with respect to a schema that I defined.
4. Search the queries by separating each word with an "OR" which allows to retrieve a document when at least one of the words of the query appears in that document. Frequency, TF-IDF and BM25F are the scoring algorithms used to decide which documents should be retrieved.
5. Assess the performance of the retrieval system by calculating the Precision@10 and the Recall@10 for every query and by calculating the mean of these across all queries.
6. Specified the previously mentioned Or groups to present a behavior named "factory()" that guarantees that documents which contain more of the words in the query searched, will score higher. This parameter was set to 0.9 in both Frequency and TF-IDF scoring schemes and turned off (set 0) for the BM25F scoring. The tunning of these values was done by checking the effects of them on the mean of the system's Precision@10.
7. Remove the directory created for the indexing.
___
**(i)**

To check the indexation of the Medline collection, line 303 of the file "retrieval_system.py" can be uncommented. This line makes a call to a function "checkDocumentsIndexed()" that presents for every document the contents that were saved and are inside the directory responsible for indexation ("indexdir").
It is probably best to comment line 310 to check this as this one is printing a lot of information to the command-line.
___
**(ii)**

The function "querySearch(allQueries)", called in line 306 of the file "retrieval_system.py", uses the indexation to retrieve documents for each query in the file named MED.QRY. This is the search function that looks through the indexed documents using three diferent scoring algorithms (Frequency, TF-IDF and BM25F) to find the most relevant documents for every query and retrieves them.
___
**(iii)**

I calculate the Precision@10 and the Recall@10 for every query by making use of the relevance judgements in the file MED:REL. After these are calculated for all the queries, I make a mean of the values obtained in order to assess the performance of the system.
___