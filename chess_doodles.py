
list2 = [4, 5, 6]
list3 = [1, 2, 3]
dic1 = {'a':1, 'b':2}
dic2 = {}
for i in range(2):
    dic2[list(dic1.keys())[i]] = list(dic1.values())[i]

del dic2['a']
print(dic2)
print(dic1)