# Health Informatics - Project 2

The [Medline collection](http://ir.dcs.gla.ac.uk/resources/test_collections/medl/) is a classical resource in information retrieval research, originally created to assist in the development of evaluation experiments. It is a small subset of MEDLINE, consisting of 1033 documents and 30 queries, for which we have relevance judgements.

Using a Python retrieval library named [Woosh](https://whoosh.readthedocs.io/), you should:
* **(i)** index the Medline collection considering the documents in the file named MED.ALL,
* **(ii)** use the index to retrieve documents for each query in the file named MED.QRY, and
* **(iii)** assess the performance of the system using the relevance judgements in the file named MED.REL, specifically by computing the Precision@10 metric.

Present the Python code used for solving the exercise, and comment on any decisions that you consider to be relevant.

Notice that the file named MED.ALL contains a numeric identifier for each document (that you can use as the title) together with the document's contents, whereas the file named MED.QRY contains an identifier and a textual description of the information need (that you can use as the query to be submitted to the Woosh index). The file named MED.REL has four columns, with the first one referring to the query identifier, and the third one referring to the document identifier.