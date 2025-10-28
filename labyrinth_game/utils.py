from constants import ROOMS
from player_actions import get_input

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

    user_answer = get_input("Ваш ответ: ")

    if user_answer.lower() == correct_answer.lower():
        print("Загадка решена.")
        room["puzzle"] = None
        game_state["player_inventory"].append("gold_doubloon")
	print("Вы получили награду: золотой дублон!")
    else:
        print("Неверно. Попробуйте снова.")

def show_help():
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
