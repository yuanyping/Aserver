def outer(func):
	def inner():
		print("认证成功！")
		result = func()		#这里就相当于是把原始的f1 进行执行
		print("日志添加成功")
		return result			#返回f1函数体，这是必须执行的
	return inner				#返回inner 函数体，inner就已经包涵了f1的函数体
@outer
def f1():
    print("业务部门1数据接口......")
    a=2
    return a


f1()