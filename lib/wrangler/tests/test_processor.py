import unittest
import tempfile
import os
import shutil
import subprocess
from wrangler.processor import Processor


class ProcessorTest(unittest.TestCase):

    def setUp(self):
        self.dirs = {}
        for dir_type in ['repos', 'cache', 'target']:
            self.dirs[dir_type] = tempfile.mkdtemp(prefix="PT.%s." % dir_type)

        self.asset_defs = {}
        for i in range(3):
            asset_id = 'asset_%s' % i
            repo_path = os.path.join(self.dirs['repos'], asset_id) 
            self.create_repo(asset_id, repo_path)
            self.asset_defs[asset_id] =  {
                'type': 'git',
                'uri': repo_path,
            }

    def create_repo(self, repo_path):
        parent_dir, basepath = os.path.split(repo_path)
        cmd = '''
        cd %s;
        mkdir %s;
        cd %s;
        git init;
        touch foo;
        git add .;
        git commit -am "initialized";
        '''
        subprocess.call(cmd, shell=True)


    def tearDown(self):
        for dir_ in [self.repos_dir, self.cache_dir, self.target_dir]:
            shutil.rmtree(dir_)

    def test_resolve_asset_defs(self):
        processor = Processor(
            cache_dir=self.dirs['cache'],
            target_dir=self.dirs['target']
        )
        processor.resolve_asset_defs(self.asset_defs)

