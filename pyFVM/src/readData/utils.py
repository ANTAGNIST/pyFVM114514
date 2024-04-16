def unique(ls_1D:list)->list:
    """
    :param ls_1D: 类似[0,0,3,2,4,4]的一维列表
    :return: 返回ls_1D中的唯一的数字[0,3,2,4]
    """
    ls_temp = []
    for l in ls_1D:
        if l in ls_temp:
            continue
        ls_temp.append(l)
    return ls_temp

def extract_number_from_str(line:str):
    data = ""
    for l in line:
        if l.isnumeric():
            data = data + l
    data = data.split()[0]
    data = int(data)
    return data