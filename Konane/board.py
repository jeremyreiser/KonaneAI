'''
Created on Dec 1, 2019
@author: Jeremy Reiser
'''

class Board(object):
    '''
    This class represents the state of the game board at any given time.
    It implements functionality of jumping, copying, and printing the board.
    '''


    def __init__(self, board_size):
        '''
        Constructor - Creates the game board with a given board_size
        state[i][j] = 0 if a white piece is occupying space (i,j),
                    = 1 if a black piece is occupying space (i,j),
                    = 2 if the space (i,j) is empty
        '''
        self.board_size = board_size
        self.boardId = ""
        self.state = [[0 for i in range(board_size)] for j in range(board_size)] 
        for i in range(0, board_size):
            for j in range(0, board_size):
                if(i%2 == 0):
                    if(j%2 == 0):
                        self.state[i][j] = 1;
                else:
                    if(j%2 == 1):
                        self.state[i][j] = 1;
                        
                        
    def getBoardSize(self):
        return self.board_size
    
    def remove(self, x, y):         # Function to remove any piece
        self.state[x][y] = 2;
        
    def jump(self, x1, y1, x2, y2):         # Implements jump functionality
        jumper = self.state[x1][y1]         # x1, y1 are the coordinates of the moving piece
        if(x1 == x2 and y1 == y2 - 1):      # x2, y2 are the coordinates of the adjacent piece
            if(self.state[x2][y2+1] == 2):
                self.state[x2][y2+1] = jumper
                self.remove(x2,y2)
                self.remove(x1,y1)
            else:
                print("Space beyond is occupied")
        elif(x1 == x2 and y1 == y2 + 1):
            if(self.state[x2][y2-1] == 2):
                self.state[x2][y2-1] = jumper
                self.remove(x2,y2)
                self.remove(x1,y1)
            else:
                print("Space beyond is occupied")
        elif(x1 == x2 - 1 and y1 == y2):
            if(self.state[x2+1][y2] == 2):
                self.state[x2+1][y2] = jumper
                self.remove(x2,y2)
                self.remove(x1,y1)
            else:
                print("Space beyond is occupied")
        elif(x1 == x2 + 1 and y1 == y2):
            if(self.state[x2-1][y2] == 2):
                self.state[x2-1][y2] = jumper
                self.remove(x2,y2)
                self.remove(x1,y1)
            else:
                print("Space beyond is occupied")
        else:
            print("Pieces not adjacent")
            print()
            
    def isNextTo(self, x1, y1, x2, y2):  #Currently not used
        if(x1 == x2 and (y1 == y2 + 1 or y1 == y2 - 1)):
            return 1;
        elif(y1 == y2 and (x1 == x2 + 1 or x1 == x2-1)):
            return 1;
        return 0;
    
    def printBoard(self):               #Display board to output window
        for i in range(self.board_size):
            print(self.state[i])
            print()
            
    def copyBoard(self):                #Makes a copy of the board
        b = Board(self.board_size)
        for i in range(self.board_size):
            for j in range(self.board_size):
                b.state[i][j] = self.state[i][j]
            
        return b;
    
    def getBoardId(self):               #Generates unique board ID
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.boardId = self.boardId + str((self.state[i][j]))
                
        return self.boardId;