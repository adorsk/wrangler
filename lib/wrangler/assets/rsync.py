import os, shutil, subprocess
import copy


#@TODO: improve passing of cache, target_dir.
class RsyncAsset(object):

    def __init__(self, id=None, source=None, path=None, args=None,
                 cache_dir=None, target_dir=None, **kwargs):
        self.id = id
        self.source = source
        self.path = path
        self.args = args
        self.cache_dir = cache_dir
        self.target_dir = target_dir

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def resolve(self):
        # If already in the target, do nothing.
        target_path = os.path.join(self.target_dir, self.id)
        if os.path.exists(target_path):
            return

        # Get the cache path.
        cache_path = os.path.join(self.cache_dir, self.id)

        # Sync to the cache. 
        cmd = """
        rsync -aL %s %s/ %s/
        """ % (self.args, self.source, cache_path)
        subprocess.call(cmd, shell=True)

        #@TODO: move copying logic into common place?
        copy_kwargs = {}
        # If there was a path, copy just that path to the target.
        if self.path:
            source_path = os.path.join(cache_path, self.path)

        # Otherwise copy the whole repo.
        else:
            source_path = cache_path

        shutil.copytree(source_path, target_path, **copy_kwargs)
