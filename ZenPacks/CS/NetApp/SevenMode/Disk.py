from Products.ZenModel.DeviceComponent import DeviceComponent
from Products.ZenModel.ManagedEntity import ManagedEntity
from Products.ZenModel.ZenossSecurity import ZEN_CHANGE_DEVICE, ZEN_VIEW
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class Disk(DeviceComponent, ManagedEntity):
    meta_type = portal_type = 'NetAppDisk'

    disk_name = None
    disk_uid = None
    node = None
    raid_state = None
    raid_type = None
    bay = None
    byte_per_sector = None
    disk_type = None
    rpm = None
    model = None
    serialnr = None
    firmware = None
    poweron_hours = None
    grown_defect_list_count = None
    total_bytes = None

    _properties = ManagedEntity._properties + (
        {'id': 'disk_name', 'type': 'string'},
        {'id': 'disk_uid', 'type': 'string'},
        {'id': 'node', 'type': 'string'},
        {'id': 'raid_state', 'type': 'string'},
        {'id': 'raid_type', 'type': 'string'},
        {'id': 'bay', 'type': 'int'},
        {'id': 'byte_per_sector', 'type': 'int'},
        {'id': 'disk_type', 'type': 'string'},
        {'id': 'rpm', 'type': 'int'},
        {'id': 'model', 'type': 'string'},
        {'id': 'serialnr', 'type': 'string'},
        {'id': 'firmware', 'type': 'string'},
        {'id': 'poweron_hours', 'type': 'int'},
        {'id': 'grown_defect_list_count', 'type': 'int'},
        {'id': 'total_bytes', 'type': 'long'},
    )

    _relations = ManagedEntity._relations + (
        ('raid_group',
         ToOne(ToManyCont,
               'ZenPacks.CS.NetApp.SevenMode.RaidGroup',
               'disks')
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
        return self.raid_group().plex().aggregate().netapp_device()

    def getRRDTemplateName(self):
        return 'NetApp7Mode_Disk'
