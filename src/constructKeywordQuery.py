from trec_car.read_data import iter_annotations


def get_keyword_queries(input_outlines_file):
    page_details = []
    with open(input_outlines_file, 'rb') as f:
        for p in iter_annotations(f):
            page_details.append((p.page_id, p.page_name))

    return page_details
