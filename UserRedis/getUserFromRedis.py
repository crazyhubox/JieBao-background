from redis import Redis
import base64




class BaseRedis:
    """Connect the Redis and """
    def __init__(self):
        Host = '49.235.241.94'
        self.rdb = Redis(host=Host, password='130298',
                         db=0, decode_responses=True)
        self.tempTables = 'temp_users'        
        self.pubTables = 'pub_users'
        self.finishTables = 'finished_users'

    def popUser(self):
        return self.rdb.spop(self.tempTables)

    def getTotalUsers(self):
        # users = self.rdb.smembers('users')
        users = self.rdb.smembers(self.pubTables)
        return users

    def addUser(self, userinfo: str):
        self.rdb.sadd(self.pubTables, userinfo)

    def removeErrorUser(self):
        """Remove the current userInfo."""
        print('[INFO]: Remove the ERROR userInfo. -->',self.currentUserInfo)
        # pub_users finished_users
        self.rdb.srem(self.pubTables,self.currentUserInfo)
        self.rdb.srem(self.finishTables,self.currentUserInfo)

    def recoverErroUer(self):
        self.rdb.sadd(self.tempTables, self.currentUserInfo)


    def saddUser(self,keyname:str,userinfo:str):
        self.rdb.sadd(keyname, userinfo)


class UserInfoRedis(BaseRedis):

    def __init__(self) -> None:
        super().__init__()
        self.currentUserInfo = ''

    def __initUserInfo(self):
        user_num = self.rdb.scard(self.tempTables)
        if user_num:
            print('No initialization required.')
            return

        users = self.getTotalUsers()
        # TODO 如果users有问题
        for each in users:
            print(each)
            self.rdb.sadd(self.tempTables, each)
        print(
            f'[INFO]: Read the user_info successfully! There are {user_num} users.')

    
    def ReadUserInfo(self):
        """This function is a generator. Whenever a user is returned, the temp_user's user_num will decline.
        """
        # 初始化用户列表
        self.__initUserInfo()
        user_num = self.rdb.scard(self.tempTables)
        # 依次pop每一个用户的信息
        for _ in range(user_num):
            user_info = self.popUser()
            # 添加到已完成表中
            self.saddUser(self.finishTables,user_info)
            self.currentUserInfo = user_info
            user_info = user_info.split(',')
            uid = user_info[0]
            password = user_info[1]
            password = self.ts_pw(password)
            yield uid, password
  
    
    def getNewUser(self):
        newUserInfo = self.rdb.sdiff(self.pubTables,self.finishTables)
        for each in newUserInfo:
            uid,password = self.cleanUserInfo(each)
            yield uid,password,each

    def cleanUserInfo(self,userInfo:str):
        user_info = userInfo
        user_info = user_info.split(',')
        uid = user_info[0]
        password = user_info[1]
        password = self.ts_pw(password)
        return uid ,password
        
    def ts_pw(self,pw:str):
        a = base64.b64decode(pw.encode())
        return a.decode()
    

if __name__ == "__main__":
    # print(ReadUserInfo())
    u_obj = UserInfoRedis()
    # u_obj.__initUserInfo()
    # 18121253,YnY381381
    # t_str ='WW5ZMzgxMzgx'
    # t_key = base64.b64encode(t_str.encode())
    
    # 20721681 Aa961028
    t_key_str=  'QWE5NjEwMjg=' 
    # t_key_str=  t_key.decode()
    print(t_key_str) 
    pas = u_obj.ts_pw(t_key_str)
    print(pas)
    # for each_u,each_p in u_obj.ReadUserInfo():
    #     print(each_u,each_p)

    # test_set = u_obj.getNewUser()
    # print(test_set)

    # for each in u_obj.getNewUser():
    #     i,p = u_obj.cleanUserInfo(each)
    #     print(i,p)
    
    
    # u_obj.currentUserInfo = '16123113,MTMwRTJkODk4'
    # u_obj.removeErrorUser()