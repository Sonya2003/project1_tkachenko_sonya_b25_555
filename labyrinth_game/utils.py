from constants import ROOMS

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
