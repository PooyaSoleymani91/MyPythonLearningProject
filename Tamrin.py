import time

namee=input("Name?").lower()
x=time.time()
c={}
print("your name has:")
for n in namee:
    j=0
    if n==" ": continue
    if n in c:continue
    for i in namee:
        if n==i:
            j=j+1
    c[n]=j
for k in c:
    print(k + " " + str(c[k]))
print(time.time()-x)

y=time.time()
namee=namee.replace(" ","")
b=[]
for n in namee:
    if n not in b:
        print(f"your name has {namee.count(n)} {n}")
        b.append(n)
print(time.time()-y)