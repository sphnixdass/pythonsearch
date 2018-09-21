import re

str = "hi \\dass"
print(re.search(r'\\da',str))

# f = "hat rat mat pat"
# regx = re.compile('rat')
# f2 = regx.sub("food",f)
# print(regx)
# print(f2)


# str = 'we need to inform him with the latest information'
#
# # temp = re.findall('e[ds]',str)
# temp = re.finditer('e[ds]',str)
# for i in temp:
#     print(i.match)


# for i in re.finditer("inform",str):
#     print(i.span())

# alltext = re.findall('inform','we need to inform him with the latest information')
#
# for x in alltext:
#     print(x)



# temptext = '''
# Janice is 22 and Theon is 33
# Gabriel is 44 and Joey is 21
# '''
#
# ages= re.findall(r'\d{1,3}',temptext)
# names = re.findall(r'[A-Z][a-z]*',temptext)
# ageDict = {}
# d = 0
#
# for eachitem in names:
#     print(eachitem )
#     ageDict[eachitem] = ages[d]
#     d+=1
#
# print(ageDict)
#regatag="<a.*?(.+?)</a>"


#patternatag=re.compile(regatag)
#titles=re.findall(patternatag,temptext)
#print(titles)
