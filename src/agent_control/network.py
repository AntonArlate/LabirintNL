# https://www.youtube.com/watch?v=xMz7XSaqdRA&t=117s
# Реализация нейросети при помощи numpy

import numpy as np

INPUT_DIM = 4 # количество входных значений
OUT_DIM = 3 # количество вsходных значений
H_DIM = 5 # количество нейронов на слое (пока 1 слой)

x = np.random.randn(INPUT_DIM) # Входящий вектор, пока задаётся случайными значениям т.е. массив x(INPUT_DIM)

w1 = np.random.randn(INPUT_DIM, H_DIM) # Матрица весов от одного слоя к другому
b1 = np.random.randn(H_DIM) # это массив весов для нейрона смещения (при его наличии)
w2 = np.random.randn(H_DIM, OUT_DIM) 
b2 = np.random.randn(OUT_DIM)

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

probs = predict(x)
pred_class = np.argmax(probs) # Это наш ответ в виде индекса нейрона выхода
print('choice:', pred_class)