from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class RaidGroup(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetAppRaidGroup'

    rg_name = None

    _properties = ManagedEntity._properties + (
        {'id': 'rg_name', 'type': 'string'},
    )

    _relations = ManagedEntity._relations + (
        ('plex',
         ToOne(ToManyCont,
               'ZenPacks.CS.NetApp.SevenMode.Plex',
               'raid_groups')
         ),
        ('disks',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.Disk',
                    'raid_group')
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
        return self.plex().aggregate().netapp_device()

    def getRRDTemplateName(self):
        return 'NetApp7Mode_RaidGroup'
