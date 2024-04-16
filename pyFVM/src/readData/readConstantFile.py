def read_faces_file(
    path:str="./faces"
) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    count = 0
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").replace(";", " ").split()
        if len(line) == 0:
            count += 1
            continue
        # 判断并赋值the_number_of_faces
        if line[0].isnumeric():
            the_number_of_faces = int(line[0])
            count += 1
            break
        count += 1
    # 从(后的数字开始赋值data
    lines = lines[count:]
    count = 0
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            count += 1
            continue
        if line[0] == "(":
            count += 1
            break
        count += 1
    lines = lines[count:]
    # 开始赋值data
    i = 0
    data = [[] for _ in range(the_number_of_faces)]
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").split()
        if len(line) == 0:
            break
        data[i].extend(line[1:])
        i += 1
    # 把data中的str转变为int
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    return [data, the_number_of_faces]

def read_boundary_file(
    path:str="./boundary",
) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    count = 0
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").replace(";", " ").split()
        if len(line) == 0:
            count += 1
            continue
        # 判断并赋值the_number_of_boundaries
        if line[0].isnumeric():
            the_number_of_boundaries = int(line[0])
            count += 1
            break
        count += 1
    # 从(后的数字开始赋值data
    lines = lines[count:]
    count = 0
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            count += 1
            continue
        if line[0] == "(":
            count += 1
            break
        count += 1
    lines = lines[count:]
    # 开始赋值data
    data = {}
    for line in lines:
        line = line.strip().replace(";", " ").split()
        if len(line) == 0:
            continue
        if line[0] == ")":
            break
        if line[0] == "{" or line[0] == "}":
            continue
        if len(line) == 1:
            key = line[0]
            data[key] = {}
            continue
        data[key][line[0]] = line[1]
    # 将data中的str变成int
    for key, value in data.items():
        for k, v in value.items():
            if v.isnumeric():
                data[key][k] = int(v)
    return [data, the_number_of_boundaries]


def read_neighbour_file(
    path:str="./neighbour"
) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    count = 0
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").replace(";", " ").split()
        if len(line) == 0:
            count += 1
            continue
        # 判断并赋值the_number_of_face2pointsID
        if line[0].isnumeric():
            the_number_of_internalFaces = int(line[0])
            count += 1
            break
        # 取note.nFaces的值
        from src.readData import extract_number_from_str
        if line[0] == "note":
            strNumCells = line[2]
            the_number_of_elements = extract_number_from_str(strNumCells)
            count += 1
    # 从(后的数字开始赋值data
    lines = lines[count:]
    count = 0
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            count += 1
            continue
        if line[0] == "(":
            count += 1
            break
        count += 1
    lines = lines[count:]
    # 开始赋值data
    i = 0
    data = [[] for _ in range(the_number_of_internalFaces)]
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            continue
        if line[0] == ")":
            break
        data[i].extend(line)
        i += 1
    # 把data中的str转变为int
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    return [data, the_number_of_internalFaces, the_number_of_elements]

def read_owner_file(
    path:str="./owner"
) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    count = 0
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").replace(";", " ").split()
        if len(line) == 0:
            continue
        # 判断并赋值the_number_of_face2pointsID
        if line[0].isnumeric():
            the_number_of_faces = int(line[0])
            count += 1
            break
        count += 1
    # 从(后的数字开始赋值data
    lines = lines[count:]
    count = 0
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            count += 1
            continue
        if line[0] == "(":
            count += 1
            break
        count += 1
    lines = lines[count:]
    # 开始赋值data
    i = 0
    data = [[] for _ in range(the_number_of_faces)]
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            continue
        if line[0] == ")":
            break
        data[i].extend(line)
        i += 1
    # 把data中的str转变为int
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = int(data[i][j])
    return [data, the_number_of_faces]

def read_points_file(
    path:str="./points"
) -> list:
    with open(path, 'r') as file:
        lines = file.readlines()
    count = 0
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").replace(";", " ").split()
        if len(line) == 0:
            count += 1
            continue
        # 判断并赋值the_number_of_pointsCoordinate
        if line[0].isnumeric():
            the_number_of_pointsCoordinate = int(line[0])
            count += 1
            break
        count += 1
    # 从(后的数字开始赋值data
    lines = lines[count:]
    count = 0
    for line in lines:
        line = line.strip().split()
        if len(line) == 0:
            count += 1
            continue
        if line[0] == "(":
            count += 1
            break
        count += 1
    lines = lines[count:]
    # 开始赋值data
    i = 0
    data = [[] for _ in range(the_number_of_pointsCoordinate)]
    for line in lines:
        line = line.strip().replace("(", " ").replace(")", " ").split()
        if len(line) == 0:
            break
        data[i].extend(line)
        i += 1
    # 把data中的str转变为int
    for i in range(len(data)):
        for j in range(len(data[i])):
            data[i][j] = float(data[i][j])
    return [data, the_number_of_pointsCoordinate]


