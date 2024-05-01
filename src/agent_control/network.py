# https://www.youtube.com/watch?v=xMz7XSaqdRA&t=117s
# Реализация нейросети при помощи numpy

import time
import numpy as np

import numpy as np

class Layer:
    def __init__(self, N, bias=False):
        self.N = N
        self.Out = np.zeros((1, N))
        self.In = np.zeros(N)
        self.E_In = np.zeros(N)
        self.E_Out = np.zeros(N)
        self.bias = bias
        if bias:
            self.b = np.zeros((1, N))
            self.E_b = np.zeros((1, N))
            self.bias_value = True
        else:
            self.bias_value = False
        self.prev_layer = None
        self.next_layer = None

    def set_prev_layer(self, prev_layer):
        self.prev_layer:Layer = prev_layer
        if prev_layer is not None:
            m = prev_layer.N
            n = self.N
            self.w = np.random.uniform(-1, 1, (m, n))
            self.E_w = np.zeros((m, n))

    def set_next_layer(self, next_layer):
        self.next_layer:Layer = next_layer


def relu(t):
    a = -0.01
    x = np.maximum(t, 0)
    x[x == 0] = a * t[x == 0]
    return x # Всё также используется numpy которая получая вектор, вернёт также вектор

def deriv_relu(t):
    a = -0.1
    x = np.where(t > 0, 1, a)
    return x


def softmax(t):
    out = np.exp(t) 
    return out / np.sum(out)

def predict(x):
    t1 = x @ w1 + b1 # Перемножаем входной вектор на матрицу весов получая вектор второй размерности матрицы (количество нейронов далее). Затем прибавляем смещение.
    h1 = relu(t1) # Пропускаем вектор t1 через функцию активации.
    t2 = h1 @ w2 + b2 # Получаем значения на нейронах выхода
    z = softmax(t2)
    return z

def predict_full(network):
    lastIndex = len(network) - 1
    
    i = 1
    while i <= lastIndex:
        layer:Layer = network[i]
        layer.In = layer.prev_layer.Out @ layer.w + layer.b
        layer.Out = relu(layer.In)
        i += 1
    # z = softmax(network[i - 1].In)
    # отключаем нормализацию, теперь получаем чистые значения
    z = network[i - 1].In
    return z
    



# -------
# Модуль отвечающий за обучение. Должен принять вектор ошибок и выполнить обучение

class Backward:
    def one_lay(self, layer: Layer):
        # Потребуется для каждого слоя:
        # {i} буду отмечать как индекс слоя
        # dE|dt{i} Выход ошибки на текущем слое
        # dE|dw{i} = h{i-1}.T @ dE|dt{i} Важно понимать что индекс весов равен индексу следующего в прямом порядке слою
        # dE|db{i} = dE|dt {i}
        # dE|dh{i-1} = dE|dt{i} @ w{i}.T
        # dE|dt{i-1} = dE|dh{i-1} * deriv(t{i-1}) ; t - вход слоя
        # на этом мы получаем исходящую ошибку для предыдущего слоя
        # далее запуск обучения выглядит следующим образом
        # w{i} = w{i} - ALPHA * dE|dw{i} ; ALPHA - коофициент обучения



        LEARNING_RATE = 0.1

        layer.E_w = layer.prev_layer.Out.T @ layer.E_Out
        layer.E_b = layer.E_Out
        layer.prev_layer.E_In = layer.E_Out @ layer.w.T
        layer.prev_layer.E_Out = layer.prev_layer.E_In * deriv_relu(layer.prev_layer.In)

        layer.w = layer.w - LEARNING_RATE * layer.E_w
        layer.b = layer.b - LEARNING_RATE * layer.E_b

    def full_net(self, network: list[Layer]):
        layer = network[len(network)-1]
        while layer.prev_layer != None:
            self.one_lay(layer)
            layer = layer.prev_layer
        pass

# -------
# Модуль генерации ошибки. Должен вычислить ошибку согласно алгоритму

class ErrorGenerator:
    def __init__(self):
        self.prev_predict = -1 # предсказание на предыдущем шаге
        self.prev_vecc = 0
        self.vecctor_error = 0
        self.prev_choise = -1

    def calculate(self, vecctor, choise, env_reward):
        # Задача получив значение награды, сравнить её с ожидаемой на прошлом шаге.
        # если полученая награда больше ожидаемой, подаётся отрицательная разность для обучения на данный шаг
        if (self.prev_predict == -1):
            self.prev_predict = vecctor[0, choise]
            self.prev_choise = choise
            self.prev_vecc = vecctor

        # self.vecctor_error = vecctor - self.prev_vecc 
        self.vecctor_error = self.prev_vecc - self.prev_vecc # так мы зануляем вектор
        self.vecctor_error[0, self.prev_choise] = self.prev_predict - env_reward

        # записываем шаг
        self.prev_predict = vecctor[0, choise]
        self.prev_choise = choise
        self.prev_vecc = vecctor
        
        # тут мы получим dE|dt для выходного слоя
        return self.vecctor_error
            
            # error = vecctor[choise] - self.prev_predict # возможно наоборот
            # self.prev_predict = vecctor[choise]
            # return error
    
    def get_vecctor_error (self):
        return self.vecctor_error
        
    # y_full = np.zeros((1, 111))
    # Нам надо заполнить правильными ответами. Что есть правильный ответ в нашей задаче?
    # это то на сколько выбраный шаг оказался близок к ожидаемому.
    # Если для обычной функции разница y>p , передаётся положительная коррекция
    # То для нас если передсказане p < f (факта), используем стандарт с коррекцией к этому факту
    # Если p>f значит не оправдало ожиданий и передаём отрицательную коррекцию
    # можно будет допустим потом нормализовать при помощи к примеру функции активации


if __name__ == '__main__':
   
    # Попробуем инициализировать сеть при помощи класса. Передаём схему в виде массива
    def network_init(net_scheme, bias_scheme):
        network: list[Layer] = []
        for N_in_layer, bias_in_layer in zip(net_scheme, bias_scheme):
            new_layer = Layer(N_in_layer, bias_in_layer)    
            network.append(new_layer)
            i = network.index(new_layer)
            if i != 0:
                network[i].set_prev_layer(network[i-1])
                network[i-1].set_next_layer(network[i])
        return network

    net_scheme = [4, 3, 3, 4]
    bias_scheme = [False, True, True, True]
    network = network_init(net_scheme, bias_scheme)
    INPUT_DIM = network[0].N # количество входных значений
    OUT_DIM = network[2].N # количество вsходных значений
    H_DIM = network[1].N # количество нейронов на слое (пока 1 слой)
    err_gen = ErrorGenerator()
    backward = Backward()

    previous_step = 0

    x = np.random.randn(INPUT_DIM) # Входящий вектор, пока задаётся случайными значениям т.е. массив x(INPUT_DIM)
    network[0].Out = np.random.randn(*network[0].Out.shape)
    x = network[0].Out

    w1 = np.random.randn(INPUT_DIM, H_DIM) # Матрица весов от одного слоя к другому
    w1 = network[1].w
    b1 = np.random.randn(H_DIM) # это массив весов для нейрона смещения (при его наличии)
    b1 = network[1].b

    w2 = np.random.randn(H_DIM, OUT_DIM) 
    w2 = network[2].w
    b2 = np.random.randn(OUT_DIM)
    b2 = network[2].b

    environment_reward = 0
for i in range(1, 6000):
    print("Итерация", i)
    time.sleep(0.1)
    #* Нейросеть считает ожидаемую награду за действия и выбирает необходимое. 
    # predicted_rewards = predict(x)
    # теперь x это выход слоя 0 но также мы теперь можем передать всю сеть, а функция разберётся
    predicted_rewards = predict_full(network)
    # На выходных нейронах мы будем получать рассчитаную награду за действия
    choise = np.argmax(predicted_rewards) # Это наш ответ в виде индекса нейрона выхода
    
    print('choice:', choise)

    #! Получается что мы будем сначала сканировать всё окружение и передавать все значения сканера одним вектором.

    #* Отправляем задачу в модуль вычисления ошибки. У нас есть текущий вектор решений и выбор. Их и будем передавать
    # error = err_gen.calculate(predicted_rewards, choise)
    dE_dt2 = err_gen.calculate(predicted_rewards, choise, environment_reward) # получили вектор выхода ошибок для слоя OUT
    
    network[len(network)-1].E_Out = dE_dt2
    
    print('errors:', dE_dt2)
    print('out:', network[3].Out)

    #* Запускаем обучение
    backward.full_net(network)

        #* Среда выполняет действие.
    # x = np.random.randn(INPUT_DIM)
    # network[0].Out = np.random.randn(INPUT_DIM)
    # Симулируем награду от среды, так чтобы нейронка двигалась всегда по индексу 2 (выдавала число 3)
    
    if choise == 2:
        environment_reward = 1
    else:
        environment_reward = -1