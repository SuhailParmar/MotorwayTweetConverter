from os import getenv

api_base_url = getenv('API_BASE_URL', 'localhost')
api_post_endpoint = getenv('API_POST_ENDPOINT', 'api/events/')
api_port = getenv('API_PORT', 8000)

rabbit_host = getenv('MQ_HOST', 'localhost')
rabbit_port = getenv('MQ_PORT', 5672)
rabbit_source_queue = getenv('MQ_SOURCE_QUEUE', 'M6_Raw_Events')
rabbit_dlqueue = getenv('MQ_DL_QUEUE', 'M6_Dead_Letter')
rabbit_username = getenv('MQ_USERNAME', 'guest')
rabbit_password = getenv('MQ_PASSWORD', 'guest')
rabbit_exchange = getenv('MQ_EXCHANGE', 'MotorwayExchange')
rabbit_routing_key = getenv('MQ_ROUTING_KEY', 'M6_Enriched')
rabbit_dl_routing_key = getenv('MQ_DL_ROUTING_KEY', 'M6_DL')
rabbit_vhost = getenv('MQ_VHOST', 'motorway_vhost')

log_file = getenv('LOG_FILE', 'motorway_tweet_converter.log')