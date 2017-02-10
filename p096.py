# Problem 96
# Solving Sudoku
import copy
from random import shuffle

digits = {d for d in range(1,10)}
sudokuLen = 9
# A Sudoku puzzle is a 9x9 list.
def prettyPrint(puzzle):
    for col in range(sudokuLen):
        for row in range(sudokuLen):
            if isinstance(puzzle[col][row],int):
                print(puzzle[col][row],end=" ")
            else:
                print(".",end=" ")
        print()
    print()
def createSolutionMatrix(p):
    # Pre-process
    s = p.copy()
    for x in range(sudokuLen):
        for y in range(sudokuLen):
            if p[y][x] == '0':
                s[y][x] = [d for d in digits]
            else:
                s[y][x] = int(p[y][x])
    return s
def prepareQueue():
    # Return a queue with all squares in the sudoku matrix
    q = Queue()
    for x in range(sudokuLen):
        for y in range(sudokuLen):
            q.put((x,y))

    return q
def prepareSet(p):
    # Return a set with all the solved squares in the
    # sudoku matrix
    s = set()
    for x in range(sudokuLen):
        for y in range(sudokuLen):
            if isinstance(p[y][x],int):
                s.add((x,y))
    return s
def setValue(x,y,solution,gridSet):
    if isinstance(solution[y][x],int): return
    solution[y][x] = solution[y][x][0]
    gridSet.add((x,y))
    eliminatePossibilities(x,y,solution,gridSet)
def removeValFromSquarePossibilities(x,y,v,solution,gridSet):
    if isinstance(solution[y][x],int): return
    try:
        solution[y][x].remove(v)
        if len(solution[y][x]) == 1:
            setValue(x,y,solution,gridSet)
    except ValueError: pass
def checkForUniqueValuesInRow(y,solution,gridSet):
    for d in digits:
        numOccurrences = 0
        c = -1
        for col in range(sudokuLen):
            if isinstance(solution[y][col],int):
                if solution[y][col] == d:
                    numOccurrences = -1
                    break
            else:
                if d in solution[y][col]:
                    numOccurrences += 1
                    c = col
        if numOccurrences == 0:
#            print("error in row",y,", couldn't find", d)
#            prettyPrint(solution)
            raise Exception()
        elif numOccurrences == 1:
            solution[y][c] = d
            gridSet.add((c,y))
def checkForUniqueValuesInColumn(x,solution,gridSet):
    for d in digits:
        numOccurrences = 0
        r = -1
        for row in range(sudokuLen):
            if isinstance(solution[row][x],int):
                if solution[row][x] == d:
                    numOccurrences = -1
                    break
            else:
                if d in solution[row][x]:
                    numOccurrences += 1
                    r = row
        if numOccurrences == 0:
#            print("error in col",x,", couldn't find", d)
#            prettyPrint(solution)
            raise Exception()
#            print("error in col")
#            exit() # Error
        elif numOccurrences == 1:
            solution[r][x] = d
            gridSet.add((x,r))
def numOccurrencesInSection(d,xMin,yMin,solution):
    numOccurrences = 0
    (posX,posY) = (-1,-1)
    for dx in range(3):
        for dy in range(3):
            if isinstance(solution[yMin+dy][xMin+dx],int):
                if solution[yMin+dy][xMin+dx] == d:
                    numOccurrences = -1
                    return(-1,None,None)
            else:
                if d in solution[yMin+dy][xMin+dx]:
                    numOccurrences += 1
                    (posX,posY) = (xMin+dx,yMin+dy)
    return(numOccurrences,posX,posY)
def checkForUniqueValuesInSection(x,y,solution,gridSet):
    xMin = (x//3)*3
    yMin = (y//3)*3
    for d in digits:
        (numOccurrences,posX,posY) = numOccurrencesInSection(d,xMin,yMin,solution)
        if numOccurrences == -1:
            continue
        elif numOccurrences == 0:
            raise Exception()
#            print("error in section")
#            print(d,xMin,yMin)
#            prettyPrint(solution)
#            exit() # Error
        elif numOccurrences == 1:
            solution[posY][posX] = d
            gridSet.add((posX,posY))
def eliminateInRow(x,y,solution,gridSet):
    for col in range(sudokuLen):
        removeValFromSquarePossibilities(col,y,solution[y][x],solution,gridSet)
def eliminateInColumn(x,y,solution,gridSet):
    for row in range(sudokuLen):
        removeValFromSquarePossibilities(x,row,solution[y][x],solution,gridSet)
def eliminateInSection(x,y,solution,gridSet):
    xMin = (x//3)*3
    yMin = (y//3)*3
    for dx in range(3):
        for dy in range(3):
            removeValFromSquarePossibilities(xMin+dx,yMin+dy,solution[y][x],solution,gridSet)
def eliminatePossibilities(x,y,solution,gridSet):
    eliminateInRow(x,y,solution,gridSet)
    eliminateInColumn(x,y,solution,gridSet)
    eliminateInSection(x,y,solution,gridSet)
    checkForUniqueValuesInRow(y,solution,gridSet)
    checkForUniqueValuesInColumn(x,solution,gridSet)
    checkForUniqueValuesInSection(x,y,solution,gridSet)
def isSolved(p):
    for x in range(sudokuLen):
        for y in range(sudokuLen):
            if not isinstance(p[y][x],int):
                return False
    for row in p:
        if len(set(row)) is not 9:
            print("uh oh!!!")
            exit()
            return False
    return True
def findOccurrencesInRow(digit,puzzle,row):
    occurrences = []
    for col in range(sudokuLen):
        if isinstance(puzzle[row][col],int):
            if puzzle[row][col] == digit:
                return None
        elif digit in puzzle[row][col]:
            occurrences.append((col,row))
    return occurrences
def occurrencesInSameSection(occ):
    if len(occ) > 3:
        return False
    if len(occ) == 3:
        return (occ[0][0]//3 == occ[1][0]//3 and occ[1][0]//3 == occ[2][0]//3 and occ[0][1]//3 == occ[1][1]//3 and occ[1][1]//3 == occ[2][1]//3)
    elif len(occ) == 2:
        return occ[0][0]//3 == occ[1][0]//3 and occ[0][1]//3 == occ[1][1]//3
    else:
        return True
def smartCheckSectionsByRow(puzzle,gridSet):
    # For each row, if say, 2 is only available in the
    # pieces of the row in that section, remove it everywhere
    # else in that section.
    for row in range(sudokuLen):
        sectY = row//3 * 3
        for digit in digits:
            occurrences = findOccurrencesInRow(digit,puzzle,row)
            if occurrences is not None and occurrencesInSameSection(occurrences):
                sectX = occurrences[0][0] // 3 * 3
                for dx in range(3):
                    for dy in range(3):
                        if (sectX+dx,row) not in occurrences:
                            removeValFromSquarePossibilities(sectX+dx,sectY+dy,digit,puzzle,gridSet)
def findOccurrencesInColumn(digit,puzzle,col):
    occurrences = []
    for row in range(sudokuLen):
        if isinstance(puzzle[row][col],int):
            if puzzle[row][col] == digit:
                return None
        elif digit in puzzle[row][col]:
            occurrences.append((col,row))
    return occurrences
def smartCheckSectionsByColumn(puzzle,gridSet):
    for col in range(sudokuLen):
        sectX = col//3 * 3
        for digit in digits:
            occurrences = findOccurrencesInColumn(digit,puzzle,col)
            if occurrences is not None and occurrencesInSameSection(occurrences):
                sectY = occurrences[0][1] // 3 * 3
                for dx in range(3):
                    for dy in range(3):
                        if (col,sectY+dy) not in occurrences:
                            removeValFromSquarePossibilities(sectX+dx,sectY+dy,digit,puzzle,gridSet)
def occurrencesInSameRow(occ):
    if len(occ) > 3:
        return False
    if len(occ) == 3:
        return occ[0][1] == occ[1][1] and occ[1][1] == occ[2][1]
    elif len(occ) == 2:
        return occ[0][1] == occ[1][1]
    else:
        return True
def occurrencesInSameColumn(occ):
    if len(occ) > 3:
        return False
    if len(occ) == 3:
        return occ[0][0] == occ[1][0] and occ[1][0] == occ[2][0]
    elif len(occ) == 2:
        return occ[0][0] == occ[1][0]
    else:
        return True
def findOccurrencesInSection(digit,puzzle,xMin,yMin):
    o = []
    for dx in range(3):
        for dy in range(3):
            if isinstance(puzzle[yMin+dy][xMin+dx],int):
                if puzzle[yMin+dy][xMin+dx] == digit:
                    return None
            elif digit in puzzle[yMin+dy][xMin+dx]:
                o.append((xMin+dx,yMin+dy))
    return o
def smartCheckRowsBySection(puzzle,gridSet):
    for xMin in range(0,sudokuLen,3):
        for yMin in range(0,sudokuLen,3):
            for digit in digits:
                occurrences = findOccurrencesInSection(digit,puzzle,xMin,yMin)
                if occurrences is not None and occurrencesInSameRow(occurrences):
                    # iterate over the row and remove everything not in occurrences
                    row = occurrences[0][1]
                    for col in range(sudokuLen):
                        if (col,row) not in occurrences:
                            removeValFromSquarePossibilities(col,row,digit,puzzle,gridSet)
def smartCheckColumnsBySection(puzzle,gridSet):
    for xMin in range(0,sudokuLen,3):
        for yMin in range(0,sudokuLen,3):
            for digit in digits:
                occurrences = findOccurrencesInSection(digit,puzzle,xMin,yMin)
                if occurrences is not None and occurrencesInSameColumn(occurrences):
                    # iterate over the row and remove everything not in occurrences
                    col = occurrences[0][0]
                    for row in range(sudokuLen):
                        if (col,row) not in occurrences:
                            removeValFromSquarePossibilities(col,row,digit,puzzle,gridSet)

def smartCheck(p,gridSet):
    # If a section is lacking value v, and v is only possible
    # in a row or a column, than we can remove v from that
    # row and column in other sections

    # Similarly, if a row or column is lacking value v, and v is only
    # possible in a given section, then we can remove v from other entries
    # in that section.

    simpleSmartCheck(p,gridSet)

    smartCheckRowsBySection(p,gridSet)
    smartCheckColumnsBySection(p,gridSet)
    smartCheckSectionsByRow(p,gridSet)
    smartCheckSectionsByColumn(p,gridSet)


def simpleSmartCheck(p,gridSet):
    for num in range(sudokuLen):
        checkForUniqueValuesInRow(num,p,gridSet)
        checkForUniqueValuesInColumn(num,p,gridSet)
    for x in range(0,sudokuLen,3):
        for y in range(0,sudokuLen,3):
            checkForUniqueValuesInSection(x,y,p,gridSet)

def checkForUniquesInRow(row,solution,gridSet):
    for col in range(sudokuLen):
        if isinstance(solution[row][col],int): continue
        counter = len(solution[row][col])
        locations = []
        for x in range(sudokuLen):
            if solution[row][x] == solution[row][col]:
                counter -= 1
                locations.append((x,row))
        if counter == 0:
            for x in range(sudokuLen):
                if (x,row) not in locations and not isinstance(solution[row][x],int):
                    for d in solution[row][col]:
                        # remove D from x,row
                        removeValFromSquarePossibilities(x,row,d,solution,gridSet)
            # remove all instances of
        # If the entry has length n, and there are n
        # entries that match it (including itself)
        # then remove all other instances of all its
        # contents from the row
def checkForUniquesInRows(p,gridSet):
    for row in range(sudokuLen):
        checkForUniquesInRow(row,p,gridSet)
def checkForUniquesInColumn(col,solution,gridSet):
    for row in range(sudokuLen):
        if isinstance(solution[row][col],int): continue
        counter = len(solution[row][col])
        locations = []
        for y in range(sudokuLen):
            if solution[y][col] == solution[row][col]:
                counter -= 1
                locations.append((col,y))
        if counter == 0:
            for y in range(sudokuLen):
                if (col,y) not in locations and not isinstance(solution[y][col],int):
                    for d in solution[row][col]:
                        # remove D from x,row
                        removeValFromSquarePossibilities(col,y,d,solution,gridSet)
def checkForUniquesInColumns(p,gridSet):
    for col in range(sudokuLen):
        checkForUniquesInColumn(col,p,gridSet)
def checkForUniquesInSection(x,y,solution,gridSet):
    for dx in range(3):
        for dy in range(3):
            if isinstance(solution[y+dy][x+dx],int): continue
            counter = len(solution[y+dy][x+dx])
            locations = []
            for _dx in range(3):
                for _dy in range(3):
                    if solution[y+_dy][x+_dx] == solution[y+dy][x+dx]:
                        counter -= 1
                        locations.append((x+_dx,y+_dy))
            if counter == 0:
                for _dx in range(3):
                    for _dy in range(3):
                        if (x+_dx,y+_dy) not in locations and not isinstance(solution[y+_dy][x+_dx],int):
                            for d in solution[y+dy][x+dx]:
                                removeValFromSquarePossibilities(x+_dx,y+_dy,d,solution,gridSet)
def checkForUniquesInSections(p,gridSet):
    for x in range(0,sudokuLen,3):
        for y in range(0,sudokuLen,3):
            checkForUniquesInSection(x,y,p,gridSet)
def superSmartCheck(p,gridSet):
    # Look for pairs in the same row/col/sect,
    # for example, if two squares in a row have [2,3],
    # then remove all other 2,3 from that row
    smartCheck(p,gridSet)
    checkForUniquesInSections(p,gridSet)
    checkForUniquesInColumns(p,gridSet)
    checkForUniquesInRows(p,gridSet)

def findGroupOfTwo(p):
    xs = [x for x in range(sudokuLen)]
    ys = [y for y in range(sudokuLen)]
    for x in xs:
        for y in ys:
            if isinstance(p[y][x],int): continue
            elif len(p[y][x]) == 2:
                return (x,y)

    return (-1,-1)

def conditionalSolve(p,first=True):
    q = set()
    (_x,_y) = findGroupOfTwo(p)
    if _x is -1 or _y is -1:
        print("Couldn't find any pairs.")
        exit()
    else:
        _p = copy.deepcopy(p)
        if first:
            choice = 0
        else:
            choice = 1
        try:
            removeValFromSquarePossibilities(_x,_y,_p[_y][_x][choice],_p,q)
        except Exception:
            _p = copy.deepcopy(p)
            choice = (choice + 1) % 2
            removeValFromSquarePossibilities(_x,_y,_p[_y][_x][choice],_p,q)
        q.add((_x,_y))
        while True:
            try:
                (x,y) = q.pop()
            except KeyError:
                if isSolved(_p):
                    return _p
                else:
                    _p = conditionalSolve(_p,first)
            try:
                eliminatePossibilities(x,y,_p,q)
            except Exception:
                return conditionalSolve(p, not first)

def solveSudoku(p):
    solution = createSolutionMatrix(p)
    gridSet = prepareSet(solution)

    iterCount = 1
    while True:
        try:
            (x,y) = gridSet.pop()
            eliminatePossibilities(x,y,solution,gridSet)
        except KeyError:
            if isSolved(solution):
                valueString = "".join(str(s) for s in solution[0][0:3])
                return int(valueString)
            else:
                iterCount += 1
                superSmartCheck(solution,gridSet)
                if iterCount % 5 == 0:
                    solution = conditionalSolve(solution)



if __name__ == "__main__":
    curPuzzle = []
    topLeftSum = 0
    f = open("p096_sudoku.txt")
    lines = f.readlines()
    puzzleCount = 1
    i = 0
    while i < len(lines):
        print(i//10 + 1)
        line = lines[i]
        i += 1
        curPuzzle = []
        for n in range(9):
            line = lines[i]
            i += 1
            curPuzzle.append(list(line.strip()))
        topLeftSum += solveSudoku(curPuzzle)
    print(topLeftSum)
