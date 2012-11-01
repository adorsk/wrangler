import os, shutil, subprocess
import copy


#@TODO: improve passing of cache, target_dir.
class GitAsset(object):

    def __init__(self, id=None, source=None, refspec=None, path=None, 
                 include_dot_git=False, cache_dir=None, 
                 target_dir=None, **kwargs):
        self.id = id
        self.source = source
        self.refspec = refspec
        self.path = path
        self.include_dot_git = include_dot_git
        self.cache_dir = cache_dir
        self.target_dir = target_dir

    def __str__(self):
        return "%s %s" % (object.__str__(self), self.__dict__)

    def clone_repo(self, dest=""):
        cmd = "git clone %s %s" % (self.source, dest)
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
            subprocess.call("cd %s; git checkout master; git pull" % (cache_path) , shell=True)

        # Otherwise if there was a ref...
        else:
            # If we don't have the refspec locally, then do a fetch.
            retcode = subprocess.call(
                ("cd %s; git rev-parse --verify -q %s") % (cache_path,
                                                           self.refspec), 
                shell=True
            )
            if retcode != 0:
                subprocess.call(
                    ("cd %s; git fetch") % (cache_path),
                    shell=True
                )

            # Checkout the rev.
            subprocess.call(
                ("cd %s; git checkout %s") % (cache_path, self.refspec),
                shell=True
            )

        # Setup options for adding to target dir.
        copy_kwargs = {}

        #@TODO: move copying logic into common place?
        # If there was a path, copy just that path to the target.
        if self.path:
            source_path = os.path.join(cache_path, self.path)

        # Otherwise copy the whole repo.
        else:
            source_path = cache_path
            # Don't include .git folder if not specified.
            if not self.include_dot_git:
                copy_kwargs['ignore'] = shutil.ignore_patterns('.git')

        shutil.copytree(source_path, target_path, **copy_kwargs)
