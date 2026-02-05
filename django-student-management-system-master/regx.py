import re
mainstr=input("Enter your string:")
searchstr=input("Find you earch to search")
match=re.search(searchstr,mainstr,re.IGNORECASE)

#match=re.match(searchstr,mainstr)
if match!=None:
    print("match",match.start())

else:
    print("Not match")








'''matcher=re.finditer(searchstr,mainstr)
for m in matcher:
    print("Start index:",m.start())
    print("Group:",m.group())
    print("End:",m.end())
    
pattern=re.compile("Python") 
matcher=pattern.finditer("Python is easy to learn")
for m in matcher:
    print("Start index:",m.start())
    print("Group:",m.group())
    print("End:",m.end()) '''