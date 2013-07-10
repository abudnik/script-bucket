import random
import itertools

def PrintMat(mat):
    size = len(mat)
    for i in range(size):
        s = ""
        for j in range(size):
            s += ' ' + str(mat[i][j]) + ' '
        print s

def PrintSolution(s, mat, size):
    sum = 0
    for e in s:
        sum += mat[e[0]][e[1]]
    print sum
    out = []
    for i in range(size):
         out.append( [mat[i][j] for j in range(size)] )
    for e in s:
        out[e[0]][e[1]] = '*'
    PrintMat(out)

def GenerateMatrix(mat, size):
    for i in range(size):
         mat.append( [random.randint(0,9) for j in range(size)] )

def BruteForce(mat, size):
    s = [[0,0] for i in range(size)]
    best_sum = 0
    permut = itertools.permutations(range(size))
    for p in permut:
        sum = 0
        for i in range(size):
            sum += mat[p[i]][i]
        if sum > best_sum:
            best_sum = sum
            for i in range(size):
                s[i][0] = p[i]
                s[i][1] = i
    return s

def M1(mat, size):
    s = [[0,0] for i in range(size)]
    array = []
    for i in range(size):
        for j in range(size):
            array.append((mat[i][j],i,j))
    array.sort(key=lambda x: x[0], reverse=True)

    best_sum = 0
    for i in range(size*size):
        temp = [array[i]]
        sum = array[i][0]
        avail_row = [True for j in range(size)]
        avail_col = [True for j in range(size)]
        avail_row[array[i][1]] = False
        avail_col[array[i][2]] = False
        for j in range(size*size):
            if not avail_row[array[j][1]] or not avail_col[array[j][2]]:
                continue
            temp.append(array[j])
            avail_row[array[j][1]] = False
            avail_col[array[j][2]] = False
            sum += array[j][0]
            if len(temp) == size:
                break

        if sum < best_sum:
            break

        if sum > best_sum:
            best_sum = sum
            for j in range(size):
                s[j] = temp[j][1:]

    return s

def Main():
    size = 9
    mat = []
    GenerateMatrix(mat, size)
    PrintMat(mat)

    s = BruteForce(mat, size)
    PrintSolution(s, mat, size)

    s = M1(mat, size)
    PrintSolution(s, mat, size)

Main()
