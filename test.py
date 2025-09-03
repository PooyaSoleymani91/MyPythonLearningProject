txt= "Hello HOW Are you?"
# print(txt.capitalize().casefold().center(100))
# print(txt.count(" ")+1)
# print(txt)
# x=len(txt)
# print(x)
# newtext=""

# for i in range(0,len(txt)) :
#     if i%2 == 1:
#             newtext = newtext + txt[i].capitalize()
#     else:
#         newtext = newtext + txt[i].lower()
# print(newtext)
i=1
mylist=list()
testlist=["pp"]
ilist=[1]
for i in range(1,10) :
        ilist[0]=i
        mylist=mylist
        mylist.append("PP"+str(i))
print(mylist[0:-1])
for x in mylist:
        print(x)
j=2
j+=1
print(mylist)
mylist.insert(1,"ezafe shod")
print(mylist)
list1=["mansour","bat","pooya"]
list2=["bat","sol","marshal"]
print(list1)
print(list1.index("bat"))
list1.extend(list2)
print(list1)
list1.remove("bat")
print(list1)
list1.pop(1)
print(list1)
list1.pop()
print(list1)
list1.sort()
print(list1)
list1.sort(reverse=True)
print(list1)
list1.clear()
print(list1)

