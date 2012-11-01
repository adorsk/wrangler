import wrangler.assets as assets
import sys


class Processor(object):
    """ Process and resolve a given set of asset definitions. """
    def __init__(self, cache_dir=None, target_dir=None):
        self.cache_dir = cache_dir
        self.target_dir = target_dir

    def resolve_asset_defs(self, asset_definitions={}):
        for asset_id, asset_def in asset_definitions.items():
            self.resolve_asset_def(asset_id, asset_def)

    def resolve_asset_def(self, asset_id, asset_def):
        # Create asset from asset definition.
        print >> sys.stderr, "Resolving '%s'..." % (asset_id)
        asset = self.asset_def_to_asset(asset_id, asset_def)
        asset.resolve()

    def asset_def_to_asset(self, asset_id, asset_def):
        """ Convert an asset definition to an asset object. """
        asset_args = {
            'id': asset_id,
            'cache_dir': self.cache_dir,
            'target_dir': self.target_dir
        }
        asset_args.update(asset_def)

        asset_type = asset_def.get('type')

        if asset_type == 'git':
            AssetClass = assets.GitAsset
        elif asset_type == 'rsync':
            AssetClass = assets.RsyncAsset
        elif asset_type == 'hg':
            AssetClass = assets.HgAsset
        elif asset_type == 'url':
            AssetClass = assets.UrlAsset

        return AssetClass(**asset_args)
