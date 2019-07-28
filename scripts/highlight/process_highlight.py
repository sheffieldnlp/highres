"""
Extract results from database and then perform analysis on top of to draw insights
"""
from backend.models import Dataset, Document, Summary, SummaryGroup
from backend.app import create_app
from flask_sqlalchemy import SQLAlchemy
import json
from nltk.util import ngrams


def process_doc(results):
    """
    Build indexes and texts for the given document
    """
    indexes = []
    texts = []
    for result_id, data in results.items():
        for h_id, highlight in data['highlights'].items():
            indexes.extend(highlight['indexes'])
            texts.append(highlight['text'])
    return indexes, texts


def sanity_check(results, components, comp_types):
    """
    Check whether the components indexing agree with the result
    """
    for result_id, data in results.items():
        for h_id, highlight in data['highlights'].items():
            from_doc = [components[idx] for idx in sorted(highlight['indexes'])
                        if comp_types[idx] == 'word']
            assert ' '.join(from_doc) == highlight['text']


def calc_ref_overlap(summ, texts):
    summ_text = summ.text.split()
    h_text = ' '.join(texts).split()
    ngram_overlap = []
    for i in range(1, 4):
        summ_text_ngrams = list(set(list(ngrams(summ_text, i))))
        h_text_ngrams = list(set(list(ngrams(h_text, i))))
        overlap = len([token for token in h_text_ngrams
                            if token in summ_text_ngrams]) \
                  / len(summ_text_ngrams)
        ngram_overlap.append(overlap)
    return ngram_overlap


def calc_doc_overlap(components, comp_types, h_idxs):
    """
    Calculate word overlap ratio between document and highlights
    """
    h_idxs = set(h_idxs)

    h_idxs = [idx for idx in h_idxs if comp_types[idx] == 'word']
    len_h_idxs_words = len(h_idxs)
    print(len_h_idxs_words)
    len_components_words = len([idx for idx, _ in enumerate(components)
                                if comp_types[idx] == 'word'])

    return len_h_idxs_words/len_components_words


def parse(doc_json):
    """
    Parse document into components (list of all tokens) and comp_types (list of types for all tokens)
    """
    components = []
    comp_types = []
    for sent in doc_json['sentences']:
        for idx, token in enumerate(sent['tokens']):
            aWord = token['word']
            if token['word'] == '-LRB-':
                aWord = '('
            elif token['word'] == '-RRB-':
                aWord = ')'
            elif token['word'] == '``':
                aWord = '"'
            elif token['word'] == '\'\'':
                aWord = '"'
            components.append(aWord)
            comp_types.append('word')
            if idx != len(sent['tokens']) - 2:
                components.append(' ')
                comp_types.append('whitespace')
    return components, comp_types


def main():
    """
    The main program measures:
    - Overlap between the document and its highlights
    """
    #%%
    app = create_app()
    db = SQLAlchemy(app)
    results_dir = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/results'
    q_results = db.session.query(Summary, SummaryGroup, Document, Dataset)\
        .join(Document).join(SummaryGroup).join(Dataset)\
        .filter(Dataset.name == 'BBC', SummaryGroup.name == 'BBC_ref_gold').all()
    #%%
    for summ, _, doc, _ in q_results:
        print('Document %s' % doc.doc_id)
        doc_json = json.loads(doc.doc_json)
        components, comp_types = parse(doc_json)
        results = doc_json['results']
        sanity_check(results, components, comp_types)
        indexes, texts = process_doc(results)
        overlap = calc_doc_overlap(components, comp_types, indexes)
        ngram_overlap = calc_ref_overlap(summ, texts)
        print(overlap)

if __name__ == '__main__':
    main()

