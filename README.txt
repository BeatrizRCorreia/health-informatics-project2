******* Run my solution - Linux environment instructions: *******

1. Open a terminal.
2. Get to the folder where the file "retrieval_system.py" is (along with this file, the med folder and other Python files: Document.py, Query.py and QueryResult.py).
3. Run the command "python3 retrieval_system.py".

******* Install the packages needed - Linux environment instructions: *******

WHOOSH
command: "pip3 install Whoosh"
NLTK
command: "pip3 install nltk"

******* Functionality: *******

The line 297 of the file "retrieval_system.py", can be changed in order to check the effects of the different preprocessing techniques on the mean of Precision@10 and Recall@10:

Line 297:
preprocessingForDocsAndQueries(allDocs, allQueries, removePonctuation = True, removeStopwords = True, tokenizationAndStemmer = True)

By changing one or multiple parameters to "False", the corresponding preprocessing technique will not applied.