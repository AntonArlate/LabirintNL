import numpy as np
import math
import time


class Layer:
    weight=[]#link weights
    vector=[]#output signsls
    def __init__(self,neurons_cnt,links_cnt,layer_cnt):
        self.layer_cnt=layer_cnt
        self.weight=np.ones((links_cnt,neurons_cnt))
        np.random.seed(1)
        for i in range(self.weight.shape[0]):
            for j in range(self.weight.shape[1]):
                self.weight[i,j]=np.random.random()
        #         #self.weight[i,j]=j

        self.alpha=0.3

    def __str__(self):
        return "Layer {}\n{}".format(self.layer_cnt,self.weight)


    def output(self,vector):#direct signal
        self.vector=vector.copy()#get output signals of the layer
        res=self.weight.dot(vector)#setup common signal for the next layer

        res=1/(1+math.e**(-res))#setup output signal for the next layer

        #print("{}\n{}".format(self.layer_cnt,res))
        #print("============================================")
        return res



    def checkError(self,vector):

        #print(f"Layer:{self.layer_cnt}")
        t_weight=self.weight.transpose()#get each neuron weight in strings
        #print("============================================")
        #print(t_weight)
        vector=t_weight.dot(vector)#get error per neuron
        #print("============================================")
        #print(vector)
        #print("============================================")
        #print(self.vector)
        #print("============================================")
        self.vector=vector*self.vector*(1-self.vector)*self.vector*self.alpha#back propagation equasion
        #print(self.vector)
        #print("============================================")
        self.weight+=self.weight*self.vector.transpose()#change layer weights
        #print(self.weight)
        #print("============================================")

        return vector


l1=Layer(2,3,1)
l2=Layer(3,2,2)
l3=Layer(2,2,3)

print("{}\n{}\n{}".format(l1,l2,l3))
print("============================================")

w_field=300
h_field=300
y=180

#e=np.array([[1],[1]])
res=np.array([[0],[0]])

for x in range(50,60,1):

    v_in=np.array([[x/w_field],[y/h_field]])
    print(v_in)
    print("=============================================================================================")

    i = 0
    j = 0
    while res[0,0]<0.8 or (res[1,0]<0.4 or res[1,0]>0.6):
        time.sleep(0.01)
        i += 1
        # A: получаем результат нейросети
        res=l2.output(l1.output(v_in))

        #print(f"{res[0,0]*w_field}, {res[1,0]*h_field}")

        # A: вычисляем ошибку вычитая координаты цели из результата
        e=np.array([[0.8-res[0,0]],[0.5-res[1,0]]])

        if i > (j + 100):
          print(e)
          j = i
        # print("============================================")

        # Запускаем обучение
        l1.checkError(l2.checkError(e))

