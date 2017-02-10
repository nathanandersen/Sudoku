# Problem 96
total = 0
# Memory model:
# a 81-length list

def sameRow(i,j):
    return (i//9 == j//9)

def sameCol(i,j):
    return ((i-j)%9 == 0)

def sameSection(i,j):
    return (i//27 == j//27 and (i % 9)//3 == (j % 9)//3)


def solve(puzzArr):
    if puzzArr == "": return
#    print(puzzArr)
    global total
    i = puzzArr.find('0')
    if i is -1:
        total += int(puzzArr[0:3])
        return
    invalidOptions = set()
    for j in range(81):
        if sameRow(i,j) or sameCol(i,j) or sameSection(i,j):
            invalidOptions.add(puzzArr[j])
#    print(invalidOptions)
    for option in '123456789':
        if option not in invalidOptions:
            solve(puzzArr[:i] + option + puzzArr[i+1:])


if __name__ == "__main__":
    f = open("p096_sudoku.txt")
    curPuzzle = ""
    num = 1
    for line in f:
        if line.startswith("Grid"):
            print(num)
            solve(curPuzzle)
            curPuzzle = ""
            num += 1
        else:
            curPuzzle += line.strip()

    print(total)
