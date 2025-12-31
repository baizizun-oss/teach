#在下划线①②③处将代码补充完成，并删除序号
def isP(x):				#自定义函数，判断x是否为素数
    flag=True
    for i in ①(2,int(x**0.5)+1):
        if ②==0:
            flag=False
            break
    return flag


n=int(input("属于一个不小于6的偶数："))
for i in range(3,n//2+1):
    if isP(i) and isP(n-i):
        print(n,"=",i,"+",③)

