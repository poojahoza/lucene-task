from trec_car.read_data import iter_annotations, iter_paragraphs, ParaText
import re


def get_keyword_queries(input_outlines_file):
    page_details = []
    with open(input_outlines_file, 'rb') as f:
        for p in iter_annotations(f):
            page_details.append((p.page_id, p.page_name))
            outline_headings = p.flat_headings_list()
            for outline in outline_headings:
                headlines = " ".join([p.page_name] + [re.sub('[^a-zA-Z0-9 \n]', '', section.heading) for section in outline])
                headlines_id = "/".join([p.page_id] + [section.headingId for section in outline])
                page_details.append((headlines_id, headlines))

    return page_details

def get_paragraphs(paragraphs_file):
    with open(paragraphs_file, 'rb') as f:
        for p in iter_paragraphs(f):
            texts = [elem.text if isinstance(elem, ParaText)
                 else elem.anchor_text
                 for elem in p.bodies]
            yield p.para_id+'|__|'+(' '.join(texts))
