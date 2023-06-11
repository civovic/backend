import os


class Env(object):

    @staticmethod
    def get(key, default=None):
        return os.environ.get(f'{key}', default)

    @staticmethod
    def bool(key, default=None):
        return Env.get(key, default) in ['1', 'true', True, 'True']

    @staticmethod
    def str(key, default=None):
        value = Env.get(key, default)
        return str(value) if value else default

    @staticmethod
    def int(key, default=None):
        value = Env.get(key, default)
        return int(value) if value else default
