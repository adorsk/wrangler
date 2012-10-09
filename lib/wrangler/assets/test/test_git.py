import unittest
from wrangler.assets import git
import shutil
import tempfile
import subprocess
import os


class GitTest(unittest.TestCase):

    def setUp(self):
        self.repo1 = tempfile.mkdtemp()
        subprocess.call("""
                        cd %s; 
                        git init; 
                        touch foo; 
                        git add .; 
                        git commit -m "initialized";
                        git checkout -b "cow";
                        touch cowfile;
                        git add .;
                        git commit -m "added cowfile";
                        git checkout master;
                        """ % self.repo1, 
                        shell=True
                       )

    def tearDown(self):
        shutil.rmtree(self.repo1)

    def test_fetch(self):

        cache_dir = tempfile.mkdtemp(prefix="POC_CACHE.")
        cache = git.AssetCache(dir_=cache_dir)
        target_dir = tempfile.mkdtemp(prefix="POC_TARGET.")
        target = git.AssetTargetDir(dir_=target_dir)

        asset = git.GitAsset(id="fish", uri=self.repo1, refspec='cow', path=None, 
                             include_dot_git=False, cache=cache,
                             target_dir=target)
        asset.resolve()
        print "tdir: ", [p for p in os.walk(target_dir)]

        shutil.rmtree(cache_dir)
        shutil.rmtree(target_dir)

if __name__ == '__main__':
    unittest.main()
