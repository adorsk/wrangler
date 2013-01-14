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
argparser.add_argument('targets', help=(
    'Specific assets to act. If left empty', 'acts on all assets'),
    nargs='*')

argparser.add_argument('-f', '--assetfile', type=str, default='AssetFile.py', 
                       help='AssetFile to use')
argparser.add_argument('-c', type=str, default='.wrangler.py', 
                       help='Config file to use')
argparser.add_argument('-t', '--targetdir', type=str, 
                       help='Target dir to put assets into.')

def initialize_asset_file(asset_file):
    if os.path.exists(asset_file):
        print >> sys.stderr, "Already initialized."
        return

    asset_file_tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'templates', 'AssetFile.py')
    shutil.copy(asset_file_tpl, asset_file)
    print >> sys.stderr, "Initialized with '%s'." % asset_file

class Wrangler(object):
    def __init__(self, asset_file=None, config={}, targets=None):
        self.assets_data = self.read_asset_file(asset_file)

        # Update config w/ options from command line.
        self.config = {}
        self.config.update(self.assets_data.get('config', {}))
        self.config.update(config)

        self.setup_dirs()
        self.target_defs = self.get_target_defs(targets)

    def setup_dirs(self):
        for dir_ in [self.config['CACHE_DIR'], self.config['TARGET_DIR']]:
            if not os.path.exists(dir_):
                os.makedirs(dir_)

    def get_target_defs(self, targets):
        if targets:
            return dict(
                [(k, v) for k, v in self.assets_data['assets'].iteritems() 
                 if k in targets])
        else:
            return self.assets_data['assets']

    def clean(self):
        """ Clear out assets in the target dir. """
        for asset_id in self.target_defs.keys():
            self.remove_asset(asset_id)

    def remove_asset(self, asset_id):
        target_path = os.path.join(self.config['TARGET_DIR'], asset_id)
        print >> sys.stderr, "removing '%s'..." % target_path
        if os.path.exists(target_path):
            if os.path.isdir(target_path):
                shutil.rmtree(target_path)
            else:
                os.remove(target_path)

    def install(self):
        """ Install assets in target dir. """
        processor = Processor(
            cache_dir=self.config['CACHE_DIR'],
            target_dir=self.config['TARGET_DIR']
        )
        processor.resolve_asset_defs(self.target_defs)
        print >> sys.stderr, "Install finished."

    def update(self):
        """ Update assets. Removes and then re-installs assets. """
        processor = Processor(
            cache_dir=self.config['CACHE_DIR'],
            target_dir=self.config['TARGET_DIR']
        )
        print self.target_defs
        for asset_id, asset_def in self.target_defs.items():
            self.remove_asset(asset_id)
            processor.resolve_asset_defs({asset_id: asset_def})
        print >> sys.stderr, "Update finished."

    def read_asset_file(self, asset_file):
        """ Read data from asset file. """
        assets_data = {}
        execfile(asset_file, assets_data)
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
    
    if action == 'init':
        initialize_asset_file(args.assetfile)
    else:
        wrangler = Wrangler(asset_file=args.assetfile, config=config,
                        targets=args.targets)
        getattr(wrangler, action)()
