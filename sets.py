myset={'1','2','3','4','5','6'}
mysetnum={1,2,3,4,5,6}
myset.pop()
mysetnum.pop()
print(myset)
print(mysetnum)
myset.pop()
mysetnum.pop()
print(myset)
print(mysetnum)
myset.pop()
mysetnum.pop()
print(myset)
print(mysetnum)
myset.pop()
mysetnum.pop()
print(myset)
print(mysetnum)
myset.pop()
mysetnum.pop()
print(myset)
print(mysetnum)

#set ha tartib nadarand va tekrari nadarand 
#----
#bardasht shakhsi: shabihe majmue haye riyazi hastand ghabeliyate eshterak va ejtema va... darand

myset1={'salam','khubi','pooya'}
myset2={'che khabar','salam','ghorboonet','pooya'}

myset3=myset1.intersection(myset2) #eshterak
print(myset3)

myset3=myset1 & myset2 #eshterak
print(myset3)

myset3=myset1.union(myset2) #ejtema
print(myset3)

myset3=myset1 | myset2 #ejtema
print(myset3)

myset3=myset1.difference(myset2) #ekhtelaf
print(myset3)