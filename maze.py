import sys

# Or use I/O to read .txt, and must convert hashtag into other symbols
# 2 means wall
maze = [[2,2,2,2,2,2],
        [0,0,2,2,2,2],
        [2,0,2,2,2,2],
        [2,0,2,2,2,2],
        [2,0,0,0,0,0],
        [2,2,2,2,2,2]]

# Read file
with open ("maze.txt") as m:
    fmaze = []
    for row in m:
        frow = []
        for col in row:
            if col == "#":
                frow.append(2)
            elif col == "\n":
                break
            else:
                frow.append(0)
        fmaze.append(frow)
        print(frow)
                
print(maze)
print(fmaze)
#maze = fmaze

#Go upside function
def goUp(location):
    #If it is the topmost, return False
    if(location[1]== 0):
        return False
    else:
        #If it is not the topmost, go up
        newLocation = [location[0], location[1]-1]
        #If it have been there, return False
        if newLocation in routeHistory:
            return False
        #If it is wall, return False
        elif maze[newLocation[0]][newLocation[1]] == 2:
            return False
        #If the position is right, return True
        else:
            rightRoute.append(newLocation)
            routeHistory.append(newLocation)
            return True
        
#the same as goup method - down, left, right
def goDown(location):
     if(location[1]==5):
        return False
     else:
        newLocation = [location[0], location[1]+1]
        if newLocation in routeHistory:
            return False       
        elif maze[newLocation[0]][newLocation[1]] == 2:
            return False
        else:
            rightRoute.append(newLocation)
            routeHistory.append(newLocation)
            return True

def goLeft(location):
    if(location[0]==0):
        return False
    else:
        newLocation = [location[0]-1, location[1]]
        if newLocation in routeHistory:
            return False       
        elif maze[newLocation[0]][newLocation[1]] == 2:
            return False
        else:
            rightRoute.append(newLocation)
            routeHistory.append(newLocation)
            return True
        
def goRight(location):
    if(location[0]==5):
        return False
    else:
        newLocation = [location[0]+1, location[1]]
        if newLocation in routeHistory:
            return False       
        elif maze[newLocation[0]][newLocation[1]] == 2:
            return False
        else:
            rightRoute.append(newLocation)
            routeHistory.append(newLocation)
            return True
            

#store right roadmap
rightRoute = [[1,0]]
#store passed roadmap
routeHistory = [[1,0]]
#current position
location = [1,0]
#exit location
exitLocation = [len(maze)-2, len(maze[0])-1]
exitValue = maze[len(maze)-2][len(maze[0])-1]
print(exitLocation, exitValue)

#If it is not the exit [4,5], then keep going
while rightRoute[-1] != exitLocation and exitValue != 2:
    #four way - up, down, left, right.
    #If it gets True, keep going. Or change another direction.
    if goUp(location):
        location = rightRoute[-1]
        continue
    if goDown(location):
        location = rightRoute[-1]
        continue
    if goLeft(location):
        location = rightRoute[-1]
        continue
    if goRight(location):
        location = rightRoute[-1]
        continue
    #If it gets False, it means No Way to Go! Eliminate it
    rightRoute.pop()
    #Keep going
    try:
        location = rightRoute[-1]
    except IndexError:
        print("Bad maze design")
        sys.exit(1)
#print the final roadmap
if len(rightRoute)==1:
    print("No way out")
else:
    print("The Maze is good one, we can go in and out.")
    print(rightRoute)