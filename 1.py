


data=[1,2,3,4,5]
output = [value* value for value in data]


print(output)

squere = lambda x: x*x

output=[squere(x) for x in data]
print(output)

print((lambda x:x*x)(x) for x in data)

score=[]

while 1:
    key = input("请输入成绩（a为结束）：")
    if key!="a":
        score.append(int(key))
    else:
        break
print(f"成绩为：{score}")

print()