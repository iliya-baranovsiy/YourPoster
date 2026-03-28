def unique(array: list):
    seen = set()
    result = []
    for i in array:
        if i[0] not in seen:
            seen.add(i[0])
            result.append(i)
    return result
