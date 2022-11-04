from mongoDB import getDefaultTriggerList
from mongoDB import getDefaultTriggerList2


def triggerList(getDefault: list) -> dict:
    Tdict = {}
    for i, k in enumerate(getDefault):
        Tdict[i] = k

    return Tdict


def returnWithoutSmiles(name: str) -> str:
    dict2 = triggerList(getDefaultTriggerList2())
    new = name

    result = [i for i in list(new) if not i == ' ']
    q = list(new)
    for i in dict2.values():
        for j in i:
            if new.startswith(j):
                y = [i for i in q[:len(j)] if not i == ' ']
                del result[:len(y)]
            elif new.endswith(j):
                try:
                    ind = "".join(result).index(j)
                    if ind+1 == len(result):
                        del result[ind]
                    else:
                        del result[ind:]
                except ValueError:
                    pass

    res = "".join(result)
    if res[:3] in new:
        o = new.find(res[:3])
        p = new.find(res[-3:])

        res = new[o:p+3]

    if len(name) == len(res):
        return 0
    else:
        return res
