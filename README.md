# Health Informatics - Project 2

The [Medline collection](http://ir.dcs.gla.ac.uk/resources/test_collections/medl/) is a classical resource in information retrieval research, originally created to assist in the development of evaluation experiments. It is a small subset of MEDLINE, consisting of 1033 documents and 30 queries, for which we have relevance judgements.

Using a Python retrieval library named [Whoosh](https://whoosh.readthedocs.io/), you should:
* **(i)** index the Medline collection considering the documents in the file named MED.ALL,
* **(ii)** use the index to retrieve documents for each query in the file named MED.QRY, and
* **(iii)** assess the performance of the system using the relevance judgements in the file named MED.REL, specifically by computing the Precision@10 metric.

Present the Python code used for solving the exercise, and comment on any decisions that you consider to be relevant.

Notice that the file named MED.ALL contains a numeric identifier for each document (that you can use as the title) together with the document's contents, whereas the file named MED.QRY contains an identifier and a textual description of the information need (that you can use as the query to be submitted to the Woosh index). The file named MED.REL has four columns, with the first one referring to the query identifier, and the third one referring to the document identifier.
___
**Files that solve this question:**
main file: [retrieval_system.py](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/retrieval_system.py)\
objects files: [Document.py](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/Document.py), [Query.py](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/Query.py) and [QueryResult.py](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/QueryResult.py)\
Medline collection: [med folder](https://github.com/BeatrizRCorreia/health_informatics_project2/tree/master/med) with files [MED.ALL](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/med/MED.ALL) (documents), [MED.QRY](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/med/MED.QRY) (queries) and [MED.REL](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/med/MED.REL) (relevance judgements)

**My procedure to solve this question:**

1. Parse the Medline collection files: the "MED.ALL" is parsed into a list of objects of type Document; the "MED.QRY" is parsed into a list of objects of type Query and the "MED.REL" is parsed into objects of type QueryResult that are part of a Query object.
2. Preprocess all the documents and queries using three techniques: punctuation removal, removal of stopwords and tokenization and stemming.
3. Index all the documents with respect to a schema that I defined.
4. Search the queries by separating each word with an "OR" which allows retrieving a document when at least one of the words of the query appears in that document. Frequency, TF-IDF, and BM25F are the scoring algorithms used to decide which documents should be retrieved.
5. Assess the performance of the retrieval system by calculating the Precision@10 and the Recall@10 for every query and by calculating the mean of these across all queries. Everything is printed to the command-line.
6. Specified the previously mentioned Or groups to present a behavior named `factory()` that guarantees that documents which contain more of the words in the query searched, will score higher. This parameter was set to 0.9 in both Frequency and TF-IDF scoring schemes and turned off (set 0) for the BM25F scoring. The tunning of these values was done by checking the effects of them on the mean of the system's Precision@10.
7. Remove the directory created for the indexing.

**Linux environment instructions to run my program:**

1. Open a terminal.
2. Get to the folder where the file "retrieval_system.py" is (along with this file, the med folder, and other Python files: "Document.py", "Query.py" and "QueryResult.py").
3. Run the command "python3 retrieval_system.py".

**This is a screenshot of part of the command-line after executing my program:** it shows the Precision@10 and Recall@10 of the different scoring algorithms for Query 27 (all the preprocessing techniques mentioned before were applied).

![First program screenshot](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/images-README.md/first-program-screenshot.png)

**Concerning the points mentioned in the Assignment:**

**(i)** To check the indexation of the Medline collection, line 303 of the file "retrieval_system.py" can be uncommented. This line makes a call to a function `checkDocumentsIndexed()` that presents for every document the contents that were saved and are inside the directory responsible for indexation ("indexdir"). It is probably best to comment line 310 to check this as this one is printing a lot of information to the command-line.

**(ii)** The function `querySearch(allQueries)`, called in line 306 of the file "retrieval_system.py", uses the indexation to retrieve documents for each query in the file named "MED.QRY". This is the search function that looks through the indexed documents using three different scoring algorithms (Frequency, TF-IDF, and BM25F) to find the most relevant documents for a query and retrieve them.

**(iii)** I calculate the Precision@10 and the Recall@10 for every query by making use of the relevance judgments in the file "MED.REL". After these are calculated for all the queries, I make a mean of the values obtained to assess the performance of the system, as can be seen in this screenshot of the final printings in the program:

<p align="center">
	<img width="545" height="226" src="https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/images-README.md/second-program-screenshot.png">
</p>

**Functionality - the pre-processing techniques can be selected:**

The line 297 of the file "retrieval_system.py", can be changed in order to check the effects of the different pre-processing techniques on the mean of Precision@10 and Recall@10.

Line 297: `preprocessingForDocsAndQueries(allDocs, allQueries, removePunctuation = True, removeStopwords = True, tokenizationAndStemmer = True)`

By changing one or multiple parameters to _False_, the corresponding pre-processing technique will not be applied.

**Effects – different combinations of the pre-processing techniques:**

![Venn diagram](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/images-README.md/venn-diagram.png)

![Table with different techniques](https://github.com/BeatrizRCorreia/health_informatics_project2/blob/master/images-README.md/table-different-techniques.png)

**Conclusion:**

I can conclude that the scoring scheme and the pre-processing techniques used have a substantial impact in the retrieval of relevant documents.

The scoring algorithm that was able to retrieve the most relevant documents was BM25F as can be seen in the previous table. This scoring scheme achieved a Precision@10 of 67.7% and a Recall@10 of 32.3%. To this result also contributed the execution of all the pre-processing techniques, although the same values were obtained when the removal of stopwords was disabled.

It is also interesting to notice, that even though the exclusion of this technique was beneficial for the BM25F results, for a scoring scheme based in the frequency of the words, the best Precision@10 and Recall@10 (53.0% and 25.3%) were a consequence of exclusively applying it.
