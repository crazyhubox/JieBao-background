# 捷报项目总结

![avatar](https://img.shields.io/badge/Redis-v6.0.9-red)
![avatar](https://img.shields.io/badge/aiohttp-v3.7.2-blue)
![avatar](https://img.shields.io/badge/Status-End-brightgreen)

上大自2020秋季返校后, 需要师生填写每日两报, 此项目目标数解决广大同学之痛点, 解放双手. 也当做是一次项目的练手, 在此期间得到了各个学院的同学的一些鼓励和支持, 谢谢大家, 现在正式开放整个后台报送逻辑的源码.

## 项目结构

``` 

├── ErroHandler
│   └── merry.py                   异常处理装饰器类
│
├── Launcher
│   ├── Launcher.py                启动逻辑对低层方法的封装
│   └── Launcher.pyi
│
├── Notification                   错误时发送邮件               
│   └── send_email.py
│
├── Proxy                          使用代理
│   └── proxy.py
│
├── Reporter                       填报逻辑的封装
│   └── reporter.py
│
├── Requets                        低层请求和登录api的封装
│   ├── Login.py
│   ├── PostRequest.py
│   └── tempTest.py
│
├── UserRedis                      与redis的交互逻辑
│   ├── Base.py
│   └── getUserFromRedis.py
│
├── file.log                       报送日志
├── handleErro.py                  出现错误时的处理程序
├── main.py                        主程序
├── reademe.md
├── testNew.py                     用于临时测试一些功能的程序
└── vacation_self.py
```

## 主程序部分

redis数据, 登录器, 请求器, 报送器各个模块分离, 最后将它们传递给启动器由启动器去组织它们的逻辑, 这样实现易于拓展

比如如果不想使用redis实现, 想使用mongoDb的话, 只要实现相同的接口, 系统就可以正常运行

``` python
def main():
    accounts = UserInfoRedis()      #用户
    loginer = Login(...,...)        #没有代理的登录
    # loginer = ProxyLogin(...,...) #有代理的登录
    # loginer.setProxies(loginer.headers.proxies()) #代理登录器提供设置代理的接口
    req_obj = PostRequest()         #负责发送请求的对象
    reporter = AsyncReporter()      #负责报送逻辑的对象
    
    #启动器对象, 实现当日定时轮刷报送(遍历每个用户), 实现新用户前30天刷报等逻辑
    launch = Actuator(accounts=accounts,loginer=loginer,requester=req_obj,reporter=reporter)
    launch.schedule() #程序启动

    # Test  
    launch.NewUserTotal() #新用户刷报过去30天  
    launch.Sun_Moon(0)    #早报或者晚报
    launch.userPoll()
    test_u = ''
    test_p = ''
    launch.dayReport(test_u,test_p) #早报和晚报
    launch.userPoll(test_u,test_p,'2020-12-07') #遍历这个日期的所有用户的当天报送
```

## 异常处理部分

使得冗杂的异常处理, 和真是业务端饿逻辑分离开来. 在此要感谢miguelgrinberg的merry这个库, 在此基础我增加了对类方法的支持, 也使得merry有了继承的特性

``` 
├── ErroHandler
│   └── merry.py  
```

[merry源仓库地址](https://github.com/miguelgrinberg/merry)

``` python
class Actuator(Launcher):
    def __init__(self, accounts, loginer, requester, reporter):
        super().__init__(accounts, loginer, requester, reporter)

    # 异常处理的部分
    @ERRORHANDLER._try
    def selectReport(self, user, passw, flag):
        return super().selectReport(user, passw, flag) #被异常处理的函数
    
    @ERRORHANDLER._except(ValueError)
    def handleValueError(self,e):
        if e.args[0] == '[ERROR]: UserInfo ERROR.':
            self.accounts.removeErrorUser()

    @ERRORHANDLER._except(KeyboardInterrupt)
    def handleKeyboardInterrupt(self,k):
        print(k.args)
        self.accounts.recoverErroUer()
        import os
        os._exit(0)#解释器直接退出

    @ERRORHANDLER._except(Exception)
    def handleException(self,e):
        print(e.args)
        self.accounts.recoverErroUer()
            
    # 业务逻辑的部分
    def Sun_Moon(self, flag):
        """Complete the morning and evening reports of all users."""
        for user, passw in self.accounts.ReadUserInfo():
            print('[INFO]:', user)
            self.selectReport(user, passw, flag) #被异常处理的函数
            print('=' * 100)
            sleep(10)
        print('[Finished]:', datetime.now())
```

## 登录判断
里面封装的直接api登录判断, 从决定做公共服务开始就决定一定分析出上大登录的接口,这样才能在秒级返回登录判断

其实考虑到可能同一时间很多用于在登录的情况, 这里有应该使用async并发, 但是登录api对访问IP有限制

局限于没有稳定的代理, 且我们(穷学生)免费提供的服务, 所以没有这么去实现, 这也是后期困扰我们的一大问题, 因为很可能被恶意爬虫, 直接把这个api爬ban掉了

防范的措施其实就是接口api的保护, 我们分析和定义了一些规则, 使得一些异常的post数据无法访问到api, 但是这个规则用户是不知道的(我个人感觉类似软件实现的防火墙,在另一台服务器上, 异常的数据都是不会到达这个api的), 所以还比较有效的
``` python
├── Requets                        
    ├── Login.py
```

``` python
def __login(self):
    """The concrete implementation of logining process. 
    """
    response = self.loginAPI()
    r_lsit = response.history
    # for each in r_lsit:
        # print(each.headers)
    if not self.__checkAPI(r_lsit):
        raise ValueError('[ERROR]: UserInfo ERROR.')
```

## Async异步报送

不得不称赞asyncio在处理io请求时候的性能十分卓越, 真正实现了毙30天报送于一秒

``` python
  async with session.post(url='https://selfreport.shu.edu.cn/XueSFX/HalfdayReport.aspx', headers=headers ,params=params, data=data,proxy=self.proxy) as response:
            html = await response.text()
            status_code = response.status  
            print('Referer:', headers['Referer'], end=f'[{status_code}]')
            res = self.res_find.search(html)
            if res:
                print(res[1])
            else:
                raise HTTPError('AsyncPost Error.')

```

## 邮件提醒

错误时发送邮件并追踪错误

``` python
if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        exc_type, exc_value, exc_traceback_obj = sys.exc_info()
        traceback.print_tb(exc_traceback_obj)
        res:list = traceback.format_tb(exc_traceback_obj)
        res.append(type(e).__name__)
        if len(e.args):
            res.append(e.args[0])
        from Notification.send_email import send_erro
        send_erro(res)
        print('='*100)
        print(e.args)
```

## Redis
使用redis是为了速度和方便分布式拓展, 因为面向的人群并不庞大, 且redis的api简单易用, 所以使用redis做持久化存储, 以及直接使用集合运算得到新用户
```python
def getNewUser(self):
    newUserInfo = self.rdb.sdiff(self.pubTables,self.finishTables)
    for each in newUserInfo:
        uid,password = self.cleanUserInfo(each)
        yield uid,password,each
```

# 总结

捷报项目推出以来在短暂的一个多星期以内就收获了来自各个学院500多哥同学的使用, 谢谢大家的支持. 在这过程当中我们也意识到自己**写着玩**和真的**做服务**是完全不同的两回事,期间大量的时间其实是在修复服务起初我们对于网站安全的忽略所造成的问题, 期间也很感谢李瑞轩学长和蔡盛梁两位学长为我们网站所做的压力测试, 让我们意识到了网站安全建设的重要性, 也让我们明白要做好一个服务我们还有很长的一段路要走.