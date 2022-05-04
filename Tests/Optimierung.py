from scipy.optimize import minimize
someNumber = 10
a = 1
b = 2
c = 3
Liste = {"Eins": [1,1,1], "Zwei": [2, 2, 2], "Drei": [3,3,3]}

def f(someNumber, a, b, c):
    for DT in Liste:
        Wert =
    someNumber = a + b + c
    return someNumber

erg = minimize(f, someNumber, args=(a, b, c))
print(erg)