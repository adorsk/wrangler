import unittest
from wrangler.assets import git
import shutil
import tempfile
import subprocess


class GitTest(unittest.TestCase):
    def setUp(self):
        self.repo1 = tempfile.mkdtemp()
        subprocess.call(['git', 'init', self.repo1])

    def tearDown(self):
        shutil.rmtree(self.repo1)

    def test_fetch(self):

        asset = git.GitAsset(id="fish", uri=self.repo1)
        asset.fetch()

if __name__ == '__main__':
    unittest.main()
