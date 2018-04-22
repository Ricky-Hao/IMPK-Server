import redis
from Server.util import logger

log = logger.getChild('Redis')

redis_pool = redis.ConnectionPool(host='rickyhao.com', port=6379)

def subscribe(channel):
    redis_connection = redis.StrictRedis(connection_pool=redis_pool)
    pubsub = redis_connection.pubsub()
    pubsub.subscribe(channel)
    log.debug('Subscribe channel: {0}'.format(channel))
    return pubsub

def send(channel, message):
    log.debug('Channel: {0}, Message: {1}'.format(channel, message))
    redis_connection = redis.StrictRedis(connection_pool=redis_pool)
    return redis_connection.publish(channel, message)
