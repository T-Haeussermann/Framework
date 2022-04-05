from Class_DT import Asset_Digital_Twin, Product_Demand_Digital_Twin
import time

testA = Asset_Digital_Twin("Name", "MeinPT", "ADT", "fräsen", "10h", "ausgelastet")
testB = Product_Demand_Digital_Twin("Name", "MeinPT", "PDDT", "20er Loch", "heute")
print(testA.capacity)
print(vars(testB))


while True:
    print("ich empfange die daten")
    time.sleep(5.5)
    print("ich speichere die daten ab")
    time.sleep(5.5)
    print("ich publishe die daten an den broker 2")
    time.sleep(5.5)