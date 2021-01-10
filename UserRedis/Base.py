from redis import Redis

class RedisServer:
    def __init__(self) -> None:
        Host = '49.235.241.94'
        self.rdb = Redis(host=Host, password='130298',
                         db=0, decode_responses=True)

class BaseRedis(RedisServer):
    """Connect the Redis and """
    def __init__(self):
        super(BaseRedis, self).__init__()
        self.tempTables = 'temp_users'        
        self.pubTables = 'pub_users'
        self.finishTables = 'finished_users'
        self.currentUserInfo = ''

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
        
        
        
if __name__ == '__main__':
    pass
