import math
import praseLog
import relation

"""
- Sudden drift
author: leilei lin
email : leilei_lin@126.com 
"""
def calculate( w1, w2, sp,logDict):
    changepoints = []

    index = 0
    windowIndex = 0
    steadyStateDSset = set()
    steadyStateDSset_list = []

    disappeared_dict = {}  
    disappear_set = set()

    while index < len(logDict):
        traceDS = logDict[index]

        if windowIndex < w1:
            for key in traceDS:
                steadyStateDSset.add(key)  # keySet
            windowIndex = windowIndex + 1

        elif windowIndex < (w1 + w2):
            isnotCut = traceDS.issubset(steadyStateDSset)
            if not isnotCut:
                changepoints.append(index)
                index = index - 1
                windowIndex = 0
                steadyStateDSset.clear()
                disappeared_dict.clear()
            else:
                for DS in traceDS:
                    if DS not in disappeared_dict.keys():
                        disappeared_dict[DS] = 1
                    else:
                        disappeared_dict[DS] = 1 + disappeared_dict[DS]
                windowIndex = windowIndex + 1

        else:
            isDisappearCut = isCutfromDisappear(disappeared_dict, steadyStateDSset)
            if isDisappearCut:
                startIndexW2 = index - w2
                indexChange = candidateDisappear(steadyStateDSset, disappeared_dict, logDict, startIndexW2, index, sp)

                changepoints.append(indexChange)
                index = indexChange - 1
                windowIndex = 0
                steadyStateDSset.clear()
                disappeared_dict.clear()

            elif not isDisappearCut:
                # move w2

                startIndexW2 = index - w2
                for DS in logDict[startIndexW2]:   
                    disappeared_dict[DS] = disappeared_dict[DS] - 1
                    if disappeared_dict[DS] == 0:
                        del  disappeared_dict[DS]

                windowIndex = windowIndex - 1
                index = index - 1

        index = index + 1

    return changepoints

def candidateDisappear(steadyStateDSset, disappeared_dict, logDict, startIndexW2, index, maxRadius):

    iterIndex = startIndexW2
    storeDisappeaedDS_set = set()
    trueChangePoint = startIndexW2
    radius = maxRadius

    while iterIndex < index:
        DSsetIntrace = set(disappeared_dict)
        diffenretDSset = steadyStateDSset.difference(DSsetIntrace)

        if len(diffenretDSset) > 1:  
            notSame_disappeared_DS = diffenretDSset.difference(storeDisappeaedDS_set)
            if len(notSame_disappeared_DS) > 1: 
                radius = maxRadius
                trueChangePoint = iterIndex
                for DS in notSame_disappeared_DS:
                    storeDisappeaedDS_set.add(DS)
            else:  
                radius = radius - 1
                if radius == 0:
                    break

        for DS in logDict[iterIndex]:  
            disappeared_dict[DS] = disappeared_dict[DS] - 1
            if disappeared_dict[DS] == 0:
                del disappeared_dict[DS]
        iterIndex = iterIndex + 1


    return trueChangePoint


def isCutfromDisappear(disappeared_dict, stateSteadyset):
    iscut = False

    DSsetIntrace = set(disappeared_dict)  

    diffenretDSset = stateSteadyset.difference(DSsetIntrace)

    if len(diffenretDSset) > 1:
        # print("disappeared DS：%s" % diffenretDSset)
        iscut = True

    return iscut



def main():
    usage = """\
    usage:
        python driftDetection.py [-w value] [-r value] [-p value] log_file_path
    options:
        -w complete window size, integer, default value is 200
        -r detection window size, integer, default value is 200
        -p stable period, integer, default value is 10
        """
    import getopt, sys

    try:
        opts, args = getopt.getopt(sys.argv[1:], "w:r:p:")
        if len(args) == 0:
            print(usage)
            return

        complete_window_size = 200
        detection_window_size = 200
        stable_period = 10
        for opt, value in opts:
            if opt == '-w':
                complete_window_size = int(value)
            elif opt == '-r':
                detection_window_size = int(value)
        print("------------------------------------------------------------------------------")
        print("Log: ", args[0])
        print("complete window size: ", complete_window_size)
        print("detection window size: ", detection_window_size)
        print("stable period: ", stable_period)
        print("------------------------------------------------------------------------------")

        logControlflow = praseLog.PraseLogMXML(args[0])
        logDict = relation.use_dict_store_log(logControlflow)
        result = calculate(complete_window_size, detection_window_size, stable_period, logDict)
        print("All change points detected: ", result)
    except getopt.GetoptError:
        print(usage)
    except SyntaxError as error:
        print(error)
        print(usage)

    return 0



if __name__ == '__main__':

    main()