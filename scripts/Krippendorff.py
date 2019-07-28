#! /usr/bin/env python
# -*- coding: utf-8
'''
Python implementation of Krippendorff's alpha -- inter-rater reliability
(c)2011-17 Thomas Grill (http://grrrr.org)
Python version >= 2.4 required
'''

from __future__ import print_function

try:
    import numpy as np
except ImportError:
    np = None


def nominal_metric(a, b):
    return a != b


def interval_metric(a, b):
    return (a - b) ** 2


def ratio_metric(a, b):
    return ((a - b) / (a + b)) ** 2


def krippendorff_alpha(data, metric=interval_metric, force_vecmath=False, convert_items=float, missing_items=None):
    '''
    Calculate Krippendorff's alpha (inter-rater reliability):

    data is in the format
    [
        {unit1:value, unit2:value, ...},  # coder 1
        {unit1:value, unit3:value, ...},   # coder 2
        ...                            # more coders
    ]
    or
    it is a sequence of (masked) sequences (list, numpy.array, numpy.ma.array, e.g.) with rows corresponding to coders and columns to items

    metric: function calculating the pairwise distance
    force_vecmath: force vector math for custom metrics (numpy required)
    convert_items: function for the type conversion of items (default: float)
    missing_items: indicator for missing items (default: None)
    '''

    # number of coders
    m = len(data)

    # set of constants identifying missing values
    if missing_items is None:
        maskitems = []
    else:
        maskitems = list(missing_items)
    if np is not None:
        maskitems.append(np.ma.masked_singleton)

    # convert input data to a dict of items
    units = {}
    for d in data:
        try:
            # try if d behaves as a dict
            diter = d.items()
        except AttributeError:
            # sequence assumed for d
            diter = enumerate(d)

        for it, g in diter:
            if g not in maskitems:
                try:
                    its = units[it]
                except KeyError:
                    its = []
                    units[it] = its
                its.append(convert_items(g))

    units = dict((it, d) for it, d in units.items() if len(d) > 1)  # units with pairable values
    n = sum(len(pv) for pv in units.values())  # number of pairable values

    if n == 0:
        raise ValueError("No items to compare.")

    np_metric = (np is not None) and ((metric in (interval_metric, nominal_metric, ratio_metric)) or force_vecmath)

    Do = 0.
    for grades in units.values():
        if np_metric:
            gr = np.asarray(grades)
            Du = sum(np.sum(metric(gr, gri)) for gri in gr)
        else:
            Du = sum(metric(gi, gj) for gi in grades for gj in grades)
        Do += Du / float(len(grades) - 1)
    Do /= float(n)

    if Do == 0:
        return 1.

    De = 0.
    for g1 in units.values():
        if np_metric:
            d1 = np.asarray(g1)
            for g2 in units.values():
                De += sum(np.sum(metric(d1, gj)) for gj in g2)
        else:
            for g2 in units.values():
                De += sum(metric(gi, gj) for gi in g1 for gj in g2)
    De /= float(n * (n - 1))

    return 1. - Do / De if (Do and De) else 1.


if __name__ == '__main__':
    new_results = ''
    file = open('fluency_dir.csv', 'r')
    model = dict()
    q_number = dict()
    for line in file:
        split = line.split('\t')
        model[split[0].strip()] = split[1].strip()
        q_number[split[0].strip()] = int(split[2].strip()) - 1
    file.close()
    file = open('krip_result.csv', 'r')
    import numpy as np
    rate = dict()
    guided_data = []
    unguided_data = []

    for line in file:
        split = line.split(',')
        g_data = []
        u_data = []
        for j in range(33):
            g_data.append('*')
            u_data.append('*')
        _, score = split[3].split('|')
        if int(score) <= 2:
            continue

        for result in split[1:]:

            if result == '\n':
                continue
            question, score = result.split('|')
            new_results += '{} {}\n'.format(question.strip(), score.strip())
            if '100' in question or '101' in question or '102' in question:
                continue
            question = question.strip()
            score = int(score)
            if model[question] == 'guided':
                g_data[q_number[question]] = score
            elif model[question] == 'unguided':
                u_data[q_number[question]] = score
        guided_data.append(g_data)
        unguided_data.append(u_data)
    missing = '*'  # indicator for missing values

    print("interval metric: %.3f" % krippendorff_alpha(guided_data, interval_metric, missing_items=missing))

    print("interval metric: %.3f" % krippendorff_alpha(unguided_data, interval_metric, missing_items=missing))

    file.close()
    file = open('new_result.csv', 'w')
    file.write(new_results)
    file.close()
