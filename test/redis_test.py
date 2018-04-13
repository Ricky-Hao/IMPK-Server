import redis

rc = redis.Redis('rickyhao.com')

if __name__ == '__main__':
    while True:
        data = input('Data: ')
        print(rc.publish('123', data))