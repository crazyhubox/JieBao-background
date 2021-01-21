from .Base import BaseRedis

import base64

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
    for a,b,c in u_obj.getNewUser():
        print(a)
    t_key_str=  ''
    print(t_key_str)
    pas = u_obj.ts_pw(t_key_str)
    print(pas)