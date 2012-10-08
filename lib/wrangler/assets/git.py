import tempfile
import os, shutil, subprocess
import copy


#@TODO: get cache path from other source?
class AssetCache(object):
    def __init__(self, dir_="/tmp/POC_cache"):
        self._cache_dir = dir_
        self._setup_cache_dir()

        self._registry = {}
        pass

    def _setup_cache_dir(self):
        if not os.path.isdir(self._cache_dir):
            os.mkdir(self._cache_dir)

    def __getitem__(self, key):
        return self._registry[key]

    def __setitem__(self, key, metadata):
        cache_path = os.path.join(self._cache_dir, key)
        shutil.copytree(metadata['path'], cache_path)
        metadata['cache_path'] = cache_path
        self._registry[key] = copy.deepcopy(metadata)

    def __del(self, key):
        metadata = self._registry[key]
        shutil.rmtree(metadata.get('cache_path'))
        del self._registry[key]

    def __contains__(self, key):
        return self._registry.has_key(key)

#@TODO: just another cache? DictDir?
#@TODO: get dir path from other source?
class AssetTargetDir(object):
    def __init__(self, dir_="/tmp/POC_Target"):
        self._target_dir = dir_
        self._setup_target_dir()
        self._registry = {}
        for key in os.listdir(self._target_dir):
            self._registry[item] = item

    def _setup_target_dir(self):
        if not os.path.isdir(self._target_dir):
            os.mkdir(self._target_dir)

    def __getitem__(self, key):
        return self._registry[key]

    def __contains__(self, key):
        return self._registry.has_key(key)

    def __setitem__(self, key, metadata):
        dir_path = os.path.join(self._target_dir, key)
        copy_kwargs = metadata.get("copy_kwargs", {})
        shutil.copytree(metadata['path'], dir_path, **copy_kwargs)
        metadata['dir_path'] = dir_path
        self._registry[key] = copy.deepcopy(metadata)

    def __del(self, key):
        metadata = self._registry[key]
        shutil.rmtree(metadata.get('dir_path'))
        del self._registry[key]

#@TODO: improve passing of cache, target_dir.
class GitAsset(object):

    def __init__(self, id=None, uri=None, refspec=None, path=None, include_dot_git=False,
                 cache=None, target_dir=None, **kwargs):
        self.id = id
        self.uri = uri
        self.refspec = refspec
        self.path = path
        self.include_dot_git = include_dot_git
        self.cache = cache
        self.target_dir = target_dir
        super(GitAsset, self).__init__(**kwargs)

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def clone_repo(self, dest=""):
        subprocess.call(['git', 'clone', self.uri, dest])

    def resolve(self):
        # If repo is not in cache, clone it and it to the cache.
        if self.id not in self.cache:
            tmp_dir = tempfile.mkdtemp()
            self.clone_repo(dest=tmp_dir)
            metadata = {'path': tmp_dir}
            self.cache[self.id] = metadata

        # Get the cache path.
        cache_path = self.cache[self.id]['cache_path']

        # If no refspec was given, pull the latest.
        if self.refspec is None:
            subprocess.call("cd %s; git checkout HEAD" % (cache_path) , shell=True)

        # Otherwise if there was a ref...
        else:
            # If we don't have the refspec locally, then fetch it.
            retcode = subprocess.call(
                ("cd %s; git rev-parse --verify -q %s") % (cache_path,
                                                           self.refspec), 
                shell=True
            )
            if retcode != 0:
                subprocess.call(
                    ("cd %s; git fetch %s %s") % (cache_path, self.uri,
                                                  self.refspec),
                    shell=True
                )

            # Checkout the rev.
            subprocess.call(
                ("cd %s; git checkout %s %s") % (cache_path, self.uri,
                                                 self.refspec),
                shell=True
            )

        # Setup options for adding to target dir.
        copy_kwargs = {}

        #@TODO: move copying logic into common place?
        # If there was a path, copy just that path to the target.
        if self.path:
            source_path = os.path.join(cache_path, copy_path)

        # Otherwise copy the whole repo.
        else:
            source_path = cache_path
            # Don't include .git folder if not specified.
            if not self.include_dot_git:
                copy_kwargs['ignore'] = shutil.ignore_patterns('.git')

        self.target_dir[self.id] = {
            'path': source_path,
            'copy_kwargs': copy_kwargs
        }
