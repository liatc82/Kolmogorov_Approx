# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 22:12:17 2017

@author: liat
"""

import BellmanFord

#import Example448

import time

from Experiments import Example448


def createProbGraphKolmogorov(prob):
    g = {}
    i = 0
    prob[float('-Inf')] = 0
    prob[float('Inf')] = 0
    vals = sorted(list(prob))
    for p in vals:
        g[p] = {}
        j = 0
        for q in vals:
            if q > p:
                sumij = getUnderProbSum(prob, p, q)
                if p == float('-Inf') or q == float('Inf'):
                    g[p][q] = sumij
                else:
                    g[p][q] = sumij / 2
    return g


def createProb(prob, source, p, m):
    s = float('Inf')
    t = float('Inf')
    aProb = {}
    i = m
    edge = False
    while s:
        s = p[i][s]
        if t == float('Inf'):
            aProb[s] = prob[s] + getUnderProbSum(prob, s, t)
        elif s == float('-Inf'):
            aProb[t] = aProb[t] + getUnderProbSum(prob, s, t)
        else:
            aProb[t] = aProb[t] + getUnderProbSum(prob, s, t)/2
            aProb[s] = prob[s] + getUnderProbSum(prob, s, t)/2
        t = s
        i = i - 1
        if s == source: break
    return aProb

def getUnderProbSum(prob, s, t):
    res = 0
    for i in prob.keys():
        if i > s and i < t:
            res = res + prob[i]
    return res


def optTrimKolmog(prob, m):
    m = m + 1
    if len(prob.keys())+1 <= m:
        return prob
    graph = createProbGraphKolmogorov(prob)
    source = float('-Inf')
    d, p = BellmanFord.bellman_ford(graph, source, m + 1)
    p = createProb(prob, source, p, m)
    return p

def sumRandVars(p1, p2):
    p = {}
    for v1 in p1.keys():
        for v2 in p2.keys():
            if (v1 + v2) not in p:
                p[v1 + v2] = 0
            p[v1 + v2] = p[v1 + v2] + p1[v1] * p2[v2]
    return p


def sumOptKolmog(dist, e, n):
    m = int(1 / e) * int(n)
    #m=10
    print("m=",m)
    p = {0: 1}
    for d in dist:
        p_org = sumRandVars(p, d)
        p = optTrimKolmog(p_org, m)
    return p


def sumAccurate(dist):
    p = {0: 1}
    for d in dist:
        p = sumRandVars(p, d)
    return p


def lessThanT(dist, T):
    prob = 0
    for key in dist:
        if (key <= T):
            prob = prob + dist[key]
    return prob


def lessThanAllT(dist, distapx):
    d = {}
    for key in dist:
        d[key] = lessThanT(distapx, key) - lessThanT(dist, key)
    return d


def error(dist, distapx):
    d = {}
    for key in dist:
        d[key] = abs(lessThanT(distapx, key) - lessThanT(dist, key))
    return max(list(d.values()))

def checkSumOne(dist):
    ssum = 0
    for key in dist:
        ssum = ssum + dist[key]



def test():
    x=2
    # dist=[{1:0.5, 10:0.5},{2:0.5, 20:0.5},{3:0.5, 30:0.5},{4:0.5, 40:0.5}]
    # S =sumAccurate(dist)
    # Sapx = sumOptTrim(dist,4,1)
    # print (S, Sapx)
    # print (lessThanAllT(S, Sapx))
#    prob1 = {1: 0.3333, 20: 0.12, 6: 0.16666, 4: 0.1, 12: 0.08, 100: 0.05, 50: 0.15}
#    prob = {1: 0.3333, 2: 0.3333, 3: 0.16666, 4: 0.16666}
#    prob2 = {(1, 1): 0.16666, (1, 2): 0.16666, (2, 1): 0.16666, (2, 2): 0.16666, (3, 1): 0.16666, (4, 1): 0.16666}
#    probapx2 = {(1, 1): 0.16666, (1, 2): 0.33333, (3, 1): 0.5}
#    probapx = {1: 0.4, 2: 0.4, 4: 0.2}
#     appxprob = optTrimKolmog(Example448.prob,40)
#     print(appxprob)
#     print('****************************************************************************')
#     print(error(Example448.prob, appxprob))
    #exp = {2:0.2, 4:0.2, 6:0.2, 8:0.2, 10:0.2}
    #appx10rv5 = {315.55: 0.2, 328.635: 0.2, 340.0455: 0.2, 342.2835: 0.2, 355.7835: 0.2}

    # appxprob = optTrimKolmog(Example448.sumtenrandvars,110)
    # print(appxprob)
    # print('****************************************************************************')
    # print(error(Example448.sumtenrandvars, appxprob))
    # n=8
    # x = {}
    # for i in range(n):
    #     x[i] = 1.0/n
    #
    # xx = optTrimKolmog(x,5)
    # print(xx)
    # print('****************************************************************************')
    # xxopt = {0:0.125,1:0.1875,3:0.25,5:0.25,7:0.1875}
    # print(error(x, xx))
    # print(error(x, xxopt))




if __name__ == '__main__': test()
