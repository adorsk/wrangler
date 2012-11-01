import os, shutil, subprocess
import copy
import urllib2


#@TODO: improve passing of cache, target_dir.
class UrlAsset(object):

    def __init__(self, id=None, source=None, cache_dir=None, 
                 target_dir=None, **kwargs):
        self.id = id
        self.source = source
        self.cache_dir = cache_dir
        self.target_dir = target_dir

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def fetch(self, dest=""):
        target_file = open(dest, "wb")
        source_stream = urllib2.urlopen(self.source)
        target_file.write(source_stream.read())
        source_stream.close()
        target_file.close()

    def resolve(self):
        # If already in the target, do nothing.
        target_path = os.path.join(self.target_dir, self.id)
        if os.path.exists(target_path):
            return

        # Get the cache path.
        cache_path = os.path.join(self.cache_dir, self.id)

        # If not in the cache, fetch it.
        if not os.path.exists(cache_path):
            self.fetch(dest=cache_path)

        # Copy from the cache to the target.
        shutil.copy(cache_path, target_path)
