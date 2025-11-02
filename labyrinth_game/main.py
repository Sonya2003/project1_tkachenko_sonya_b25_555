#!/usr/bin/env python3

from constants import ROOMS
from utils import describe_current_room, solve_puzzle, show_help, attempt_open_treasure
from player_actions import show_inventory, get_input, move_player, take_item, use_item


game_state = {
    'player_inventory': [], # Инвентарь игрока
    'current_room': 'entrance', # Текущая комната
    'game_over': False, # Значения окончания игры
    'steps_taken': 0 # Количество шагов
}
  
def process_command(game_state, command):

    parts = command.split()

    if not parts:
        return

    action = parts[0]

    directions = ["north", "south", "east", "west"]
    if action in directions:
        move_player(game_state, action)
        return

    match action:

        case "look":
            describe_current_room(game_state)

        case "use":
            if len(parts) > 1:
                item_name = parts[1]
                use_item(game_state, item_name)
            else:
                print("Укажите предмет: use [название предмета]")

        case "go":

            if len(parts) > 1:
                direction = parts[1]
                move_player(game_state, direction)
            else:
                print("Укажите направление: go north/south/east/west")

        case "take":
            if len(parts) > 1:
               item_name = parts[1] 
               take_item(game_state, item_name)
            else:
                print("Укажите предмет.")
        
        case "inventory":
            show_inventory(game_state)

        case "quit" | "exit":
            game_state['game_over'] = True
            print("Игра окончена.")

        case "solve":
            if game_state["current_room"] == "treasure_room":
                attempt_open_treasure(game_state)
            else:
                solve_puzzle(game_state)

        case "help":
            show_help()

def main():
    print("Добро пожаловать в Лабиринт сокровищ!")
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = input("\nВведите команду: ")
    
        process_command(game_state, command)

if __name__ == "__main__":
    main()
