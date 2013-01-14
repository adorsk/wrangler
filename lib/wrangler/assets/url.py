import os, shutil, subprocess
import copy
import urllib2
import tempfile


#@TODO: improve passing of cache, target_dir.
class UrlAsset(object):

    def __init__(self, id=None, source=None, cache_dir=None, 
                 target_dir=None, unzip=False, untar=False, path=None, **kwargs):
        self.id = id
        self.source = source
        self.cache_dir = cache_dir
        self.target_dir = target_dir
        self.unzip = unzip
        self.untar = untar
        self.path = path

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

        # If unzip is true, unzip to temp dir.
        # @TODO: put this in a common place.
        if self.unzip:
            tmpdir = tempfile.mkdtemp()
            unzip_cmd = "unzip -d %s %s" % (tmpdir, cache_path)
            subprocess.call(unzip_cmd, shell=True)
            if self.path:
                source_path = os.path.join(tmpdir, self.path)
            else:
                source_path = tmpdir

        elif self.untar:
            tmpdir = tempfile.mkdtemp()
            cmd = "tar -xzf %s -C %s" % (cache_path, tmpdir)
            subprocess.call(cmd, shell=True)
            if self.path:
                source_path = os.path.join(tmpdir, self.path)
            else:
                source_path = tmpdir
        else:
            source_path = cache_path

        #@TODO: move copying logic into common place?
        # If there was a path, copy just that path to the target.
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path)
        else:
            shutil.copy(source_path, target_path)
