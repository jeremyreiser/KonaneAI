'''
Created on Dec 11, 2019

@author: Jeremy
'''

from board import Board
from player import Player

class Brain(object):
    '''
    Brain class performs the move evaluation portion of the program
    Later, also added server parsing functionality
    '''


    def __init__(self):
        self.limit = 5000           #limit number of generated board states
                                    #(no longer used)
    def testMoves(self, p1):        
        '''
        This function tests all board states and ranks the available moves 
        (no longer used due to unfeasibility)
        '''                           
        file1 = open("states.txt","a+") 
        file1.write(p1.board.getBoardId())  #write board state to file
        file1.write("\n")
        max = -100                  #stores number of my moves available
        min = 1000                  #stores number of opponent's moves available
        bestMove = []
        myMoves = []
        myMoves2 = []
        theirMoves = []
        theirMoves2 = []
        theirBestMove = []
        moves = p1.generateMoves()
        file1.write(str(len(moves)))
        file1.write("\n")
        opponent = 1
        if(p1.color):
            opponent = 0
            
        for x in moves:             #for each of my available moves, do:
            print("Testing move: ", x[0],",",x[1],",",x[2],",",x[3])
            move = ""
            move = move + str(x[0]) + str(x[1]) + str(x[2]) + str(x[3])
            file1.write(move)       #write the move associated with this board
            file1.write("\n")
            board = p1.board.copyBoard()    #copy of starting board
            mycolor = p1.color
            p2 = Player(mycolor, board)
            p3 = Player(opponent, board)
            p2.board.jump(x[0],x[1],x[2],x[3])  #execute the move
            board = p2.board
            print("My new moves: ")
            myMoves = p2.generateMoves()    #generates new moveset for evaluation purposes
            print("My opponent's new moves: ")
            theirMoves = p3.generateMoves()
            print("This leaves me with:",len(myMoves), "moves.")
            print("This gives my opponent:", len(theirMoves), "moves.")
            p2.board.printBoard()
            for y in theirMoves:            #for each of their new moves, do:
                print("Testing opponent move: ",y)
                board2 = board.copyBoard()
                p3.board = board2
                p3.board.jump(y[0],y[1],y[2],y[3])  #execute move
                p2.board = p3.board
                print("My new moves: ")
                myMoves2 = p2.generateMoves()       #my resulting moves 
                print("Opponent's new moves: ")
                theirMoves2 = p3.generateMoves()
                if((len(myMoves2)-len(theirMoves2)) < min):
                    min = len(myMoves2)-len(theirMoves2)    #opponent seeks to minimize my available moves
                    theirBestMove = [y[0],y[1],y[2],y[3]]
            if((len(myMoves)-len(theirMoves)) > max):
                max = len(myMoves)-len(theirMoves)          #i seek to maximize my moves over their moves
                bestMove = [x[0],x[1],x[2],x[3]]
            file1.write(str(len(myMoves)-len(theirMoves)))  #stores my move evaluation value
            file1.write("\n")
            if((len(theirMoves) > 0) and (self.limit > 0)):
                self.limit = self.limit - 1
                print("Opponent makes best move: ", theirBestMove) #assume my opponent makes their best move
                p3.board = board            
                p2.board = board
                p3.board.jump(theirBestMove[0],theirBestMove[1],theirBestMove[2],theirBestMove[3])
                p3.board.printBoard()
                p2.board = p3.board
                self.testMoves(p2)          #recursively tests my new set of moves
        file1.close()
        
    def makeMove(self, bid):
        '''
        This function attempts to make a move based on the evaluated moves
        associated with a particular board state
        '''
        file1 = open("states.txt","r")
        lines = []
        found = -1
        numMoves = 0
        max = -100
        curMove = []
        bestMove = []
        for line in file1:
            lines.append(line.rstrip('\n'))
        for x in range(len(lines)):
            if((lines[x].find(bid)) > -1):
                #print("Found board id at line:", x+1)
                found = x
        
        if(found == -1):
            print("Failed to make move!")
            return -1;
        
        found = found + 1
        #numMoves = int(lines[found])
        #print("Number of moves to choose from in this case: ",numMoves)
        '''
        for x in range(numMoves):  #This was used when attempting to evaluate all possible board states
            found = found + 1
            curMove = [int(lines[found][0]), int(lines[found][1]), int(lines[found][2]), int(lines[found][3])]
            found = found + 1
            if(int(lines[found]) > max):
                max = int(lines[found])
                bestMove = curMove
        
        if(numMoves == 0):
            print("No moves left, you lose.")
        else:
            print("Best move is: ",bestMove)
        '''
        print("Move to be made: ",lines[found], lines[found+1], lines[found+2], lines[found+3])
        file1.close()

        return [lines[found],lines[found+1], lines[found+2], lines[found+3]];
        
    def minimax(self, p1):
        '''
        This function performs a minimax evaluation on my moves given the board state
        Checks my moves, each of my opponent's resulting moves, and the number of
        available moves I am left with (depth of 3). Returns my best move and my
        opponent's best move.
        '''
        oboard = p1.board.copyBoard()   #copy the original board
        weights = []                    #this array unused
        moves = p1.generateMoves()      
        if(len(moves) == 0):
            print("You lose!")
            return [0,-2];
        opp = 1
        max = -1
        min = 100
        bestMove = 0
        theirBestMove = 0
        if(p1.color):                   #finds opponent's color
            opp = 0
        for x in range(len(moves)):
            theirMoves = []             #array to store opponent's moves
            print("Trying move:",x)     #test each of my moves
            p1.board = oboard.copyBoard()
            p1.board.jump(moves[x][0],moves[x][1],moves[x][2],moves[x][3])
            p2 = Player(opp,p1.board)   #create my opponent's player
            print("Move",x,"gives opponent following moves:")
            theirMoves = p2.generateMoves()     #generate my opponent's moves
            if(len(theirMoves) == 0):           #if they have no moves, I win
                print("No moves found for opponent. Execute move:",moves[x])
                print("You win!")
                return [moves[x],-1];           #return my winning move
            sboard = p1.board.copyBoard()
            if(min < 100 and min > max):    #save opponent's best minimax move
                max = min
                min = 100
                bestMove = x-1
                theirBestMove = worstMove   
                worstMove = 0
            for y in range(len(theirMoves)):    #for each of their moves
                moves2 = []
                print("Opponent tries move",y)  #try the move
                p2.board = sboard.copyBoard()
                p2.board.jump(theirMoves[y][0],theirMoves[y][1],theirMoves[y][2],theirMoves[y][3])
                p1.board = p2.board
                moves2 = p1.generateMoves()
                print("which gives me",len(moves2),"moves.")
                if(len(moves2) < min):          #stores the minimum number of moves I can have
                    min = len(moves2)           
                    worstMove = y               #assumes my opponent will make the worst move for me
        if(len(moves) == 1):
            worstMove = theirBestMove           #fixes bug if I only have one available move
        print("Minimax best move is:",bestMove, moves[bestMove])
        #print(theirBestMove)
        oboardc = oboard.copyBoard()            #copy board
        oboardc.jump(moves[bestMove][0],moves[bestMove][1],moves[bestMove][2],moves[bestMove][3])
        #print("In minimax function")
        p3 = Player(1,oboardc)
        if(p1.color):
            p3.color = 0
        omoves = p3.generateMoves()
        print("Opponent's best move is:",omoves[theirBestMove])
        p1.board = oboard.copyBoard()           #restore the original board
        return [moves[bestMove],omoves[theirBestMove]];
    
    def parseMove(turn):
        '''
        This function parses the opponent's turn as represented by the server
        '''
        turn.replace('Move','')
        turn.replace('[','')
        turn.replace(']','')
        intFound = 1
        for x in turn:
            if(x == ":"):
                intFound = intFound + 1
            if(intFound == 1):
                str1 = str1 + x
            if(intFound == 2):
                str2 = str2 + x
            if(intFound == 3):
                str3 = str3 + x
            if(intFound == 4):
                str4 = str4 + x
        return [int(str1), int(str2), int(str3), int(str4)]

    def parseRemove(removed):
        '''
        This function parses the opponent's removed piece as represented
        by the server.
        '''
        removed.replace('Removed','')
        removed.replace('[', '')
        removed.replace(']','')
        intFound = 0
        for x in removed:
            if(x == ":"):
                intFound = intFound + 1
            if(intFound == 1):
                str1 = str1 + x
            if(intFound == 2):
                str2 = str2 + x
        
        return[int(str1),int(str2)];
        