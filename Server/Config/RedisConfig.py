from redis import StrictRedis

redis = StrictRedis(host='192.168.191.137', port=6379, db=1)
print("Redis 连接成功！")