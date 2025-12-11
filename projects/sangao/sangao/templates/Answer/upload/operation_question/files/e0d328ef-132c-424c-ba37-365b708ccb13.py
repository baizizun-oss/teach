dl=float(input("请输入用电量："))
if dl<=100:
    jg=dl*0.56
    print("用电价格为：",jg)
elif dl<=200:
    jg=dl*(0.56+0.09)
    print("用电价格为：",jg)
elif dl<=300:
    jg=dl*(0.56+0.09)
    print("用电价格为：",jg)
else:
    jg=dl*(0.56+0.27)
    print("用电价格为：",jg)
