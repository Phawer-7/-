from mongoDB import getDefaultTriggerList


def triggerList(getDefault: list) -> dict:
    Tdict = {}
    for i, k in enumerate(getDefault):
        Tdict[i] = k

    return Tdict


def returnWithoutSmiles(name: str) -> str:
    dict2 = triggerList(getDefaultTriggerList())

    new = name
    result = list(new)
    for i in dict2.values():
        for j in i:
            try:
                if new.startswith(j):
                    del result[0:len(j)]
                elif new.endswith(j):
                    del result[result.index(j)]
            except ValueError:
                return 0

    res = "".join(result)
    if len(name) == len(res):
        return 0
    else:
        return res
