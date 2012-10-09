#/usr/bin/env python
""" Main executable. """
import sys
import os
import shutil
from processor import Processor


config = {}

#@TODO: get config from a more standard place.
def read_config():
    config_path = '.wrangler.py'
    execfile(config_path, config)

def init():
    """ Create the initial AssetFile. """
    asset_file_target = 'AssetFile.py'
    if os.path.exists(asset_file_target):
        print >> sys.stderr, "Already initialized."
        return

    asset_file_tpl = os.path.join(os.path.abspath(__file__), 'templates', 'AssetFile.py')
    os.copy(asset_file_tpl, asset_file_target)
    print >> sys.stderr, "Initialized with AssetFile.py ."

def show():
    pass

def clean():
    """ Clear out the target dir. """
    for item in os.listdir(config['TARGET_DIR']):
        item_path = os.path.join(config['TARGET_DIR'], item)
        shutil.rmtree(item_path)

def install():
    """ Install assets in target dir. """
    # Read in asset file.
    assets_file_path = 'AssetFile.py'
    assets_data = {}
    execfile(assets_file_path, assets_data)

    # Update config.
    #config.update(assets_data['config'])

    # Resolve assets.
    processor = Processor()
    processor.resolve_asset_defs(assets_data['assets'])

if __name__ == '__main__':
    # Read the config.
    print "yo"
