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

def draw_target(canvas, x, y, size=5, color='green'):
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

def second_cycle():
    global count
    # В начале нам надо собрать данные
    global target_coordinates
    current_coordinates = labyrinth.obj.getCoords()

    x_diff = target_coordinates[0] - current_coordinates[0]
    y_diff = target_coordinates[1] - current_coordinates[1]
    distance = math.sqrt(x_diff**2 + y_diff**2)
    reward = 1 / (abs(distance) + 1)
    

    # передаём в нейросеть данные
    incoming_data = np.hstack((np.array(target_coordinates), np.array(current_coordinates))).reshape(1, -1)
    incoming_data = nl.normalize_data(incoming_data)
    network[0].Out = incoming_data
    # передаём данные на решение неейросети
    predicted_rewards = forward(network)
    # обращаемся к дополнительному модулю для трансфера ответа нейросети в нажатие кннопки.
    choise, key_symbol = trascriptAnswer(predicted_rewards)
    # Отправляем задачу в модуль вычисления ошибки. 
    network[len(network)-1].E_Out = err_gen.calculate(predicted_rewards, choise, reward) 
    
    if count > 100:
        print(choise)
        print(reward)
        print("ERROR", network[len(network)-1].E_Out[0][choise])
        count = 0
    count = count + 1

    # Запускаем обучение
    backward.full_net(network)
    # Среда выполняет действие
    labyrinth.canvas.event_generate(f"<KeyPress-{key_symbol}>")

    if target_coordinates == current_coordinates: 
        print('!!!DONE!!!')
        


    # labyrinth.canvas.event_generate("<KeyPress-Left>")
    # print('object X:', labyrinth.obj.x)
    root.after(5, second_cycle)  # Интервал работы нейросети


draw_target(labyrinth.canvas, target_coordinates[0], target_coordinates[1])
root.after(0, second_cycle)  # Запускаем Вторичный цикл для работы нейросети


root.mainloop()