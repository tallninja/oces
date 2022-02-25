import aioredis


class Cache:
    def __init__(self, url):
        self.url = url

    def create_client(self):
        return aioredis.from_url(self.url)
