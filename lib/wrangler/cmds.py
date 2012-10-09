#/usr/bin/env python
""" Main executable. """
import sys
import os
import shutil
from processor import Processor


config = {}
assets_file_path = 'AssetFile.py'

#@TODO: get config from a more standard place.
def read_config():
    config_path = '.wrangler.py'
    execfile(config_path, config)

def init():
    """ Create the initial AssetFile. """
    if os.path.exists(asset_file_path):
        print >> sys.stderr, "Already initialized."
        return

    asset_file_tpl = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                  'templates', 'AssetFile.py')
    shutil.copy(asset_file_tpl, asset_file_path)
    print >> sys.stderr, "Initialized with '%s'." % asset_file_path

def show():
    print >> sys.stderr, "show"
    pass

#@TODO: disabled for now!
def clean():
    """ Clear out the target dir. """
    assets_data = read_assets_file()
    config = assets_data['config']
    for item in os.listdir(config['TARGET_DIR']):
        item_path = os.path.join(config['TARGET_DIR'], item)
        print >> sys.stderr, "removing '%s'..." % item_path
        shutil.rmtree(item_path)

def install():
    """ Install assets in target dir. """
    assets_data = read_assets_file()
    config = assets_data['config']
    for dir_ in [config['CACHE_DIR'], config['TARGET_DIR']]:
        if not os.path.exists(dir_):
            os.mkdir(dir_)

    processor = Processor(
        cache_dir=config['CACHE_DIR'],
        target_dir=config['TARGET_DIR']
    )
    processor.resolve_asset_defs(assets_data['assets'])

def read_assets_file():
    # Read in asset file.
    assets_data = {}
    execfile(assets_file_path, assets_data)
    return assets_data

if __name__ == '__main__':
    cmd = sys.argv[1]
    #@TODO: clean this up.
    fn = globals().get(cmd)
    fn()
