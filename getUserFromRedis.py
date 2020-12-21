from redis import Redis
Host = '49.235.241.94'
rdb = Redis(host=Host,port=6379,password='130298',db=0,decode_responses=True)

def InitUserTable():
    users = [
        '16123113,130E2d898',
        '16121337,1997913Was',
        '16120910,LYing924',
        '16123050,HUAhua102'
    ]

    for each_user in users:
        res = rdb.sadd('users',each_user)
        print(res)

def ReadUserInfo():
    user_dict = {}
    users = rdb.smembers('users')
    user_num = rdb.scard('users')
    for user_info in users:
        user_info = user_info.split(',')
        uid = user_info[0]
        password = user_info[1]
        user_dict[uid] = password    
    print(f'[INFO]: Read the user_info successfully! There are {user_num} users.')
    return user_dict

if __name__ == "__main__":
    print(ReadUserInfo())