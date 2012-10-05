class BaseAsset(object):

    filesystem_path = None

    def __init__(self, id=None):
        self.id = id

    def resolve(self, *args, **kwargs):
        pass

    def fetch(self, *args, **kwargs):
        pass

    def process(self, *args, **kwargs):
        pass


class CacheableAsset(BaseAsset):
    cacheable = True

    def __init__(self, cache_ctx=None, **kwargs):
        super(CacheableAsset, self).__init__(**kwargs)
        self.cache_ctx = cache_ctx

    def is_cached(self, *args, **kwargs):
        pass

    def cache(self, *args, **kwargs):
        pass

    def resolve(self, *args, **kwargs):
        if not self.is_cached:
            self.fetch()
            self.cache()
        self.process()
