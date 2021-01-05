from redis import Redis

# rdb = Redis(host=Host,password='130298',db=0,decode_responses=True)

# def InitUserTable():
#     users = [
#         'id,password',
#     ]

#     for each_user in users:
#         res = rdb.sadd('users',each_user)
#         print(res)

# def ReadUserInfo():
#     user_dict = {}
#     users = rdb.smembers('users')
#     user_num = rdb.scard('users')
#     for user_info in users:
#         user_info = user_info.split(',')
#         uid = user_info[0]
#         password = user_info[1]
#         user_dict[uid] = password
#     print(f'[INFO]: Read the user_info successfully! There are {user_num} users.')
#     return user_dict


class UserInfoRedis:

    def __init__(self) -> None:
        super().__init__()
        Host = '49.235.241.94'
        self.rdb = Redis(host=Host, password='130298',
                         db=0, decode_responses=True)
        self.tempTables = 'temp_users'
        self.currentUserInfo = ''
        self.pubTables = 'pub_users'

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

    def popUser(self):
        """
        docstring
        """
        return self.rdb.spop(self.tempTables)

    # def ReadUserInfo(self):
    #     user_dict = {}
    #     users = self.getTotalUsers()

    #     user_num = self.rdb.scard('users')
    #     for user_info in users:
    #         user_info = user_info.split(',')
    #         uid = user_info[0]
    #         password = user_info[1]
    #         user_dict[uid] = password
    #     print(f'[INFO]: Read the user_info successfully! There are {user_num} users.')
    #     return user_dict

    def ReadUserInfo(self):
        """This function is a generator. Whenever a user is returned, the temp_user's user_num will decline.
        """
        # 初始化用户列表
        self.__initUserInfo()
        user_num = self.rdb.scard(self.tempTables)
        # 依次pop每一个用户的信息
        for _ in range(user_num):
            user_info = self.popUser()
            self.currentUserInfo = user_info
            user_info = user_info.split(',')
            uid = user_info[0]
            password = user_info[1]
            yield uid, password

    def recoverErroUer(self):
        self.rdb.sadd(self.tempTables, self.currentUserInfo)

    def getTotalUsers(self):
        users = self.rdb.smembers('users')
        # users = self.rdb.smembers(self.pubTables)
        return users

    def addUser(self, userinfo: str):
        self.rdb.sadd(self.pubTables, userinfo)
        
        
if __name__ == "__main__":
    # print(ReadUserInfo())
    u_obj = UserInfoRedis()
    u_obj.__initUserInfo()
