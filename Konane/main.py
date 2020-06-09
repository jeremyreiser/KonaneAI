'''
Created on Dec 1, 2019
@author: Jeremy Reiser
'''
from board import Board
from player import Player
from brain import Brain

'''
This class meant for user testing
'''


boardSize = 18           # Specify board size here
b = Board(boardSize)        
q = 0                   # Variable for quitting loop
player1 = Player(1, b)
mybrain = Brain()

'''                     #For testing purposes, allows player to
                        #Specify first two pieces removed
for i in range(boardSize):   # Prints the board
    print(player1.board.state[i])
    print()
    
p = input("Enter first piece to remove: ")   # Player 1 removes first piece
if(p == "q"):                                # Skip to end if player enters q
        q = 1
else:
    if(p[1] == ","):
        player1.board.remove(9,9)
    else:
        convert1 = p[0] + p[1]
        convert2 = p[3] + p[4]
        player1.board.remove(9,9)

for i in range(boardSize):
    print(player1.board.state[i])
    print()
    
if(not q):                                  # Skip to end if player entered q
    p = input("Enter second piece to remove: ")  # Player 2 removes second piece
    if(p == "q"):
        q = 1                               # Skip to end if player enters q
    else:
        if(p[1] == ","):
            player1.board.remove(8,9)
        else:
            convert1 = p[0] + p[1]
            convert2 = p[3] + p[4]
            player1.board.remove(8,9)
        for i in range(boardSize):
            print(player1.board.state[i])
            print()

    
while(not q):
    j = input("Enter piece to jump with or q to quit: ")
    if(j == "q"):
        q = 1
    else:
        k = input("Enter piece to jump over: ")
        player1.board.jump(int(j[0]),int(j[2]), int(k[0]), int(k[2]))
        for i in range(boardSize):
            print(player1.board.state[i])
            print()
            
print(len(player1.generateMoves())," moves possible at quit")
rounds = 0


#This is meant for generating states.txt
#Uses minimax search to learn what moves are best
file1 = open("states.txt","a+")
while(player1.playing):
    file1.write(player1.board.getBoardId())
    file1.write("\n")
    player2 = Player(1, player1.board)
    if(player1.color):
        player2.color = 0
    moves = mybrain.minimax(player1)
    if(moves[1] == -1):
        print("Game ends in win!")
        player1.playing = 0
        move = ""
        move = move + str(moves[0][0])
        file1.write(move)
        file1.write("\n")
        move = ""
        move = move + str(moves[0][1])
        file1.write(move)
        file1.write("\n") 
        move = ""
        move = move + str(moves[0][2])
        file1.write(move)
        file1.write("\n") 
        move = ""
        move = move + str(moves[0][3])
        file1.write(move)
        file1.write("\n")
    elif(moves[1] == -2):
        print("Game ends in loss...")
        player1.playing = 0
    else:
        myMove = moves[0]
        theirMove = moves[1]
        print("Player 1 moves: ",myMove)
        player1.board.jump(myMove[0],myMove[1],myMove[2],myMove[3])
        move = ""
        move = move + str(myMove[0])
        file1.write(move)
        file1.write("\n")
        move = ""
        move = move + str(myMove[1])
        file1.write(move)
        file1.write("\n") 
        move = ""
        move = move + str(myMove[2])
        file1.write(move)
        file1.write("\n") 
        move = ""
        move = move + str(myMove[3])
        file1.write(move)
        file1.write("\n")
        player2.board = player1.board
        print("Player 2 moves: ",theirMove)
        player2.board.jump(theirMove[0],theirMove[1],theirMove[2],theirMove[3])
        player1.board = player2.board
        player1.board.printBoard()
file1.close()

'''
#All below code is for server integration
import socket 
import sys  
import time  

open = 1
playerChosen = 0
pieceRemoved = 0
sentRemove = 0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #server socket
s.connect(('artemis.engr.uconn.edu',4705))
iostream = ""
message = ""
print(s.recv(4096))                                     #receive first input
print(s.recv(4096))
s.send('11\r\n'.encode())                               #send username
print(s.recv(4096))
s.send('22\r\n'.encode())                               #send password
print(s.recv(4096))
s.send('14\r\n'.encode())                               #send opponent name
print(s.recv(4096))
while(open):
    if(not playerChosen):                   #while choosing player number:
        time.sleep(1)
        playerName = (s.recv(4096))
        time.sleep(1)
        message = str(playerName)
        iostream = iostream + message
        if(len(str(playerName))>5):
            print(str(playerName))
        if("Player" in str(playerName)):
            b1 = Board(18)
            myPlayer = Player(1,b1)
            playerChosen = 1
    if(playerChosen and not pieceRemoved):  #while removing pieces:  
        if("2" in str(playerName) or "White" in str(playerName)):
            myPlayer.color = 0
        #print("I am player",myPlayer.color)
        pieceRemover = playerName
        if((not pieceRemoved) and (not myPlayer.color)):
            if("Removed" in str(pieceRemover)):
                srem = ""
                for y in str(pieceRemover):
                    if(y == ":" or (ord(y) > 47 and ord(y) < 58 )):
                        srem = srem + y
                srem.strip("\n")
                srem.strip("b'")
                srem.rstrip()
                print("Opponent removed:")
                print(str(pieceRemover))
                print(srem)
                intFound = 0
                str1 = ""
                str2 = ""
                index1 = 0
                index2 = 0
                srem = srem.strip(":")
                srem = srem.strip("2")
                print(srem)
                for x in srem:
                    if(intFound == 1 and x != ":" and x != "2" and len(str1) < 3):
                        str1 = str1 + x
                    if(intFound == 2 and x != ":" and x != "2" and len(str2) < 3):
                        str2 = str2 + x
                    if(x == ":"):
                        intFound = intFound + 1
                    if(x == "2"):
                        intFound = intFound - 1
                index1 = int(str1)
                index2 = int(str2)
                myPlayer.board.remove(index1, index2)
                pieceRemoved = 1
                if(index1 == 0 and index2 == 0):
                    s.send('[0:1]\r\n'.encode())
                    myPlayer.board.remove(0,1)
                elif(index1 == 17 and index2 == 17):
                    s.send('[17:16]\r\n'.encode())  
                    myPlayer.board.remove(17,16)  
                else:
                    s.send('[8:9]\r\n'.encode())
                    myPlayer.board.remove(8,9)
        elif(not pieceRemoved and myPlayer.color):
            if("?R" in str(pieceRemover) or "?R" in str(playerName)):
                if(not sentRemove):
                    s.send('[17:17]\r\n'.encode())
                    myPlayer.board.remove(17,17)
                    sentRemove = 1
                time.sleep(1)
                pieceRemover = s.recv(4096)
                time.sleep(1)
                message = str(pieceRemover)
                iostream = iostream + message
                if(len(str(pieceRemover)) > 5):
                    print(str(pieceRemover))
                if(len(str(pieceRemover)) > 2 and "Removed" in str(pieceRemover) and "17:17" not in str(pieceRemover)):
                    srem = ""
                    for y in str(pieceRemover):
                        if(y == ":" or (ord(y) > 47 and ord(y) < 58 )):
                            srem = srem + y
                    srem.strip("\n")
                    srem.strip("b'")
                    srem.rstrip()
                    print(srem)
                    intFound = 0
                    str1 = ""
                    str2 = ""
                    for x in srem:
                        if(intFound == 1 and x != ":"):
                            str1 = str1 + x
                        if(intFound == 2 and x != ":"):
                            str2 = str2 + x
                        if(x == ":"):
                            intFound = intFound + 1
                    if(len(str1) > 2):
                        temp = str1[0] + str1[1]
                        str1 = temp
                    index1 = int(str1)
                    if(len(str2) > 2):
                        temp = str2[0] + str2[1]
                        str2 = temp
                    index2 = int(str2)
                    myPlayer.board.remove(index1, index2)
                    print("Removed opponent's piece")
                    pieceRemoved = 1
        else:
            pieceRemover = s.recv(4096)
            message = str(pieceRemover)
            iostream = iostream + message
    if(pieceRemoved and playerChosen):  #after game setup, while making moves
        time.sleep(1)                   #delay to help separate server inputs
        turn = s.recv(4096)             #receive move or move prompt
        if("?Move" not in str(turn) and "Move[" not in str(turn)):
            turn = pieceRemover         #deals with server input being jumbled
            if("?Move" not in str(turn) and "Move[" not in str(turn)):
                turn = iostream         #further deals with input being jumbled
        if("?Move" in str(turn)):       #if prompting for a move, do:
            myMove = -1
            if(myPlayer.color):         #first check if board state is saved
                myMove = mybrain.makeMove(myPlayer.board.getBoardId())
            if(myMove == -1):           #if not saved, perform minimax
                myMoves = mybrain.minimax(myPlayer)
                myMove = myMoves[0]
            x1 = int(myMove[0])
            #print(x1)
            y1 = int(myMove[1])
            #print(y1)
            x2 = int(myMove[2])
            #print(x2)
            y2 = int(myMove[3])
            #print(y2)
            '''
            The following section must be included because my representation
            of moves selects the piece to be moved, followed by the adjacent 
            piece rather than the spot to be moved to. This differs from the
            server-side representation of a move.
            '''
            if(x1 == x2 - 1):
                x2 = x2 + 1
            if(x1 == x2 + 1):
                x2 = x2 - 1
            if(y1 == y2 - 1):
                y2 = y2 + 1
            if(y1 == y2 + 1):
                y2 = y2 - 1
            myResponse = '['+str(x1)+':'+str(y1)+']:['+str(x2)+':'+str(y2)+']\r\n'
            print("Sending response: ",myResponse)  #send my move
            s.send(myResponse.encode())
        elif("Move[" in str(turn)):     #if receiving opponent's move, do:
            sturn = ""
            for y in str(turn):         #this code parses input
                if(y == ":" or (ord(y) > 47 and ord(y) < 58 )):
                    sturn = sturn + y
            sturn.strip("\n")
            sturn.strip("b'")
            sturn.rstrip()
            print(sturn)
            intFound = 1
            str1 = ""
            str2 = ""
            str3 = ""
            str4 = ""
            for x in sturn:
                if(intFound == 1 and x != ":"):
                    str1 = str1 + x
                if(intFound == 2 and x != ":"):
                    str2 = str2 + x
                if(intFound == 3 and x != ":"):
                    str3 = str3 + x
                if(intFound == 4 and x != ":"):
                    str4 = str4 + x
                if(x == ":"):
                    intFound = intFound + 1

            x1 = int(str1)
            y1 = int(str2)
            x2 = int(str3)
            y2 = int(str4)
            str1 = ""
            str2 = ""
            str3 = ""
            str4 = ""
            if(x1 == x2 - 2):       #Deals with server-side representation of a move
                x2 = x2 - 1
            if(x1 == x2 + 2):
                x2 = x2 + 1
            if(y1 == y2 - 2):
                y2 = y2 - 1
            if(y1 == y2 + 2):
                y2 = y2 + 1
            myPlayer.board.jump(x1, y1, x2, y2)     #Execute opponent's move
    
if __name__ == '__main__':
    pass