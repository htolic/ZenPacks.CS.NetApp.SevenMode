from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE, ZEN_VIEW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class Volume(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetAppVolume'

    volume_name = None
    volume_type = None
    block_type = None
    volume_state = None
    mirror_status = None
    inconsistent = None
    unrecoverable = None
    invalid = None
    total_bytes = None

    _properties = ManagedEntity._properties + (
        {'id': 'volume_name', 'type': 'string'},
        {'id': 'volume_type', 'type': 'string'},
        {'id': 'block_type', 'type': 'string'},
        {'id': 'volume_state', 'type': 'string'},
        {'id': 'mirror_status', 'type': 'string'},
        {'id': 'inconsistent', 'type': 'string'},
        {'id': 'unrecoverable', 'type': 'string'},
        {'id': 'invalid', 'type': 'string'},
        {'id': 'total_bytes', 'type': 'long'},
    )

    _relations = ManagedEntity._relations + (
        ('aggregate',
         ToOne(ToManyCont,
               'ZenPacks.CS.NetApp.SevenMode.Aggregate',
               'volumes')
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
        return 'NetApp7Mode_Volume'
