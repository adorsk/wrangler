#!/usr/bin/env python

""" Main executable. """
import sys
import os
import shutil
from processor import Processor
import argparse
argparser = argparse.ArgumentParser(
    description='Manage assets.'
)
argparser.add_argument('action', help='Action to execute')
argparser.add_argument('-f', '--assetfile', type=str, default='AssetFile.py', 
                       help='AssetFile to use')
argparser.add_argument('-c', type=str, default='.wrangler.py', 
                       help='Config file to use')

class Wrangler(object):
    def __init__(self, asset_file=None, config={}):
        self.asset_file = asset_file
        self.config = config

    def init(self):
        """ Create the initial AssetFile. """
        if os.path.exists(self.asset_file):
            print >> sys.stderr, "Already initialized."
            return

        asset_file_tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                      'templates', 'AssetFile.py')
        shutil.copy(asset_file_tpl, self.asset_file)
        print >> sys.stderr, "Initialized with '%s'." % self.asset_file

    def clean(self):
        """ Clear out the target dir. """
        assets_data = self.read_asset_file()
        config = assets_data['config']
        for item in os.listdir(config['TARGET_DIR']):
            item_path = os.path.join(config['TARGET_DIR'], item)
            print >> sys.stderr, "removing '%s'..." % item_path
            shutil.rmtree(item_path)

    def install(self):
        """ Install assets in target dir. """
        assets_data = self.read_asset_file()
        config = assets_data['config']
        for dir_ in [config['CACHE_DIR'], config['TARGET_DIR']]:
            if not os.path.exists(dir_):
                os.mkdir(dir_)

        processor = Processor(
            cache_dir=config['CACHE_DIR'],
            target_dir=config['TARGET_DIR']
        )
        processor.resolve_asset_defs(assets_data['assets'])
        print >> sys.stderr, "Install finished."

    def read_asset_file(self):
        """ Read data from asset file. """
        assets_data = {}
        execfile(self.asset_file, assets_data)
        return assets_data

if __name__ == '__main__':
    args = argparser.parse_args()
    action = args.action
    wrangler = Wrangler(asset_file=args.assetfile)
    action_method = getattr(wrangler, action)
    action_method()
