"""
@author: pooja_oza
"""
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search.similarities import ClassicSimilarity, BM25Similarity
from org.apache.lucene.search import TermQuery, BooleanQuery, BooleanClause
from org.apache.lucene.index import Term


class RankDocuments(object):

    def __init__(self, searcher):
        self.search_object = searcher

    def set_searcher_similarity(self, sim):
        if sim == 'BM25':
            self.search_object.setSimilarity(BM25Similarity())
        else:
            self.search_object.setSimilarity(ClassicSimilarity())

    @staticmethod
    def parse_query(query, fieldname):
        query_parser_obj = QueryParser(fieldname, StandardAnalyzer())
        query_parser = query_parser_obj.parse(query)
        return query_parser

    @staticmethod
    def parse_boolean_query(query, fieldname):
        boolean_query = BooleanQuery.Builder()
        for token in query.split(' '):
            boolean_query.add(TermQuery(Term(fieldname, token)), BooleanClause.Occur.SHOULD)
        return boolean_query.build()


    @staticmethod
    def score_documents(searcher, query_parser):
        hits = searcher.search(query_parser, 100)
        ranking_documents = []
        for ind, document in enumerate(hits.scoreDocs):
            each_doc = searcher.doc(document.doc)
            # print(each_doc.get("id"))
            # print(searcher.explain(query_parser, document.doc))
            ranking_documents.append((each_doc.get("id"), document.score, ind+1))
        return ranking_documents

    def get_rank_documents(self, query):
        #query_parser_obj = self.parse_query(query, "paragraphs")
        query_parser_obj = self.parse_boolean_query(query, "paragraphs")
        documents = self.score_documents(self.search_object, query_parser_obj)
        print(documents)
        return documents

    def phrase_documents(self, query_obj):
        documents = self.score_documents(self.search_object, query_obj)
        print(documents)
        return documents