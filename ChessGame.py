import copy
import Queue
import random
d = {
(0,0):('Castle',0),
(0,1):('Knight',0),
(0,2):('Bishop',0),
(0,3):('Queen',0),
(0,4):('King',0),
(0,5):('Bishop',0),
(0,6):('Knight',0),
(0,7):('Castle',0),
(1,0):('Pawn',0),
(1,1):('Pawn',0),
(1,2):('Pawn',0),
(1,3):('Pawn',0),
(1,4):('Pawn',0),

(1,5):('Pawn',0),
(1,6):('Pawn',0),
(1,7):('Pawn',0),
 
(7,0):('Castle',1),
(7,1):('Knight',1),
(7,2):('Bishop',1),
(7,3):('Queen',1),
(7,4):('King',1),
(7,5):('Bishop',1),
(7,6):('Knight',1),
(7,7):('Castle',1),
(6,0):('Pawn',1),
(6,1):('Pawn',1),
(6,2):('Pawn',1),
(6,3):('Pawn',1),
(6,4):('Pawn',1),
(6,5):('Pawn',1),
(6,6):('Pawn',1),
(6,7):('Pawn',1)
}
dUnicode = {
	('empty', None):(" "),
	
	('Castle',0):(u"\u265C"),
	('Knight',0):(u"\u265E"),
	('Bishop',0):(u"\u265D"),
	('Queen',0):(u"\u265B"),
	('King',0):(u"\u265A"),
	('Pawn',0):(u"\u265F"),


	('Castle',1):(u"\u2656"),
	('Knight',1):(u"\u2658"),
	('Bishop',1):(u"\u2657"),
	('Queen',1):(u"\u2655"),
	('King',1):(u"\u2654"),
	('Pawn',1):(u"\u2659")
}



class Piece:
	pieceType = 'empty' 
	side = None
	def setPiece(self,p,s):
		self.pieceType = p
		self. side = s
		self.notMoved = True
		self.nMove = False
	def getPiece(self):
		return self.pieceType,self.side
	def getMoves(self,board,x,y):
		moves = []
		if self.pieceType == 'Castle':
			self.nMove = True
			moves.append((0,1))
			moves.append((0,-1))
			moves.append((1,0))
			moves.append((-1,0))
			
		if self.pieceType == 'Pawn':
			if self.side == 0:
				moves.append((1,0))
				moves.append((1,-1))
				moves.append((1,1))
				if self.notMoved:
					if board.board[x+1][y].pieceType == 'empty':
						if board.board[x+2][y].pieceType == 'empty':
							moves.append((2,0))
			if self.side == 1:
				moves.append((-1,0))
				moves.append((-1,-1))
				moves.append((-1,1))
				if self.notMoved:
					if board.board[x-1][y].pieceType == 'empty':
						if board.board[x-2][y].pieceType == 'empty':
							moves.append((-2,0))
					
		if self.pieceType == 'Bishop':
			self.nMove = True
			moves.append((1,1))
			moves.append((1,-1))
			moves.append((-1,-1))
			moves.append((-1,1))
			
		if self.pieceType == 'Knight':
			moves.append((2,1))
			moves.append((2,-1))
			moves.append((-2,-1))
			moves.append((-2,1))
			moves.append((1,2))
			moves.append((1,-2))
			moves.append((-1,2))
			moves.append((-1,-2))
			
		if self.pieceType == 'Queen':
			self.nMove = True
			moves.append((0,1))
			moves.append((0,-1))
			moves.append((1,0))
			moves.append((-1,0))
			moves.append((1,1))
			moves.append((1,-1))
			moves.append((-1,-1))
			moves.append((-1,1))
			
		if self.pieceType == 'King':
			moves.append((0,1))
			moves.append((0,-1))
			moves.append((1,0))
			moves.append((-1,0))
			moves.append((1,1))
			moves.append((1,-1))
			moves.append((-1,-1))
			moves.append((-1,1))
		
		legalMoves = []
			
		for move in moves:
			nextX = x+(move[0])
			nextY = y+(move[1])
			if nextX >=0 and nextY >= 0 and nextX <=7 and nextY <= 7:
				if board.board[nextX][nextY].pieceType == 'King' and board.board[nextX][nextY].side != self.side:
					board.inCheck = board.board[nextX][nextY].side
					
				
				if self.pieceType != 'Pawn':
					if board.board[nextX][nextY].getPiece() == ('empty', None):
						legalMoves.append(move)
					if board.board[nextX][nextY].getPiece() != ('empty', None) and board.board[nextX][nextY].side != self.side:
						legalMoves.append(move)
						break
				if self.pieceType == 'Pawn':
					if (move[0] != 0) and (move[1] != 0):
						if board.board[nextX][nextY].side != self.side and board.board[nextX][nextY].pieceType != 'empty' : 
							 legalMoves.append(move)
					else:
						legalMoves.append(move)
		
		moves += legalMoves
		if self.nMove:
			nMoves = []
			
			for move in moves:
				
				for n in range(1,7):
					nextX = (move[0]*n)
					nextY = (move[1]*n)
					
					if nextX >=0 and nextY >= 0 and nextX <=7 and nextY <= 7:
						if board.board[nextX][nextY].pieceType == 'King' and board.board[nextX][nextY].side != self.side:
							board.inCheck = board.board[nextX][nextY].side
							
						if board.board[nextX][nextY].getPiece() == ('empty', None):
							#print 'direction:  ',move, (nextX,nextY)
							nMoves.append((nextX,nextY))
						if board.board[nextX][nextY].getPiece() != ('empty', None) and board.board[nextX][nextY].side != self.side:
							nMoves.append((nextX,nextY))
							break
							break
							
			moves += nMoves
		
					
		return moves 
		
				
		
				
			
		
class Board:
	def __init__(self):
		self.board=[[],[],[],[],[],[],[],[]]
		self.ply = 0
		self.capture0 = []
		self.capture1 = []
		self.inCheck = None
		for x in range(8):
			for y in range(8):
				self.board[x].append(Piece())

	def startGame(board):
		
		for x in range(8):
			for y in range(8):
				if (x,y) in d:
					p = Piece()
					p.setPiece(d[(x,y)][0],d[(x,y)][1])
					board.board[x][y] = p
		return board
	def move(self,xCurrent,yCurrent,xNew,yNew):
		if xNew >=0 and yNew >= 0 and xNew <=7 and yNew <= 7:
			if self.board[xNew][yNew].pieceType == 'empty':
				self.ply+=1
				self.board[xCurrent][yCurrent].notMoved = False
				self.board[xNew][yNew] = self.board[xCurrent][yCurrent]
				self.board[xCurrent][yCurrent] = Piece()
			else:
				if self.board[xNew][yNew].side != self.board[xCurrent][yCurrent].side:
					if self.board[xCurrent][yCurrent].side == 1:self.capture1.append(self.board[xNew][yNew])
					if self.board[xCurrent][yCurrent].side == 0:self.capture0.append(self.board[xNew][yNew])
					if self.board[xNew][yNew].pieceType == 'King':
						self.inCheck = self.board[xNew][yNew].side
					else:
						self.board[xNew][yNew] = self.board[xCurrent][yCurrent]
						self.board[xCurrent][yCurrent] = Piece()
					
			return self
	def successors(x,turn): 
		
		successorArray = []
		#print 'possible moves for player:' , turn  
		for X in range(0,8):
			for Y in range(0,8):
				if x.board[X][Y].pieceType != 'empty' and x.board[X][Y].side == turn:
					moves =  x.board[X][Y].getMoves(x,X,Y)
					#print moves
					for move in moves:
						child = copy.deepcopy(x) 
						child.move(X,Y,X+move[0],Y+move[1])
						#displayBoard(child.board)
						if child.board != x and not child in successorArray:
							successorArray.append(child)
						 
		return successorArray
		
	def boardScore(self,side):
		if side == 1:
			captured = self.capture1
			taken = self.capture0
		if side == 0:
			captured = self.capture0
			taken = self.capture1
		return len(captured)-len(taken)
	
	def inCheck(self,side):
		s = self.getMoves(side)
		return self.inCheck
	def inCheckMoves(self):
		possibleEscapeMoves = []
		if self.inCheck != None:
			for x in range(0,7):
				for y in range(0,7):
					if self.board[x][y].getPiece() == ('King', self.inCheck):
						escapeMoves = self.board[x][y].getMoves(self,x,y)
						for move in escapeMoves:
							child = copy.deepcopy(self)
							child.move(x,y,move[0],move[0])
							if child.inCheck == None:
								possibleEscapeMoves.append(move)
		return possibleEscapeMoves
	def checkmate(self):
		possibleEscapeMoves = []
		if self.inCheck != None:
			for x in range(0,7):
				for y in range(0,7):
					if self.board[x][y].getPiece() == ('King', self.inCheck):
						escapeMoves = self.board[x][y].getMoves(self,x,y)
						for move in escapeMoves:
							child = copy.deepcopy(self)
							child.move(x,y,move[0],move[0])
							if child.inCheck == None:
								possibleEscapeMoves.append(move)
		if possibleEscapeMoves == []:
			return True
		else:
			return False
		
								
							
						
				
			
	
	
	
			
	
def displayBoard(b):
		
		for y in range(8):
			if y == 0:
				print '  0   1   2   3   4   5   6   7' 
				print '---------------------------------' 
			else:
				print ''
				print '---------------------------------'
			for x in range(8):
				
				#print '|', b[x][y].pieceType[0:2],
				#print b[x][y].getPiece() #alternate ways of displaying the pieces 
				print '|',dUnicode[b[x][y].getPiece()],
			print '|',y,
		print ''
		print '---------------------------------'
		
		
x = Board().startGame()
print x.successors(1)
q = Queue.PriorityQueue()
def engine(h):
	
	b = copy.copy(h)
	displayBoard(b.board)
	moveBad = True
	while moveBad:
		m = raw_input('enter move  ')
		print m[0],m[1],m[2],m[3]
		n = []
		f = b.board[int(m[0])][int(m[1])].getMoves(b,int(m[0]),int(m[1]))
		for t in f:
			n.append((t[0]+int(m[0]),t[1]+int(m[0])));
			
		if (int(m[2]),int(m[3])) in b.board[int(m[0])][int(m[1])].getMoves(b,int(m[0]),int(m[1])):
			b.move(int(m[0]),int(m[1]),int(m[2]),int(m[3]))
			moveBad = False
		else: print 'thats not a legal move buttface'
	
	
	b = b.successors(1)[3]
	
	return engine(b)
	
engine(x)

turn = 0
def search(b):
	turn = 0
	visited = [b]
	q = Queue.PriorityQueue()
	q.put((b.boardScore(turn),b))
	
	while q.qsize()>0:
		turn = -turn +1
		
	
		child = q.get()
		#print child
		v = child[1]
		
		h = v.successors(turn)
		
		if len(h) > 0:
			for s in range(0,len(h)):
				#displayBoard(h[s].board)
				#print child[0]
				#print h[s].inCheckMoves
				if h[s].inCheckMoves() != None:
					displayBoard(h[s].board)
				if not h[s] in visited:
					newPriority = h[s].boardScore(turn) + child[0]
					q.put((newPriority,h[s]))
					visited.append(h[s])
				
#search(x)
		
	

#test(x,turn)


#print a
#for s in a:
#	displayBoard(s.board)
#print x.board[1][2].getMoves(x,1,2)
#x.move(7,7,3,5)
#a = x.successors(0)
#total = 0
#for s in a:
#	
#	k = s.successors(1)
#	for g in k:
#		print total
#		j = g.successors(0)
#		for u in j:
##				print total
##				y = u.successors(1)
##				for r in y:
#				total+=1
					
				
#for s in a:
#	k = s.successors(1)
#	for g in k:
#		j = g.successors(0)
#		for u in j:
#			print 'first'
#			displayBoard(s.board)
#			print s.capture0
#			print s.capture1
#			print 'second'
#			displayBoard(g.board)
#			
#			print g.capture0
#			print g.capture1
#			print 'third'
#			displayBoard(u.board)
#			print u.capture0
#			print u.capture1
#			if len(u.capture1) >0:
#				print 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'
#				print u.capture1[0].getPiece()
#				break
#			if len(u.capture0) >0:
#				print 'KKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKKK'
#				print u.capture0[0].getPiece()
#				break
#			total+=1

