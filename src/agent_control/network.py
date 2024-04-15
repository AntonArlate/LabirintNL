# https://www.youtube.com/watch?v=xMz7XSaqdRA&t=117s
# Реализация нейросети при помощи numpy

import time
import numpy as np

def relu(t):
    return np.maximum(t, 0) # Всё также используется numpy которая получая вектор, вернёт также вектор

def softmax(t):
    out = np.exp(t) 
    return out / np.sum(out)

def predict(x):
    t1 = x @ w1 + b1 # Перемножаем входной вектор на матрицу весов получая вектор второй размерности матрицы (количество нейронов далее). Затем прибавляем смещение.
    h1 = relu(t1) # Пропускаем вектор t1 через функцию активации.
    t2 = h1 @ w2 + b2 # Получаем значения на нейронах выхода
    z = softmax(t2)
    return z


# -------
# Модуль отвечающий за обучение. Должен принять вектор ошибок и выполнить обучение

# -------
# Модуль генерации ошибки. Должен вычислить ошибку согласно алгоритму
class ErrorGenerator:
    def __init__(self):
        self.prev_predict = 0 # предсказание на предыдущем шаге

    def calculate(self, vecctor, choise):
        if (self.prev_predict == 0):
            self.prev_predict = vecctor[choise]
        else: 
            error = vecctor[choise] - self.prev_predict # возможно наоборот
            self.prev_predict = vecctor[choise]
            return error


if __name__ == '__main__':

    INPUT_DIM = 4 # количество входных значений
    OUT_DIM = 3 # количество вsходных значений
    H_DIM = 5 # количество нейронов на слое (пока 1 слой)
    err_gen = ErrorGenerator()

    previous_step = 0

    x = np.random.randn(INPUT_DIM) # Входящий вектор, пока задаётся случайными значениям т.е. массив x(INPUT_DIM)

    w1 = np.random.randn(INPUT_DIM, H_DIM) # Матрица весов от одного слоя к другому
    b1 = np.random.randn(H_DIM) # это массив весов для нейрона смещения (при его наличии)
    w2 = np.random.randn(H_DIM, OUT_DIM) 
    b2 = np.random.randn(OUT_DIM)

for i in range(1, 6):
    print("Итерация", i)
    time.sleep(1)
    #* Нейросеть считает ожидаемую награду за действия и выбирает необходимое. 
    predicted_rewards = predict(x)
    # На выходных нейронах мы будем получать рассчитаную награду за действия
    choise = np.argmax(predicted_rewards) # Это наш ответ в виде индекса нейрона выхода
    print('choice:', choise)

    #! Получается что мы будем сначала сканировать всё окружение и передавать все значения сканера одним вектором.

    #* Среда выполняет действие.
    x = np.random.randn(INPUT_DIM)

    #* Отправляем задачу в модуль вычисления ошибки. У нас есть текущий вектор решений и выбор. Их и будем передавать
    error = err_gen.calculate(predicted_rewards, choise)

    #* Запускаем обучение