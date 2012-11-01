import os, shutil, subprocess
import copy


#@TODO: improve passing of cache, target_dir.
#@TODO: factor out common logic shared w/ git, other SCM assets.
class HgAsset(object):
    """ Mercurial Asset. """

    def __init__(self, id=None, source=None, refspec=None, path=None, 
                 include_dot_hg=False, cache_dir=None, 
                 target_dir=None, **kwargs):
        self.id = id
        self.source = source
        self.refspec = refspec
        self.path = path
        self.include_dot_hg = include_dot_hg
        self.cache_dir = cache_dir
        self.target_dir = target_dir

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def clone_repo(self, dest=""):
        cmd = "hg clone %s %s" % (self.source, dest)
        subprocess.call(cmd, shell=True)

    def resolve(self):
        # If already in the target, do nothing.
        target_path = os.path.join(self.target_dir, self.id)
        if os.path.exists(target_path):
            return

        # Get the cache path.
        cache_path = os.path.join(self.cache_dir, self.id)

        # If repo is not in cache, clone it and it to the cache.
        if not os.path.exists(cache_path):
            self.clone_repo(dest=cache_path)

        # If no refspec was given, checkout master branch and pull.
        if self.refspec is None:
            subprocess.call("cd %s; hg checkout master; hg pull" % (cache_path) , shell=True)

        # Otherwise if there was a ref...
        else:
            #@TODO!
            pass

        # Setup options for adding to target dir.
        copy_kwargs = {}

        #@TODO: move copying logic into common place?
        # If there was a path, copy just that path to the target.
        if self.path:
            source_path = os.path.join(cache_path, self.path)

        # Otherwise copy the whole repo.
        else:
            source_path = cache_path
            # Don't include .hg folder if not specified.
            if not self.include_dot_hg:
                copy_kwargs['ignore'] = shutil.ignore_patterns('.hg')
        if os.path.isdir(source_path):
            shutil.copytree(source_path, target_path, **copy_kwargs)
        else:
            shutil.copy(source_path, target_path)
