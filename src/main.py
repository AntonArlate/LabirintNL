import time
from tkinter import *

# Импортируем нейросеть
import agent_control.network as nl
# Инициализируем нейросеть
net_scheme = [4, 3, 3, 4] # схема нейронной сети
bias_scheme = [False, True, True, True] # схема нейронов смещения
learning_rate = 0.01 # Коеффициент обучения
network = nl.network_init(net_scheme, bias_scheme, learning_rate)
err_gen = nl.ErrorGenerator() # Генератор ошибок, то что будет обучать агента
backward = nl.Backward() # модуль обратного распространения и обучения
forward = nl.predict_full() # функция прямого распространения по всей сети


# Импортируем и инициализируем среду
import labyrinth.Contact as labyrinth

root = labyrinth.tk  # Получаем корневой виджет Tkinter

def second_cycle():

    # В начале нам надо собрать данные

    # labyrinth.canvas.event_generate("<KeyPress-Left>")
    # print('object X:', labyrinth.obj.x)
    root.after(500, second_cycle)  # Интервал работы нейросети



root.after(0, second_cycle)  # Запускаем Вторичный цикл для работы нейросети


root.mainloop()