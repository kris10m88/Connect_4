from graphics import *
import time
import msvcrt as m

"""
columns
1 = 115
2 = 245
3 = 375
4 = 505
5 = 635
6 = 765
7 = 895
"""

# Sets up game board
win = GraphWin("Win",995, 805)
board = Rectangle(Point(25,110),Point(960,780))
board.setFill("royalblue")
board.setWidth(0)
board.draw(win)
holes = []

y = 0
while y < 6:
    for x in range(0,7):
        holes.append(Circle(Point(130*x + 115, 110*y + 170),50))
        holes[x+7*y].setWidth(0) 
        holes[x+7*y].setFill("white")
        holes[x+7*y].draw(win)
    y += 1
# end of game board

class Game():
    def __init__(self):
        self.win = win
        self.key = None
        self.win.bind_all('<Key>', self.key_pressed)
        self.tops = [820]*7
        self.p1_tokens = []
        self.p2_tokens = []
        self.all_tokens = []
        self.waiting = True
        self.col = 0
        self.turn_1 = True
        self.over = False
        self.score1 = 0
        self.score2 = 0

    def key_pressed(self, event):
        self.key = event.keysym
        
    def handle_keypress(self):
        if self.key == "Right":
            if not self.over:
                if self.current_token.can_move(1,0):
                    self.current_token.move(1,0)
                    self.col = (self.current_token.center[0]-115)/130
            else:
                if self.current_selection:
                    self.select.move(150,0)
                    self.current_selection = False
                    
            
        elif self.key == "Left":
            if not self.over:
                if self.current_token.can_move(-1,0):
                    self.current_token.move(-1,0)
                    self.col = (self.current_token.center[0]-115)/130
            else:
                if not self.current_selection:
                    self.select.move(-150,0)
                    self.current_selection = True
                    
        
        elif self.key == "space":
            if not self.over:
                if self.tops[int(self.col)] != 170:
                    self.waiting = False
                    while self.current_token.can_move(0,1):
                        self.current_token.move(0,1)
                        time.sleep(.05)
            else:
                self.selected = True
                
        self.key = None
        
    def drop_token(self):
        self.current_token = Token(self.turn_1)
        self.current_token.draw(self.win)
        self.col = 0
        self.waiting = True
        while self.waiting:
            self.current_token.move(1,0)
            self.current_token.move(-1,0)
            self.handle_keypress()
            time.sleep(.25)

    
    def end_turn(self):
        self.tops[int(self.col)] = self.current_token.center[1]
        if self.turn_1:
            self.p1_tokens.append([self.col,int((self.current_token.center[1]-170)/110)]) 
            self.all_tokens.append(self.current_token)

        else:
            self.p2_tokens.append([self.col,int((self.current_token.center[1]-170)/110)])
            self.all_tokens.append(self.current_token)
            
            
    def check_winner_horizontal(self):
        if self.turn_1:
            for row in range(6):
                tokensc_in_row = []
                for token in self.p1_tokens:
                    if token[1] == row:
                        tokensc_in_row.append(token[0])
                for token in tokensc_in_row:
                    if token+1 in tokensc_in_row and token+2 in tokensc_in_row and token+3 in tokensc_in_row:
                        self.game_over = Text(Point(497.5,55),"Game Over. Player 1 wins!")
                        self.game_over.setSize(36)
                        self.game_over.draw(self.win)
                        self.score1 += 1
                        self.over = True
                
        else:
            for row in range(6):
                tokensc_in_row = []
                for token in self.p2_tokens:
                    if token[1] == row:
                        tokensc_in_row.append(token[0])
                for token in tokensc_in_row:
                    if token+1 in tokensc_in_row and token+2 in tokensc_in_row and token+3 in tokensc_in_row:
                        self.game_over = Text(Point(497.5,55),"Game Over. Player 2 wins!")
                        self.game_over.setSize(36)
                        self.game_over.draw(self.win)
                        self.score2 += 1
                        self.over = True
            
            
        
    def check_winner_vertical(self):
        if self.turn_1:
            for col in range(7):
                tokensc_in_col = []
                for token in self.p1_tokens:
                    if token[0] == col:
                        tokensc_in_col.append(token[1])
                for token in tokensc_in_col:
                    if token+1 in tokensc_in_col and token+2 in tokensc_in_col and token+3 in tokensc_in_col:
                        self.game_over = Text(Point(497.5,55),"Game Over. Player 1 wins!")
                        self.game_over.setSize(36)
                        self.game_over.draw(self.win)
                        self.score1 += 1
                        self.over = True
            
        else:
            for col in range(7):
                tokensc_in_col = []
                for token in self.p2_tokens:
                    if token[0] == col:
                        tokensc_in_col.append(token[1])
                for token in tokensc_in_col:
                    if token+1 in tokensc_in_col and token+2 in tokensc_in_col and token+3 in tokensc_in_col:
                        self.game_over = Text(Point(497.5,55),"Game Over. Player 1 wins!")
                        self.game_over.setSize(36)
                        self.game_over.draw(self.win)
                        self.score2 += 1
                        self.over = True
            
    def check_winner_dur(self):
        if self.turn_1:
            for token in self.p1_tokens:
                other_tokens = []
                complete = True
                for x in range(1,4):
                    other_tokens.append([token[0]+x,token[1]-x])
                for x in other_tokens:
                    if x in self.p1_tokens:
                        pass
                    else:
                        complete = False
                if complete:
                    self.game_over = Text(Point(497.5,55),"Game Over. Player 1 wins!")
                    self.game_over.setSize(36)
                    self.game_over.draw(self.win)
                    self.score1 += 1
                    self.over = True
            
        else:
            for token in self.p2_tokens:
                other_tokens = []
                complete = True
                for x in range(1,4):
                    other_tokens.append([token[0]+x,token[1]-x])
                for x in other_tokens:
                    if x in self.p2_tokens:
                        pass
                    else:
                        complete = False
                if complete:
                    self.game_over = Text(Point(497.5,55),"Game Over. Player 2 wins!")
                    self.game_over.setSize(36)
                    self.game_over.draw(self.win)
                    self.score2 += 1
                    self.over = True
    
    
    def check_winner_ddl(self):
        if self.turn_1:
            for token in self.p1_tokens:
                other_tokens = []
                complete = True
                for x in range(1,4):
                    other_tokens.append([token[0]+x,token[1]+x])
                for x in other_tokens:
                    if x in self.p1_tokens:
                        pass
                    else:
                        complete = False
                if complete:
                    self.game_over = Text(Point(497.5,55),"Game Over. Player 1 wins!")
                    self.game_over.setSize(36)
                    self.game_over.draw(self.win)
                    self.score1 += 1
                    self.over = True
                    self.turn_1 = False
                else:
                    self.turn_1 = False
            
        else:
            for token in self.p2_tokens:
                other_tokens = []
                complete = True
                for x in range(1,4):
                    other_tokens.append([token[0]+x,token[1]+x])
                for x in other_tokens:
                    if x in self.p2_tokens:
                        pass
                    else:
                        complete = False
                if complete:
                    self.game_over = Text(Point(497.5,55),"Game Over. Player 2 wins!")
                    self.game_over.setSize(36)
                    self.game_over.draw(self.win)
                    self.score2 += 1
                    self.over = True
                    self.turn_1 = True
                else:
                    self.turn_1 = True
                
    def check_full(self):
        if len(self.all_tokens) == 42:
            self.game_over = Text(Point(497.5,55),"Game Over. Tie!")
            self.game_over.setSize(36)
            self.game_over.draw(self.win)
            if self.turn_1:
                self.turn_1 = False
            else:
                self.turn_1 = True
            self.over = True
                    
    def draw_scoreboard(self):
        self.board1 = Text(Point(100,40),"Player 1:")
        self.board1.setSize(24)
        self.scoret1 = Text(Point(100,80),self.score1)
        self.scoret1.setSize(24)
        self.board1.draw(self.win)
        self.scoret1.draw(self.win)
        
        self.board2 = Text(Point(895,40),"Player 2:")
        self.board2.setSize(24)
        self.scoret2 = Text(Point(895,80),self.score2) 
        self.scoret2.setSize(24)
        self.board2.draw(self.win)
        self.scoret2.draw(self.win)
        
    def play_again(self):
        self.replay_box = Rectangle(Point(332,260),Point(664,520))
        self.replay_box.setFill("lightgray")
        self.replay_box.draw(self.win)
        
        self.replay_text = Text(Point(497.5,340),"Play again?")
        self.replay_text.setSize(36)
        self.replay_text.draw(self.win)
        
        self.yes = Text(Point(423,440),"YES")
        self.yes.setSize(36)
        self.yes.draw(self.win)
        
        self.no = Text(Point(575,440),"NO")
        self.no.setSize(36)
        self.no.draw(self.win)
        
        self.select = Rectangle(Point(365,410),Point(485,475))
        self.select.setWidth(10)
        self.select.setOutline("deepskyblue")
        self.select.draw(self.win)
        self.selected = False
        self.current_selection = True #true = yes
        
        while not self.selected:
            self.select.undraw()
            self.handle_keypress()
            time.sleep(.25)
            self.select.draw(self.win)
            self.handle_keypress()
            time.sleep(.25)
            
    def restart(self):
        self.game_over.undraw()
        self.board1.undraw()
        self.board2.undraw()
        self.scoret1.undraw()
        self.scoret2.undraw()
        self.replay_box.undraw()
        self.replay_text.undraw()
        self.yes.undraw()
        self.no.undraw()
        self.select.undraw()
        for token in self.all_tokens:
            token.piece.undraw()
            token.piece.undraw()
        self.p1_tokens = []
        self.p2_tokens = []
        self.all_tokens = []
        self.tops = [820]*7
        self.waiting = True
        self.over = False
        

class Token():
    def __init__(self, turn):
        self.piece = Circle(Point(115,60),50)
        if turn:
            self.piece.setFill("red")
            self.player = 1
        else:
            self.piece.setFill("yellow")
            self.player = 2
        self.point = self.piece.getCenter()
        self.center = [0,0]
        self.center[0] = self.point.getX()
        self.center[1] = self.point.getY()
    
    def move(self,dx,dy):
        self.piece.move(dx*130,dy*110)
        self.center[0] += dx*130
        self.center[1] += dy*110
        
    def can_move(self,dx,dy):
        if self.center[0] + (130*dx) > 895 or self.center[0] + (130*dx) < 115 :
            return False
        elif self.center[1] + (110*dy) >= game.tops[int(game.col)]:
            return False
        return True
        
        
    def draw(self, window):
        self.piece.draw(window)

game = Game()

def play():
    while not game.over:
        game.drop_token()
        game.end_turn()
        game.check_winner_horizontal()
        game.check_winner_vertical()
        game.check_winner_dur()
        game.check_winner_ddl()
        game.check_full()
    game.draw_scoreboard()
    game.play_again()


play()

playing = True

while playing:
    if game.current_selection:
        game.restart()
        play()
    else:
        playing = False
win.close()