from Products.ZenModel.Device import Device
from Products.ZenRelations.RelSchema import ToManyCont, ToOne


class NetAppDevice(Device):
    """NetApp Device"""
    meta_type = portal_type = 'NetAppDevice'

    _relations = Device._relations + (
        ('aggregates',
         ToManyCont(ToOne,
                    'ZenPacks.CS.NetApp.SevenMode.Aggregate',
                    'netapp_device')
         ),
    )
