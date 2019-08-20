from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE, ZEN_VIEW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class Aggregate(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetAppAggregate'

    aggr_name = None
    aggr_state = None
    mount_state = None
    raid_size = None
    raid_status = None
    disk_count = None
    volume_count = None
    plex_count = None
    total_bytes = None

    _properties = ManagedEntity._properties + (
        {'id': 'aggr_name', 'type': 'string'},
        {'id': 'aggr_state', 'type': 'string'},
        {'id': 'mount_state', 'type': 'string'},
        {'id': 'raid_size', 'type': 'int'},
        {'id': 'raid_status', 'type': 'string'},
        {'id': 'disk_count', 'type': 'int'},
        {'id': 'volume_count', 'type': 'int'},
        {'id': 'plex_count', 'type': 'int'},
        {'id': 'total_bytes', 'type': 'long'},
    )

    _relations = ManagedEntity._relations + (
        ('netapp_device',
         ToOne(ToManyCont,
               'ZenPacks.CS.NetApp.SevenMode.NetAppDevice',
               'aggregates')
         ),
        ('plexes',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.Plex',
                    'aggregate')
         ),
        ('volumes',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.Volume',
                    'aggregate')
         ),
        ('spare_disks',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.SpareDisk',
                    'aggregate')
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
        return self.netapp_device()

    def getRRDTemplateName(self):
        return 'NetApp7Mode_Aggregate'
