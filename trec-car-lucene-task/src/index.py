"""
@author: pooja_oza
"""
import sys
from createIndex import CreateIndex
from rankDocuments import RankDocuments

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print 'Please enter query'
        print 'Usage index.py query'
        exit()
    user_input = ' '.join(sys.argv[1:])
    print 'Given Query: %s' % user_input
    create_ind_obj = CreateIndex()
    search_object = create_ind_obj.index_documents('paragraphs_input.txt')

    rank_obj = RankDocuments(search_object)
    rank_obj.get_rank_documents(user_input)
    # phrase_query = PhraseQuery.Builder()
    # phrase_query.add(Term("contents", "hot-dog"))
    # phrase_query.add(Term("contents", "rodeo"))
    # pq = phrase_query.build()
    # rank_obj.phrase_documents(pq)