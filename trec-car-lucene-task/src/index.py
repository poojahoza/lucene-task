"""
@author: pooja_oza
"""
import sys
from createIndex import CreateIndex
from rankDocuments import RankDocuments
from constructKeywordQuery import get_keyword_queries, get_paragraphs
from utils import get_stemmed_string

RANKING_FUNCTIONS = ['BM25', 'VSM']
DEFAULT_RANK_FUNCTION = 'BM25'

if __name__ == "__main__":

    if len(sys.argv) == 1:
        print('Please enter outline_file ranking_function paragraphs_file')
        print('Usage index.py outline_file ranking_function paragraphs_file')
        exit()

    outlines_file_name = sys.argv[1]
    ranking_function = sys.argv[2]
    paragraphs_file_name = sys.argv[3]
    if ranking_function not in RANKING_FUNCTIONS:
        ranking_function = DEFAULT_RANK_FUNCTION
    output_file_name = 'output_%s.txt'%ranking_function

    create_ind_obj = CreateIndex()
    search_object = create_ind_obj.index_documents(paragraphs_file_name)

    rank_obj = RankDocuments(search_object)
    rank_obj.set_searcher_similarity(ranking_function)

    keyword_queries = get_keyword_queries(outlines_file_name)

    with open(output_file_name,'w') as output_f:
        for query in keyword_queries:
            print(get_stemmed_string(query[1]))
            ranked_data = rank_obj.get_rank_documents(get_stemmed_string(query[1]))
            for data in ranked_data:
                line = '%s Q0 %s %s %s %s \n' % (query[0],
                                                data[0],
                                                str(data[2]),
                                                str(data[1]),
                                                 ranking_function)
                output_f.write(line)
    output_f.close()

