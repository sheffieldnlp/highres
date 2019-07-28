import os

def remove_sos_eos_lines(alist):
    result = []
    for line in alist:
        line = line.strip()
        l_result = []
        lines = line.split()
        for l in lines:
            if l == '<sos>':
                continue
            if l == '<eos>':
                continue
            l_result.append(l)
        result.append(' '.join(l_result))
    return result

if __name__ == '__main__':
    file_out = open('/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/topic1024+embedded+512_highres.out')
    file_name = open('/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/highres.filename')
    folder = '/home/acp16hh/Projects/Research/Experiments/Exp_Elly_Human_Evaluation/src/Mock_Dataset_2/BBC/summaries/system_topic'
    summs = remove_sos_eos_lines(file_out.readlines())
    names = file_name.readlines()
    for i, name in enumerate(names):
        f_write = open(os.path.join(folder, name.split('.')[0] + '.data'), 'w')
        f_write.write(summs[i])
        f_write.close()

