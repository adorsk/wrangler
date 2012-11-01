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
argparser.add_argument('-t', '--targetdir', type=str, 
                       help='Target dir to put assets into.')

class Wrangler(object):
    def __init__(self, asset_file=None, config={}):
        self.asset_file = asset_file
        assets_data = self.read_asset_file()

        # Update config w/ options from command line.
        self.config = {}
        self.config.update(assets_data.get('config', {}))
        self.config.update(config)

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
        for item in os.listdir(self.config['TARGET_DIR']):
            item_path = os.path.join(self.config['TARGET_DIR'], item)
            print >> sys.stderr, "removing '%s'..." % item_path
            shutil.rmtree(item_path)

    def install(self):
        """ Install assets in target dir. """
        assets_data = self.read_asset_file()
        for dir_ in [self.config['CACHE_DIR'], self.config['TARGET_DIR']]:
            if not os.path.exists(dir_):
                os.makedirs(dir_)

        processor = Processor(
            cache_dir=self.config['CACHE_DIR'],
            target_dir=self.config['TARGET_DIR']
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
    config = {}
    action = args.action

    args_config_attrs = {
        'targetdir': 'TARGET_DIR'
    }
    for arg, config_attr in args_config_attrs.items():
        value = getattr(args, arg, None)
        if value is not None:
            config[config_attr] = value

    wrangler = Wrangler(asset_file=args.assetfile, config=config)
    action_method = getattr(wrangler, action)
    action_method()
