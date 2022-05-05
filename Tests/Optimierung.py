from scipy.optimize import minimize

Liste = {"Eins": [1,1,1], "Zwei": [2, 2, 2], "Drei": [3,3,3]}

def f(a, b, c):
    Güte = a + b + 2*c
    return Güte

Hersteller = {}

for DT in Liste:
    Güte = Liste[DT][0] + Liste[DT][1] + 2*Liste[DT][2]
    Hersteller[DT] = Güte
    print(Hersteller)

MinWert = min(Hersteller.values())
MinHersteller = [k for k, v in Hersteller.items() if v==MinWert]
'''Wenn mehrere DTs den gleichen Wert haben, nimm den ersten'''
final = {MinHersteller[0]: MinWert}
print(final)




    # erg = minimize(f, someNumber, args=(a, b, c))
    # print(erg)