from .base import CacheableAsset
import tempfile
import os, shutil, subprocess


class GitAsset(CacheableAsset):

    def __init__(self, uri=None, ref=None, sha=None, path=None, **kwargs):
        self.uri = uri
        self.ref = ref
        self.sha = sha
        self.path = path
        super(GitAsset, self).__init__(**kwargs)

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def fetch(self, *args, **kwargs):
        """ Checkout repo to cache. """
        tmpdir = tempfile.mkdtemp()
        target_path = os.path.join(tmpdir, self.id)
        subprocess.call(['git', 'clone', self.uri, target_path])
        shutil.rmtree(tmpdir)
        

    def is_cached(self, *args, **kwargs):
        # Look in cache for repo.
        # If cached repo head matches given spec, return true.
        return False
