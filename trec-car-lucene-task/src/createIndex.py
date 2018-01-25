"""
@author: pooja_oza
"""
import lucene

from java.nio.file import Paths
from org.apache.lucene.store import FSDirectory
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, DirectoryReader, \
    IndexOptions, Term
from org.apache.lucene.search import IndexSearcher, PhraseQuery
from org.apache.lucene.document import Document, Field, TextField, StoredField, FieldType, StringField
from org.apache.lucene.analysis.standard import StandardAnalyzer

from utils import get_stemmed_string
from constructKeywordQuery import get_paragraphs


class CreateIndex(object):
    """
    Create an index which contains the terms with document ids, frequencies and positions
    from the input file
    Each paragraph is considered as a document.
    """

    def __init__(self):
        lucene.initVM()

    def create_index_dir(self):
        """
        Create the directory where index is stored
        :return: index directory
        """
        path = Paths.get('index')
        indexDir = FSDirectory.open(path)
        return indexDir

    def create_index_writer(self, index_dir):
        """
        Create the index writer
        :param index_dir: the index directory
        :return: index writer object
        """
        writerConfig = IndexWriterConfig(StandardAnalyzer())
        writerConfig.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        #writerConfig.setSimilarity(ClassicSimilarity())
        writer = IndexWriter(index_dir, writerConfig)
        return writer

    def create_searcher(self, index_dir):
        """
        create the index searcher
        :param index_dir: the index directory
        :return: index searcher object
        """
        reader = DirectoryReader.open(index_dir)
        searcher = IndexSearcher(reader)
        return searcher

    def add_documents(self, input_file, writer_obj):
        """
        Read the input file and create the index from the paragraph text
        Each paragraph is one document. Store the document ids, frequencies and
        positions in the index for each term
        :param input_file: the input file used for creating the index
        :param writer_obj: the index writer object
        :return: 
        """
        contentType = FieldType()
        contentType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
        contentType.setStored(True)
        contentType.setTokenized(True)

        paras = get_paragraphs(input_file)
        for p in paras:
            doc = Document()
            lines_split = p.split('|__|')
            doc.add(StringField("id", lines_split[0], Field.Store.YES))
            doc.add(Field("paragraphs", get_stemmed_string(lines_split[1].lower()), contentType))
            writer_obj.addDocument(doc)
        writer_obj.close()

    def index_documents(self, input_file):
        """
        Create index from the input file
        :param input_file: the input file
        :return: index searcher object
        """
        index_directory = self.create_index_dir()
        index_writer = self.create_index_writer(index_directory)
        self.add_documents(input_file, index_writer)
        search_object = self.create_searcher(index_directory)
        return search_object



