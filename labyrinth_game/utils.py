import math
from constants import ROOMS
from player_actions import get_input
from const import COMMANDS

def describe_current_room(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    print(f"\n== {current_room_name.upper()} ==")
    print(room['description'])
    if room['items']:
        print("Заметные предметы:", ",".join(room['items']))
    print("Выходы:", ",".join(room['exits'].keys()))
    if room['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")


def attempt_open_treasure(game_state):
    current_room_name = game_state["current_room"]
    room = ROOMS[current_room_name]

    if 'treasure_key' in game_state["player_inventory"]:
        print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
        if 'treasure_chest' in room["items"]:
            room["items"].remove('treasure_chest')
        print("В сундуке сокровище! Вы победили!")

        game_state["game_over"] = True
        return
    else:
        print("Сундук заперт кодом. У вас нет ключа, но можно попробовать ввести код.")
        answer = get_input("Ввести код? (да/нет): ")

        if answer.lower() == "да":
            if room["puzzle"]:
                question, correct_answer = room["puzzle"]
                user_code = get_input("Введите код: ")
                if user_code.lower() == correct_answer:
                    print("Код верный! Замок щёлкает, и сундук открывается.")
                    if 'treasure_chest' in room["items"]:
                        room["items"].remove('treasure_chest')
                    print("В сундуке сокровище! Вы победили!")
                else:
                    print("Неверный код. Сундук остается запертым.")
        else:
            print("Вы отступаете от сундука.")


def solve_puzzle(game_state):
    current_room_name = game_state['current_room']
    room = ROOMS[current_room_name]

    if current_room_name == 'treasure_room':
        attempt_open_treasure(game_state)
        return

    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room["puzzle"]
    print(f"Загадка: {question}")

    user_answer = get_input("Ваш ответ: ").strip().lower()
    number_words = {
    "10": ["10", "десять"],
    "22": ["22", "двадцать два"]
    }
    acceptable_answers = number_words.get(correct_answer, [correct_answer.lower()])
    if user_answer in acceptable_answers:
        print("Загадка решена.")
        room["puzzle"] = None
        game_state["player_inventory"].append("gold_doubloon")
        print("Вы получили награду: золотой дублон!")
    else:
        print("Неверно. Попробуйте снова.")
        if current_room_name == "trap_room":
            print("Неверный ответ. Ловушка активирована.")
            trigger_trap(game_state)

def pseudo_random(seed, modulo):
    x = math.sin(seed*12.9898) * 43758.5453
    x1 = x - math.floor(x)    
    return int(x1*modulo)
    
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    inventory = game_state['player_inventory']
    if inventory:
        modulo = len(inventory)
        random_index = pseudo_random(game_state['steps_taken'], modulo) % modulo
        lost_item = inventory.pop(random_index)
        print(f"Вы потеряли предмет: {lost_item}")
    else:
        random_value = pseudo_random(game_state['steps_taken'], 10)
        if random_value < 3:
            print("Вас настигла ловушка! Игра окончена.")
            game_state['game_over'] = True
        else:
            print("Вам удалось увернуться от ловушки! Вы уцелели.")

def random_event(game_state):
    if pseudo_random(game_state['steps_taken'], 10) == 0:
        event_type = pseudo_random(game_state['steps_taken'] + 1, 3)
        if event_type == 0:
            print("Вы нашли монету.")
            current_room = game_state['current_room'] 
            game_state['current_room'][current_room]['items'].append('coin')
        if event_type == 1:
            print("Вы слышите шорох.")
            if 'sword' in game_state['player_inventory']:
                print("У вас есть меч. Вы отпугнули существо.")
            else:
                print("Вы наткнулись на страшное существо.")
        if event_type == 2:
            if game_state['current_room'] == 'trap_room' and 'torch' not in game_state['inventory']:
                print("Вы в опасности!")
                trigger_trap(game_state)
            else:
                print("Вам удалось избежать попадания в ловушку.")

def show_help():
    print("\nДоступные команды:")
    print("-" * 50)
    for command, description in COMMANDS.items():
        formatted_command = command.ljust(16)
        print(f" {formatted_command} - {description}")
    print("-" * 50)
