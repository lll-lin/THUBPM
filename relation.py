

def direct_relation(trace):
    """
    obtain DS.
    """
    traceDS = {}
    for i in range(len(trace) - 1):
        name = '%s,%s' % (trace[i], trace[i + 1]) 
        traceDS[name] = 1

    return traceDS

def use_dict_store_log(logControlflow):
    '''
    using dict for storing log
    '''
    logDict ={}
    for index, trace in enumerate(logControlflow):
        traceDS = direct_relation(trace)
        DS_set = set()
        for key in traceDS.keys():
            DS_set.add(key)
        logDict[index] = DS_set

    return logDict

def updateDSfreq(DSfreq, traceDS):
    """
    Update DS
    """
    allAboutDSfreq = {}
    for key in traceDS.keys():
        if key in DSfreq.keys():
            DSfreq[key] = DSfreq[key]+1
        else :
            DSfreq[key] = 1


    listDSfre = list(DSfreq.values())
    minfreq = min(listDSfre)

    allAboutDSfreq["DSfreq"] = DSfreq
    allAboutDSfreq["minfreq"] = minfreq

    return allAboutDSfreq



if __name__ == '__main__':
    trace1 = ['a', 'b','c','d',]
    trace2 = ['a', 'c', 'b', 'd', ]
    trace3 = ['a', 'c', 'b', 'd', ]
    DSfreq = {}  # for first
    trace = direct_relation(trace1)
    for key in trace.keys():
        DSfreq[key] = 1
    allAboutDSfreq = updateDSfreq(DSfreq, direct_relation(trace2))
    allAboutDSfreq = updateDSfreq(DSfreq, direct_relation(trace2))
    DS = allAboutDSfreq["DSfreq"]
    print("DS：", DS)