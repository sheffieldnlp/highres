import os

if __name__ == '__main__':
    file_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/all-model-predictions.txt'
    with open(file_path, 'r') as infile:
        firstLine = True
        name = False
        ptgen = False
        t_convs2s = False
        gold = False
        summaries = dict()
        filename = ''
        for line in infile:
            line = line.strip()
            if line == '':
                continue
            if firstLine:
                filename = line.split()[1]
                summaries[filename] = dict()
                firstLine = False
                continue
            if '==' in line:
                name = True
                continue
            if name:
                filename = line.split()[1]
                summaries[filename] = dict()
                name = False
                continue
            if 'PTGen' in line:
                ptgen = True
                continue
            if ptgen:
                summaries[filename]['PTGen'] = line
                ptgen = False
                continue
            if 'T-ConvS2S' in line:
                t_convs2s = True
                continue
            if t_convs2s:
                summaries[filename]['T-ConvS2S'] = line
                t_convs2s = False
                continue
            if 'GOLD' in line:
                gold = True
                continue
            if gold:
                summaries[filename]['GOLD'] = line
                gold = False
                continue
    raw_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/Raw'
    for file in os.listdir(raw_path):
        if 'json' in file:
            name = file.split('.')[0]
            gold_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/summaries/ref'
            with open(os.path.join(gold_path, name+'.data'), 'w') as infile:
                infile.write(summaries[name]['GOLD'])
            pt_gen_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/summaries/ptgen'
            with open(os.path.join(pt_gen_path, name+'.data'), 'w') as infile:
                infile.write(summaries[name]['PTGen'])
            t_convs2s_path = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/summaries/tconvs2s'
            with open(os.path.join(t_convs2s_path, name+'.data'), 'w') as infile:
                infile.write(summaries[name]['T-ConvS2S'])

