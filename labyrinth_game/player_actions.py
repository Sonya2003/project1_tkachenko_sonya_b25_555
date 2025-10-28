def show_inventory(game_state):
    inventory = game_state['player_inventory']
    if inventory:
        print("Ваш инвентарь:", ",".join(inventory).)
    else:
        print("Ваш инвентарь пуст.")

def get_input(prompt="> "):
    try:
    user_input = input(prompt)
    return user_input.strip().lower()    

    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def move_player(game_state, direction):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]

    if direction in current_room["exits"]:
        game_state["current_room"] = current_room["exits"][direction]
        game_state["steps_taken"] += 1
        describe_current_room(game_state)
    else:
        print("Нельзя пойти в этом направлении.")

def take_item(game_state, item_name):
    current_room_name = game_state["current_room"]
    current_room = ROOMS[current_room_name]

    if item_name in current_room['items']:
        game_state['player_inventory'].append(item_name)
        current_room["items"].remove(item_name)
        print(f"Вы подняли: {item_name}.")
    else:
        print("Такого предмета здесь нет.")

def use_item(game_state, item_name):
    if item_name not in game_state['player_inventory']:
        print("У вас нет такого предмета.")
        return 

    match item_name:
        case "torch":
            print("Вы зажгли факел. Стало светлеt.")
        case "sword":
            print("Вы почувствовали уверенность в своих силах, держа меч в руках.")
        case "bronze box":
            print("Вы открыли бронзовую шкатулку.")
            if "rusty_key" not in game_state['player_inventory']:
                game_state["player_inventory"].append("rusty_key")
                print("Внутри вы нашли rusty_key!")
            else:
                print("Шкатулка пуста.")
        case _:
             print(f"Вы не знаете, как использовать {item_name}.")        


