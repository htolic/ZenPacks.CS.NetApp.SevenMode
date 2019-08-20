from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class Plex(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetAppPlex'

    plex_name = None
    plex_state = None

    _properties = ManagedEntity._properties + (
        {'id': 'plex_name', 'type': 'string'},
        {'id': 'plex_state', 'type': 'boolean'},
    )

    _relations = ManagedEntity._relations + (
        ('aggregate',
         ToOne(ToManyCont,
               'ZenPacks.CS.NetApp.SevenMode.Aggregate',
               'plexes')
         ),
        ('raid_groups',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.RaidGroup',
                    'plex')
         ),
    )

    factory_type_information = ({
        'actions': ({
            'id': 'perfConf',
            'name': 'Template',
            'action': 'objTemplates',
            'permissions': (ZEN_CHANGE_DEVICE,),
        },),
    },)

    def device(self):
        return self.aggregate().netapp_device()

    def getRRDTemplateName(self):
        return 'NetApp7Mode_Plex'
