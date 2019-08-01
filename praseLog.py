from lxml import etree



def PraseLogMXML(path):
    """
    Each trace is a list, and each element in list is a dict

    """

    # ALL trace
    traces = []

    # events 
    events = set()

    """
    - process
    - ProcessInstance(*)
    - AuditTrailEntry(*)
    """

    # root = ElementTree.parse(self.path)
    tree = etree.parse(path)
    root = tree.getroot()
    process = root.xpath('./Process')[0]  
    allTraces = process.xpath('./ProcessInstance')

    for case in allTraces:
        trace = []
        # print(node)
        trace.append(case.attrib["id"])  
        for subNode in case.iterfind('AuditTrailEntry'):
            dictEvent = praseNode(subNode)
            trace.append(dictEvent)  
            events.add(dictEvent["name"])

        traces.append(trace)  

    traceControlFlow = onlyControlFlow(traces)

    return traceControlFlow

def praseNode(node):
    """
    - AuditTrailEntry
    - WorkflowModelElement(e.g. a, b)
    - EventType (e.g. assign, complete)
    - Timestamp (e.g. 2005-02-07T15:30:00.000+00:00)
    """
    dictEvent = dict()
    for item in node:
        if item.tag == 'WorkflowModelElement':
            dictEvent['name'] = item.text.strip()
        elif item.tag == 'EventType':
            dictEvent['type'] = item.text.strip()  
        elif item.tag == 'Timestamp':
            dictEvent['timestamp'] = item.text.strip()
    return dictEvent

def onlyControlFlow(traces):
    """
    - focus on control flow
    """
    listControl = []
    for t in traces:
        tempTrace = []
        t.pop(0)  
        for t_event in t:
            if t_event['type'] == "complete":  
                tempTrace.append(t_event['name'])
            else:
                pass
        listControl.append(tempTrace)
    return listControl


if __name__ == '__main__':
    
    controlFlow = PraseLogMXML("../data/Maaradji/logs/cm/cm2.5k.mxml")
    # print("log：", controlFlow)
    for i,value in enumerate(controlFlow):
        if i < 50:
            print("trace：", value)

