from celery import Celery
import os
import redis
from flask_bootstrap import Bootstrap

bootstrap = Bootstrap()

celery = Celery(__name__)


class Flask_env:
    def __init__(self, app=None):
        self.app = app
        if app:
            self.init_app(app)

    def init_app(self, app):
        if self.app is None:
            self.app = app
        env_file = os.path.join(os.getcwd(), '.env')
        if not env_file:
            raise FileNotFoundError('.env file not found')
        self.__import_vars(env_file)

    def __import_vars(self, env_file):
        # read file
        # parse the str
        # write in config
        print('load .env file from parent dir')
        with open(env_file) as opener:
            lines = opener.readlines()
            for line in lines:
                line = line.replace('\'', '')
                line = line.strip('\n')
                # export
                if not line:
                    continue
                if line.split(' ')[0] is 'export':
                    line = line.split(' ')[1]
                config_list = line.split('=')
                key, value = config_list[0], config_list[1]
                if self.app.config.get(key):
                    print(
                        'overwrite an exist key : {} {} ---> {}'.format(
                            key, self.app.config[key], value
                        )
                    )
                if value.isdigit():
                    value = int(value)
                self.app.config[key] = value


flask_env = Flask_env()


class RedisCache:
    def __init__(self, ns='REDIS_'):
        self.ns = ns
        self.client = None

    def init_app(self, app):
        # 找到redis配置文件，加载redis配置
        opts = app.config.get_namespace(self.ns)
        # 生成redis客户端
        self._pool = redis.ConnectionPool(**opts)
        self._client = redis.StrictRedis(connection_pool=self._pool)

    def __getattr__(self, name):
        return getattr(self._client, name)


redis_cache = RedisCache()
