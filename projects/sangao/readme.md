1.Python中并不支持++，只能用a+=1这样的形式来表示
2.lambda 是一个隐式函数名，相当于define。比如lambda x:x+1,这就相当于是建立了一个如下的函数
Def y(x):
Return x+1
区别在于简单，另一个是可以叠加在其他表达式中。P
比如sorted()是一个排序函数，可以对元组列表字典甚至字符串进行排序（不论哪种都是返回列表），里面有三个参数，比如

a = {{“name”:”zhangsan”,”age”:15},{“name”:”lisi”,”age”:17}}
sorted(a.items(),lambda x:x[1]["age"])#表示按照年龄排序
就是lambda函数嵌入到sorted()来使用的。


10.20
在试题模块增加了试题的来源字段（比如这道题是2024年真题），并增加了试题Model。

10.24
import a.py时只能导入a.py中的类，最好是一个类一个类的写。比如 from a import b,c,d(b,c,d为a的类)
sqlite中文本类型的字段值NULL和""还不一样，NULL表示未被设置，""表示已经设置但是空，由于NULL不符合我的预期认知，所有以后都设置为"",使用update xxx set a="" where a is NULL对其进行转换