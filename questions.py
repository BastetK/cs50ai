import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 1


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {
        filename: tokenize(files[filename])
        for filename in files
    }
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    files = dict()
    for file_name in os.listdir(directory):
        file = open(os.path.join(directory, file_name))
        files[file_name] = file.read()
    return files


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    words = nltk.tokenize.word_tokenize(document)
    words = [w.lower() for w in words]
    words = [word for word in words if word not in string.punctuation and word not in nltk.corpus.stopwords.words("english")]
    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    idfs = dict()
    unique_words = {word for doc in documents.values() for word in doc}
    for word in unique_words:
        idfs[word] = math.log(len(documents)/len([True for doc in documents.values() if word in doc]))
    return idfs

def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tf_idf = dict()
    for file, words in files.items():
        tf_idf[file] = sum([words.count(word)*idfs[word] for word in query if word in words])
    tf_idf = dict(sorted(tf_idf.items(), key=lambda item: -item[1]))
    ranked_files = list(tf_idf.keys())
    return ranked_files[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    top = dict()
    
    for sentence, words in sentences.items():
        top[sentence] = [sum([idfs[word] for word in query if word in words]),
                        len(query & set(words))/len(words)]
    top = dict(sorted(top.items(), key=lambda item: (-item[1][0], -item[1][1])))
    ranked_sentences = list(top.keys())

    return ranked_sentences[:n]


if __name__ == "__main__":
    main()
