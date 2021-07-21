import pygame
import Logic as GL
from Containers import PendingMove, Vector2
import Minimax as ALG
import time
#import the tkinter for the input function
import tkinter as tk
from tkinter import messagebox

#pop-up window
class Dialog(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title('Initial Level')
        self.createGUI()
        self.level_result = 1
        width = 300 #size-width
        height = 100 #size-height
        x = 800
        y = 500
        self.geometry('%dx%d+%d+%d' % (width, height, x, y))

    def createGUI(self):
        """
        This part is creating the window for selecting AI cleverness, difficulty initially
        :return:
        """
        frame = tk.Frame(self)
        frame.pack(fill='x')
        label = tk.Label(frame, text='Level:\n (1 - 10)', height=2, width=8)
        label.pack(side=tk.LEFT)
        self.level = tk.StringVar()
        tk.Entry(frame, textvariable=self.level).pack(side=tk.RIGHT, padx=10)
        frame2 = tk.Frame(self)
        frame2.pack(fill='x')
        # label = tk.Label(frame, text='*Choose the AI firstly and play the game', height=2, width=8)
        tk.Button(frame2, text='Confirm', command=self.clicked).pack(side=tk.RIGHT, padx=10)

    def clicked(self):
        """
        Exception handling when creating AI difficulty which not in 1-10 level in the window
        :return:
        """
        try:
            level = int(self.level.get())
            if level>10 or level<0:
                messagebox.showwarning(title='Warning',message='Input right level(1~10)!')
                return
            self.level_result = level
            #close the window
            self.quit()
            self.destroy()
        except:
            messagebox.showwarning(title='Warning',message='Input right level(1~10)!')

DEPTH = 3

#initialize
pygame.init()

#load assets
checker_icon = pygame.image.load("checker_icon.png")
board_bg = pygame.image.load("checkers_bg.png")
red_checker = pygame.image.load("checker_red.png")
black_checker = pygame.image.load("checker_black.png")
red_checker_king = pygame.image.load("checker_red_king.png")
black_checker_king = pygame.image.load("checker_black_king.png")
selected_bg = pygame.image.load("selected.png") #selected button's background
button_bg = pygame.image.load("button_bg2.png") #button's background
button_bg2 = pygame.image.load("button_bg3.png") #button2's background
allow_checker = pygame.image.load("checker_allow.png") #allow position of piece background

# configure settings
pygame.display.set_icon(checker_icon)
pygame.display.set_caption("checkers AI")
board_screen = pygame.display.set_mode((1300,1000))   #display window size
"""
    notice: Display incompatibility may occur in a high-resolution computers
    recommend -- 1920 X 1080
"""

# initialize board
board = GL.create_board()

# helper functions
checker_locs = [12 + 125*i for i in range(8)]

# log
game_log = []
mouse_flag = False
allow_move = []

#Vector, which check piece, whether it is lifted, checker piece position
selected = [Vector2(-1, -1), 0, False, (-1, -1)]

#Initialize fonts
pygame.font.init()
myfont = pygame.font.SysFont('Arail', 30)  #Set fonts

def render():
    """
    more about the interface and response, more about display
    :return:
    """
    board_screen.blit(board_bg, (0,0))
    for y in range(8):
        for x in range(8):
            tile = GL.get_piece(board, Vector2(x,y))
            if selected[0] != Vector2(-1, -1) and Vector2(x,y) in allow_move: #checker have been selected
                board_screen.blit(allow_checker, (checker_locs[x], checker_locs[y]))  #Show which position you can go
            if selected[0] != Vector2(-1, -1) and selected[0] == Vector2(x, y): #Checkers are not drag & drop and are selected
                board_screen.blit(selected_bg, (checker_locs[x], checker_locs[y]))
            if selected[0] != Vector2(-1, -1) and selected[0] == Vector2(x, y) and selected[2]: #Checkers have been selected and be drag & drop
                if tile == GL.EMPTY:
                    continue
                elif tile == GL.RED: #RED checker
                    board_screen.blit(red_checker, selected[3])
                elif tile == GL.BLACK: #BLACK checker
                    board_screen.blit(black_checker, selected[3])
                elif tile == GL.RED * GL.KING: #RED checker and become a KING
                    board_screen.blit(red_checker_king, selected[3])
                elif tile == GL.BLACK * GL.KING: #BLACK checker and become a KING
                    board_screen.blit(black_checker_king, selected[3])
                continue
                
            if tile == GL.EMPTY:
                continue
            elif tile == GL.RED:
                board_screen.blit(red_checker, (checker_locs[x], checker_locs[y]))
            elif tile == GL.BLACK:
                board_screen.blit(black_checker, (checker_locs[x], checker_locs[y]))
            elif tile == GL.RED * GL.KING:
                board_screen.blit(red_checker_king, (checker_locs[x], checker_locs[y]))
            elif tile == GL.BLACK * GL.KING:
                board_screen.blit(black_checker_king, (checker_locs[x], checker_locs[y]))
    #Display text for recording
    start = 0
    end = len(game_log)
    if end>16: #Only 16 rows are displayed at most
        start = end-16
    count = 0
    for i in range(start, end):
        textsurface = myfont.render(game_log[i], False, (0, 0, 0)) #Create a text picture
        board_screen.blit(textsurface,(1050, 100+count*30))        #display
        count+=1
    #display button
    board_screen.blit(button_bg, (1050, 750))
    textsurface = myfont.render('Rules', False, (0, 0, 0)) #Create rules button
    board_screen.blit(textsurface, (1100, 790))

    #AI level changing button
    board_screen.blit(button_bg2, (1050, 900))
    textsurface = myfont.render('1', False, (0, 0, 0)) #create the button image
    board_screen.blit(textsurface, (1065, 910))
    board_screen.blit(button_bg2, (1130, 900))
    textsurface = myfont.render('2', False, (0, 0, 0)) #create the button image
    board_screen.blit(textsurface, (1145, 910))
    board_screen.blit(button_bg2, (1210, 900))
    textsurface = myfont.render('3', False, (0, 0, 0)) #create the button image
    board_screen.blit(textsurface, (1225, 910))

    board_screen.blit(button_bg2, (1050, 950))
    textsurface = myfont.render('4', False, (0, 0, 0)) #create the button image
    board_screen.blit(textsurface, (1065, 960))
    board_screen.blit(button_bg2, (1130, 950))
    textsurface = myfont.render('5', False, (0, 0, 0))
    board_screen.blit(textsurface, (1145, 960))
    board_screen.blit(button_bg2, (1210, 950))
    textsurface = myfont.render('6', False, (0, 0, 0))
    board_screen.blit(textsurface, (1225, 960))


    pygame.display.update()

def get_grid_tile(px_x, px_y):
    """
    grid title
    :param px_x:
    :param px_y:
    :return:
    """
    return Vector2(px_x // 125, px_y // 125)

#The user will default to black checkers
curr_player = GL.BLACK
is_running = True
pending_move = PendingMove(board, curr_player)

# debugging
show_mouse_moves = False

#refresh
render()
#Create TK object
root = tk.Tk()
root.wm_withdraw()      #Hide the main page
#Pop-up window to selection difficulty
choice_level = Dialog()
choice_level.mainloop()
#DEPTH for setting the difficulty
DEPTH = choice_level.level_result

while is_running:

    if curr_player == GL.RED:
        start_s = time.time()
        move = ALG.minimax(board, DEPTH, float('-inf'), float('inf'), True)[0]
        end_s = time.time()
        print('move found in ' + str(round(end_s-start_s,4)) + ' seconds')
        time.sleep(1)       #Delay for 1 second to display the interface
        count = GL.execute_move(board, move)            
        game_log.append('RED (%d,%d)==>(%d,%d)'%(move.start_vec.x, move.start_vec.y, move.end_vec.x, move.end_vec.y))        #
        if count:
            game_log.append('%d BLACK has be captured'%count)          #
        pending_move.switch_player()
        curr_player *= -1
        gm = GL.game_over(board, curr_player)
        if gm:
            print([None, 'Red', 'Black'][gm] + ' Won!')
            render()    #Refresh before finishing
            messagebox.showwarning(title='End',message=str([None, 'Red', 'Black'][gm]) + ' Won!')
            is_running = False

    for event in pygame.event.get():

        if event.type == pygame.QUIT: #quit
            is_running = False
            break

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                ms = GL.get_all_potential_moves(board, curr_player)
                if len(ms) == 0:
                    print('no moves!')
                for m in ms:
                    print(m)
                print()
            
            if event.key == pygame.K_p:
                print(board)
            
            if event.key == pygame.K_t:
                print('Turn: ' + [None, 'Red', 'Black'][curr_player])
            
            if event.key == pygame.K_l:
                show_mouse_moves = not show_mouse_moves
                print('Toggled ' + ['Off', 'On'][show_mouse_moves] + ' Show Mouse Moves')

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x>1000:
                if x>=1050 and x<=1050+163 and y>=750 and y<=750+91:
                    import os
                    os.system("start notepad.exe rule.txt")
                mouse_flag = False
                continue
            mouse_flag = True
            from_vec = get_grid_tile(x, y)
            selected[2] = True #select the piece
            selected[3] = (checker_locs[from_vec.x], checker_locs[from_vec.y]) #the vector/position of the pieces
            tile = GL.get_piece(board, from_vec) #get the piece
            if tile == GL.BLACK or tile == GL.BLACK * GL.KING:  #set the checker piece(king) be selected
                selected[0] = from_vec
                selected[1] = tile
                temp_move = GL.get_potential_moves(board, from_vec)  #get the available/potential position
                allow_move = []   #initialize the moving
                try:    #try to add the move to available position
                    for i in temp_move:
                        allow_move.append(i.end_vec)
                except: #empty when you fail
                    allow_move = [] #initialize the moving
                    
            elif selected[0] != Vector2(-1, -1):    #If the piece be selected, it will not be operated
                continue
                
            if show_mouse_moves:
                print("from: " + str(from_vec))
            pending_move.set_start(from_vec)
            
        if event.type == pygame.MOUSEBUTTONUP:
            x, y = event.pos
            #select the difficulty
            if x>1050 and x<1090 and y>900 and y<940:       #AI cleverness level 1
                DEPTH = 1
                game_log.append('change AI cleverness: 1')
                continue
            if x>1130 and x<1170 and y>900 and y<940:       #AI cleverness level 2
                DEPTH = 2
                game_log.append('change AI cleverness: 2')
                continue
            if x>1210 and x<1250 and y>900 and y<940:       #AI cleverness level 4
                DEPTH = 4
                game_log.append('change AI cleverness: 3')
                continue

            if x>1050 and x<1090 and y>950 and y<990:       #AI cleverness level 5
                DEPTH = 5
                game_log.append('change AI cleverness: 4')
                continue
            if x>1130 and x<1170 and y>950 and y<990:       #AI cleverness level 7
                DEPTH = 7
                game_log.append('change AI cleverness: 5')
                continue
            if x>1210 and x<1250 and y>950 and y<990:       #AI cleverness level 9
                DEPTH = 9
                game_log.append('change AI cleverness: 6')
                continue

            if x<0 and x>1000 and y<0 and y>1000:
                continue
            if not mouse_flag:
                continue
            to_vec = get_grid_tile(x, y)
            selected[2] = False      #drop down the selected piece
            if from_vec==to_vec and GL.get_piece(board, from_vec)!=GL.EMPTY: #No moves, indicating selected
                continue
            
            if show_mouse_moves:
                print("to: " + str(to_vec))
            pending_move.set_end(to_vec)
            
            if pending_move.is_valid():
                if show_mouse_moves:
                    print('VALID')
                count = GL.execute_move(board, pending_move)
                game_log.append('BLACK (%d,%d)==>(%d,%d)'%(pending_move.start_vec.x, pending_move.start_vec.y, pending_move.end_vec.x, pending_move.end_vec.y))      #
                if count:
                    game_log.append('%d RED has be captured'%count)
                selected = [Vector2(-1, -1), 0, False, (-1, -1)]    #reset
                pending_move.switch_player()
                curr_player *= -1
                gm = GL.game_over(board, curr_player)
                if gm:
                    print([None, 'Red', 'Black'][gm] + ' Won!')
                    render()  #refresh before finishing
                    messagebox.showwarning(title='End',message=str([None, 'Red', 'Black'][gm]) + ' Won!')
                    is_running = False
            else:
                if show_mouse_moves:
                    print('NOT VALID')
                pending_move.reset()

        if event.type == pygame.MOUSEMOTION:
            x, y = event.pos
            #preventing out of the page
            if x>=0 and x<=900 and y>=0 and y<=1000:
                if selected[0] != Vector2(-1, -1) and selected[0] != get_grid_tile(x,y): #piece is not in the selected position
                    selected[3] = (x, y)  #set the position
                    render()
        
    render()


pygame.display.quit()
pygame.quit()
exit()
