#COLUMN, ROW

import os
import random

u_lost = False

class Tile:

    def __init__(self):
        self.coords = (0,0)
        self.mine = False
        self.number = 0
        self.revealed = False
        self.flag = False
    
    def __repr__(self):
        if self.flag == True:
            visual = "[*]"
            return visual
        if self.revealed == True:
            if self.mine == False:
                if self.number != 0:
                    visual = f"[{self.number}]"
                else:
                    visual = "[ ]"
            else:
                visual = "[!]"
        else:
            visual = "[X]"
        return visual
    
    def reveal(self):
        x = self.coords[0]
        y = self.coords[1]
        if self.revealed == False:
            self.revealed = True
            if self.mine == True:
                global u_lost
                u_lost = True
            if self.number == 0:
                if (x+1, y) in tiles_dict:
                    tiles_dict[(x+1, y)].reveal()
                if (x, y+1) in tiles_dict:
                    tiles_dict[(x, y+1)].reveal()
                if (x-1, y) in tiles_dict:
                    tiles_dict[(x-1, y)].reveal()
                if (x, y-1) in tiles_dict:
                    tiles_dict[(x, y-1)].reveal()
                if (x+1, y+1) in tiles_dict:
                    tiles_dict[(x+1, y+1)].reveal()
                if (x-1, y-1) in tiles_dict:
                    tiles_dict[(x-1, y-1)].reveal()
                if (x-1, y+1) in tiles_dict:
                    tiles_dict[(x-1, y+1)].reveal()
                if (x+1, y-1) in tiles_dict:
                    tiles_dict[(x+1, y-1)].reveal()
            
def ask_input():
    global board_size, num_mine
    os.system("clear")
    print("Enter a board size that is a square :)) between ≥ 3x3 and ≤ 10x10")
    board_size_str = input()
    os.system("clear")
    board_size = tuple(map(int, board_size_str.split("x")))

    print("Enter a mine number that makes sense")
    num_mine = int(input())
    os.system("clear")

def create_board():
    global tiles_dict
    tiles_dict = {}
    for column in range(board_size[0]):
        for row in range(board_size[1]):
            tiles_dict[(column, row)] = Tile()
            tiles_dict[(column, row)].coords = (column, row)

def place_mines():
    mines_list = random.sample(list(tiles_dict), num_mine)
    for item in mines_list:
        tiles_dict[item].mine = True

def create_numbers():
    for key in tiles_dict:
        mine_tracker = 0
        neighbourhood = [(key[0], key[1]), (key[0]+1, key[1]), (key[0], key[1]+1), (key[0]-1, key[1]), (key[0], key[1]-1), (key[0]+1, key[1]+1), (key[0]-1, key[1]-1), (key[0]+1, key[1]-1), (key[0]-1, key[1]+1)]
        for n in neighbourhood:
            if n in tiles_dict:
                if tiles_dict[n].mine == True:
                    mine_tracker += 1
        tiles_dict[key].number = mine_tracker

def find_start_tile():
    global start_tile
    valid_tile_found = False
    while valid_tile_found == False:
        start_tile = random.choice(list(tiles_dict))
        if tiles_dict[start_tile].number == 0:
            tiles_dict[start_tile].reveal()
            break

def print_board():
    column_tracker = 0
    row_tracker = 0
    print("   ", end="")
    print("".join(" "+str(num)+" " for num in list(range(board_size[0]))))
    for key in tiles_dict.keys():
        if column_tracker == 0:
            print(f" {row_tracker} ", end="")
        print(tiles_dict[key], end="")
        column_tracker += 1
        if column_tracker % board_size[0] == 0:
            print()
            row_tracker += 1
            column_tracker = 0

def start_game():
    os.system("clear")
    if u_lost == True:
        print("YOU LOST")
        print()
        return
    win = True
    for key in list(tiles_dict):
        if tiles_dict[key].mine == True and tiles_dict[key].flag != True:
            win = False
        if tiles_dict[key].mine == False and tiles_dict[key].reveal == False:
            win = False
    if win == True:
        print("YOU WON")
        return
    print("Write r to reveal or f to flag")
    print()
    print_board()
    print()
    mode = input()
    os.system("clear")
    print("Select a tile using this format: row,column")
    print()
    print_board()
    print()
    selected_tile_str = input()
    selected_tile = tuple(map(int, selected_tile_str.split(",")))
    if mode == "r":
        tiles_dict[selected_tile].reveal()
    else:
        tiles_dict[selected_tile].flag = True

    start_game()

ask_input()
create_board()
place_mines()
create_numbers()
find_start_tile()
start_game()