import time
from tkinter import *
import math
import numpy as np

# Импортируем нейросеть
import agent_control.network as nl
# Инициализируем нейросеть
net_scheme = [4, 10, 10, 4] # схема нейронной сети
bias_scheme = [False, True, True, True] # схема нейронов смещения
learning_rate = 0.05 # Коеффициент обучения
network = nl.network_init(net_scheme, bias_scheme)
err_gen = nl.ErrorGenerator() # Генератор ошибок, то что будет обучать агента
backward = nl.Backward(learning_rate) # модуль обратного распространения и обучения
forward = nl.predict_full # функция прямого распространения по всей сети
target_coordinates = (388.0, 458.0) 

count = 0


# Импортируем и инициализируем среду
import labyrinth.Contact as labyrinth

root = labyrinth.tk  # Получаем корневой виджет Tkinter

def drawTarget(canvas, x, y, size=5, color='green'):
    """
    Функция для отрисовки значка цели на карте.
    
    Параметры:
    canvas (tkinter.Canvas) - холст, на котором будет отрисован значок цели.
    x, y (int) - координаты центра значка цели.
    size (int) - размер значка цели.
    color (str) - цвет значка цели.
    """
    # Вычисляем координаты левого верхнего угла значка
    left = x - (size // 2)
    top = y - (size // 2)
    
    # Создаем овальный значок цели
    target = canvas.create_oval(left, top, left + size, top + size, fill=color, outline='')
    
    return target

def trascriptAnswer(vecctor):
    key_map = {
    0: "Left",
    1: "Right",
    2: "Up",
    3: "Down"
}
    choise = np.argmax(vecctor)
    key_symbol = key_map.get(choise, "")
    return choise, key_symbol

def calculateReward(distance):
    if not hasattr(calculateReward, "prev_distance"):
        calculateReward.prev_distance = 0
    reward = 0
    if calculateReward.prev_distance == distance:
        reward = reward - 0.001
    else:
        reward = 1 / (abs(distance))
    calculateReward.prev_distance = distance
    return reward

def second_cycle():
    global count
    global target_coordinates
    gamma = 0.9

    state = network[0].Out
    # вызываем решение неейросети с прошлой итерации (позже надо будет метод написать)
    prev_predicted_rewards = network[len(network)-1].Out
    # обращаемся к дополнительному модулю для трансфера ответа нейросети в нажатие кннопки.
    action, key_symbol = trascriptAnswer(prev_predicted_rewards) # в action нужно решение для текущих данных (можно получить с прошлой итерации)
    # Среда выполняет действие
    labyrinth.canvas.event_generate(f"<KeyPress-{key_symbol}>")
    # Надо собрать данные, новое состояние и награду

    # В начале нам надо собрать данные
    current_coordinates = labyrinth.obj.getCoords()

    x_diff = target_coordinates[0] - current_coordinates[0]
    y_diff = target_coordinates[1] - current_coordinates[1]
    distance = math.sqrt(x_diff**2 + y_diff**2)

    # конвертируем данные в вектор нейросети
    next_state = np.hstack((np.array(target_coordinates), np.array(current_coordinates))).reshape(1, -1)
    next_state = nl.normalize_data(next_state)

    # Запускаем вычислитель награды
    reward = calculateReward(distance)

    # Вычисляем предсказание награды на следующем шагу
    network[0].Out = next_state
    predicted_rewards = forward(network)
    td_target = reward + gamma * np.max(predicted_rewards) # Нужен вектор решений для новых данных
    # т.е. на прошлом шагу должно было получиться это
    # но нейронка предсказала это prev_predicted_rewards
    # td_error = td_target - np.max(prev_predicted_rewards)
    td_error = np.max(prev_predicted_rewards) - td_target

    # принудительно переписываем значения чтобы понять как работает
    # td_error = 0.1 # ошибка
    # action = 0 # на индексе

    print("reward: ", reward)
    print("PRreward: ", prev_predicted_rewards)
    print("target: ", td_target)
    print("error: ", td_error)
    print("choise: ", action)
    print(network[len(network)-1].Out)
    # Создаём и передаём нейросети вектор ошибок
    network[len(network)-1].E_Out = np.zeros_like(network[len(network)-1].E_Out)
    network[len(network)-1].E_Out += 0.0001
    network[len(network)-1].E_Out[0][action] = td_error
    # Запускаем обучение
    backward.full_net(network)

    
    if count > 100:
        print(action)
        print(reward)
        print("ERROR", network[len(network)-1].E_Out[0][action])
        count = 0
    count = count + 1




    if target_coordinates == current_coordinates: 
        print('!!!DONE!!!')
        


    # labyrinth.canvas.event_generate("<KeyPress-Left>")
    # print('object X:', labyrinth.obj.x)
    root.after(50, second_cycle)  # Интервал работы нейросети


drawTarget(labyrinth.canvas, target_coordinates[0], target_coordinates[1])
network[0].Out = network[0].Out + 0.00001

root.after(0, second_cycle)  # Запускаем Вторичный цикл для работы нейросети


root.mainloop()