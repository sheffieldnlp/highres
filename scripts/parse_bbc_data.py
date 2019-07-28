import os
import json
import re
from stanfordcorenlp import StanfordCoreNLP

if __name__ == '__main__':
    p_id = re.compile('\d+')
    file_dir = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/Raw'
    result_doc_dir = "/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/documents"
    result_ref_dir = "/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/summaries/ref"
    nlp = StanfordCoreNLP(r'/home/acp16hh/Data/Dependencies/stanford-corenlp-full-2018-10-05', memory='16g')
    props = {'annotators': 'tokenize,ssplit,pos,lemma,ner,parse,coref', 'coref.algorithm': 'neural',
             'pipelineLanguage': 'en', 'outputFormat': 'json'}
    props2 = {'annotators': 'tokenize, ssplit', 'pipelineLanguage': 'en', 'outputFormat': 'json'}
    for file in os.listdir(file_dir):
        doc_id = p_id.match(file).group()
        is_url = False
        is_title = False
        is_summ = False
        is_body = False
        url = []
        title = []
        summ = []
        body = []
        with open(os.path.join(file_dir, file)) as infile:
            for line in infile:
                line = line.strip()
                if line == '':
                    continue
                if '[SN]URL[SN]' in line:
                    is_url = True
                    is_title = False
                    is_summ = False
                    is_body = False
                    continue
                if '[SN]TITLE[SN]' in line:
                    is_title = True
                    is_url = False
                    is_summ = False
                    is_body = False
                    continue
                if '[SN]FIRST-SENTENCE[SN]' in line:
                    is_summ = True
                    is_body = False
                    is_url = False
                    is_title = False
                    continue
                if '[SN]RESTBODY[SN]' in line:
                    is_body = True
                    is_url = False
                    is_title = False
                    is_summ = False
                    continue
                if is_url:
                    url.append(line)
                if is_title:
                    title.append(line)
                if is_summ:
                    summ.append(line)
                if is_body:
                    body.append(line)
            try:
                resultJSON = nlp.annotate(" ".join(body), properties=props)
                result = json.loads(resultJSON)
            except:
                print(doc_id)
                nlp.close()
                exit(1)
            result['doc_id'] = doc_id
            for sent in result['sentences']:
                del sent['parse']
                del sent['basicDependencies']
                del sent['enhancedDependencies']
                del sent['enhancedPlusPlusDependencies']
                del sent['entitymentions']
                for token in sent['tokens']:
                    del token['lemma']
                    del token['pos']
                    del token['ner']
                    del token['speaker']
                    del token['before']
                    del token['after']
            result['paragraph'] = {}
            result['paragraph']['endSentIndex'] = [0]
            for paragraph in body:
                sents = json.loads(nlp.annotate(paragraph, properties=props2))
                prevLen = len(result['paragraph']['endSentIndex']) - 1
                result['paragraph']['endSentIndex'] \
                    .append(len(sents['sentences']) + result['paragraph']['endSentIndex'][prevLen])
            # del result['paragraph']['endSentIndex'][0]
            with (open(result_doc_dir + "/" + doc_id + ".data", "w")) as outfile:
                json.dump(result, outfile, sort_keys=False)
            with (open(result_ref_dir + "/" + doc_id + ".data", "w")) as outfile:
                outfile.write(summ[0])
    nlp.close()

