#for mesle baghiye zaban haye barname nevisi nist karbordesh intoriye ke har list , tupl , set , string va... bashan be ezaye har item daroone anha halghe tekrar mishe

#mesale string:

a="pooya"

for item in a:
    print(item)
print('-------')
#mesal haye digar:
b=['salam','khoobi','pooya','123','test']
for item in b:
    print(item)
print('-------')
for item in b:
    if item=="123":
        break #dastoore khorooj az halghe
    print(item)
print('-------')
for item in b:
    if item=="123":
        continue #dastoore anjam nadadane dastoorate badi va raftan be iteme badi for
    print(item)
print('-------')


#hala age bekhaym mesle baghiye zaban ha az for estefade konim mitoonim az tabee range estefade konim

for i in range(10): #range az sefr shoroo mikone va hamchenin 10 ro ham shamel nemishe
    print(i)
print("-------")
#mesal digar:
for i in range(10):
    if i%2==1:
        print(i)
print("-------")

#taiine mahdoode:
for i in range(3,11): #deghat konim: 11 ro shamel nemishe va ta 10 mire
    print(i)
print("-------")

#taiin hamhaye for:
for i in range(0,10,2): #goftam gamhaye dotaii bere
    print(i)
print("-------")
for i in range(0,10,3): #goftam gamhaye setayi bere
    print(i)
print("-------")

#estefade az esle dar for: bad az tamam shodane for else ro anjam mide (karbordesh kame)

for i in range(10):
    print(i)
else:
    print("finished")
print("-------")


#halghe haye too dar too (nested for):

for item in b:
    print(item+":")
    for itemm in item:
        print(itemm)
print("-------")

color=["Ghermez","Abi","Sabz","Zard","Soorati","Narenji"]
mive=["Sib","Golabi","Porteghal","hendoone"]

for m in mive:
    for c in color:
        print(m+" "+c)
print("-------")