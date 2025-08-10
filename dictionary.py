test={
"name":"Pooya",
"Famil":"Soleymani",
"sen":33,
"name":"Pooyaaaaaaa" #in baraye ine ke neshoon bedim kilide tekrari nemigire va meghdare kilide akhar ro lahaz mikone
}

print(type(test))
print(test)
print(len(test))
x=test["name"]
print(x)
y=test.get("Famil")
print(y)
listkeys=test.keys()
print(listkeys)
listvalue=test.values()
print(listvalue)
itemmssss=test.items() #har item ro ba kilidesh va valuesh dakhele ye list gharar mide va hamashun ro tu ye tuple mizare
print(itemmssss)
ayavoojooddarad="name" in test #javab true ya false
print(ayavoojooddarad)

test["sen"]=34 #taghire value
print(test)
test["jensiyat"]="mard" #ezafe kardane yek kilide jadid va meghdar dadan be an
print(test)

test.update({"sen" : 35}) #raveshe digeye taghir
print(test)
test.update({"shoghl": "barname nevis" , "sen" :34}) #shoghl nabood va ezafe shod va sen ham taghir kard
print(test)
copiedtest=test.copy() #کپی کردن دیکشنری ها NOKTE MOHEM: Nemishe hamintori benevisim copiedtest=test chon ke taghir too harkoodoom az ina oonyeki ro ham avaz mikone

test.pop("jensiyat") #pak kardane yek kilid dar dictionary (hatman bayad kilid bedim)
print("copiedtest=")
print(copiedtest)
print("test=")
print(test)
test.popitem() #pak kardane akharin kilide vared shode (az pyton ver3.7 be bad intoriye)

print(test)
del test["Famil"] #pak kardane yek kilid ba raveshe digar nokte: age kilid nazarim masalan benevisim
#del test kolle test ro pak mikone engar aslan test nadarim
print(test)

#age bekhaym kolle dade haye dakhele test ro pak konim az clear estefade mikonim mesal:
test.clear()
print(test)

test=copiedtest.copy()

#تست کردن کپی کردن اشتباه یک دیکشنری
worngcopy=test

print("wrongcopy=")
print(worngcopy)
print("test=")
print(test)

worngcopy.pop("name")

print("wrongcopy=")
print(worngcopy)
print("test=")
print(test)

#didim ke ba taghire wrongcopy, test ham taghir mikone ke eshtebahe
#dorostesh ine
rightcopy=test.copy()
#ya
rightcopy=dict(test)

#nested dictionary ya dicitionary haye too dar too

nesteddic={
    "father": {"esm" : "Pooya","famil" :"Soleyamni"},
    "Mother":{"esm" : "Mahsa","famil" : "Soleymani"},
    "Son": {"esm" : "Taraz" , "famil" : "Soleymani"},
    "daughter": {"esm" : "Tiyanaz" , "famil" : "Soleymani"}
}

print(nesteddic["Son"]["esm"])

#ya

father={"esm" : "Pooya","famil" :"Soleyamni"}
Mother={"esm" : "Mahsa","famil" : "Soleymani"},
Son={"esm" : "Taraz" , "famil" : "Soleymani"},
daughter= {"esm" : "Tiyanaz" , "famil" : "Soleymani"}
nesteddic2={
    "father": father,
    "Mother":Mother,
    "Son": Son,
    "daughter": daughter
}


if "esm" in father:
    print("hast")
else:
    print("nist")