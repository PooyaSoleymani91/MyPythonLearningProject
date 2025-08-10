tuple1=("ali",110,True,"123",5.5)

tuple2=("pooya","soleymani")

tuple3=("test 1 itemi",)

tuple1=tuple1+tuple2 #test taghire tuple

print(tuple1)

new_list=list(tuple1)

new_list.append("ezafe")
new_list.append("ezafe")

tuple1=tuple(new_list) #test taghire tuple
print(new_list)
print(tuple1)