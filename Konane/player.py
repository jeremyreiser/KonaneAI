'''
Created on Dec 1, 2019
@author: Jeremy
'''
from board import Board

class Player(object):
    
    '''
    Player class handles checking validity of moves and generating valid moves
    '''
    
    def __init__(self, color, board):
        '''
        Constructor
        '''
        self.color = color          #color stored as int, 1 = black
        self.board = board          #associated board state
        self.board_size = board.getBoardSize()
        self.playing = 1            
        
    def isValidMove(self, x1, y1, x2, y2):
        '''
        Checks if moves are valid
        -x1, y1 are the coordinates of the piece to be moved
        -x2, y2 are the coordinates of the adjacent piece to be jumped
        '''
        
        if(x1 not in range(self.board_size) or x2 not in range(self.board_size) or 
           y1 not in range(self.board_size) or y2 not in range(self.board_size)):
            return 0;
        if(self.board.state[x1][y1] != self.color):    #If trying to move opponent
            return 0;
        if(self.board.state[x2][y2] != (not self.color)):    #If trying to jump self or empty
            return 0;
        if(x1 == x2 and y1 == y2 - 1 and (y2+1 in range(self.board_size))):
            if(self.board.state[x2][y2+1] == 2):
                return 1;
        elif(x1 == x2 and y1 == y2 + 1 and (y2-1 in range(self.board_size))):
            if(self.board.state[x2][y2-1] == 2):
                return 1;
        elif(x1 == x2 - 1 and y1 == y2 and (x2+1 in range(self.board_size))):
            if(self.board.state[x2+1][y2] == 2):
                return 1;
        elif(x1 == x2 + 1 and y1 == y2 and (x2-1 in range(self.board_size))):
            if(self.board.state[x2-1][y2] == 2):
                return 1;
        return 0;
    
    def generateMoves(self):        
        '''
        This function generates all available moves,
        then stores them in a list
        '''
        movesList = []              
        for x in range(self.board_size):
            for y in range(self.board_size):
                if(self.isValidMove(x, y, x, y+1)):
                    movesList.append([x,y,x,y+1])
                if(self.isValidMove(x,y,x,y-1)):
                    movesList.append([x,y,x,y-1])
                if(self.isValidMove(x, y, x-1, y)):
                    movesList.append([x,y,x-1,y])
                if(self.isValidMove(x,y,x+1,y)):
                    movesList.append([x,y,x+1,y])
        #for x in range(len(movesList)):  # Prints available moves (for testing purposes)
        #    print(movesList[x])
        return movesList;      # The list of available moves
    
