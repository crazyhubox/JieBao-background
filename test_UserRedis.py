from UserRedis.getUserFromRedis import UserInfoRedis


u_obj = UserInfoRedis()

# 20721681 Aa961028
# 18124274 Swsn990826
# 18121145 Fy20001003
# 15122557 SHENjian0512
# 18121142 Xiwanwan0615
# 18123467 Kpsj981002
# 18121121 a610bq9262C
# 20124323,As8122194
t_key_str=  'QXM4MTIyMTk0'
# t_key_str=  t_key.decode()
print(t_key_str)
pas = u_obj.ts_pw(t_key_str)
print(pas)