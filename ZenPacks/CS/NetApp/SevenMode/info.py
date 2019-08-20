from zope.interface import implements

from Products.Zuul.infos import ProxyProperty
from Products.Zuul.infos.device import DeviceInfo
from Products.Zuul.infos.component import ComponentInfo

from ZenPacks.CS.NetApp.SevenMode.interfaces import (
    INetAppDeviceInfo,
    IAggregateInfo,
    IPlexInfo,
    IRaidGroupInfo,
    IDiskInfo,
    IVolumeInfo,
    ISpareDiskInfo,
)


class NetAppDeviceInfo(DeviceInfo):
    implements(INetAppDeviceInfo)


class AggregateInfo(ComponentInfo):
    implements(IAggregateInfo)

    aggr_name = ProxyProperty('aggr_name')
    aggr_state = ProxyProperty('aggr_state')
    mount_state = ProxyProperty('mount_state')
    raid_size = ProxyProperty('raid_size')
    raid_status = ProxyProperty('raid_status')
    disk_count = ProxyProperty('disk_count')
    volume_count = ProxyProperty('volume_count')
    plex_count = ProxyProperty('plex_count')
    total_bytes = ProxyProperty('total_bytes')


class PlexInfo(ComponentInfo):
    implements(IPlexInfo)

    plex_name = ProxyProperty('plex_name')
    plex_state = ProxyProperty('plex_state')


class RaidGroupInfo(ComponentInfo):
    implements(IRaidGroupInfo)

    rg_name = ProxyProperty('rg_name')


class DiskInfo(ComponentInfo):
    implements(IDiskInfo)

    disk_name = ProxyProperty('disk_name')
    disk_uid = ProxyProperty('disk_uid')
    node = ProxyProperty('node')
    raid_state = ProxyProperty('raid_state')
    raid_type = ProxyProperty('raid_type')
    bay = ProxyProperty('bay')
    byte_per_sector = ProxyProperty('byte_per_sector')
    disk_type = ProxyProperty('disk_type')
    rpm = ProxyProperty('rpm')
    model = ProxyProperty('model')
    serialnr = ProxyProperty('serialnr')
    firmware = ProxyProperty('firmware')
    poweron_hours = ProxyProperty('poweron_hours')
    grown_defect_list_count = ProxyProperty('grown_defect_list_count')
    total_bytes = ProxyProperty('total_bytes')


class VolumeInfo(ComponentInfo):
    implements(IVolumeInfo)

    volume_name = ProxyProperty('volume_name')
    volume_type = ProxyProperty('volume_type')
    block_type = ProxyProperty('block_type')
    volume_state = ProxyProperty('volume_state')
    mirror_status = ProxyProperty('mirror_status')
    inconsistent = ProxyProperty('inconsistent')
    unrecoverable = ProxyProperty('unrecoverable')
    invalid = ProxyProperty('invalid')
    total_bytes = ProxyProperty('total_bytes')


class SpareDiskInfo(ComponentInfo):
    implements(ISpareDiskInfo)

    sparedisk_name = ProxyProperty('sparedisk_name')
    disk_uid = ProxyProperty('disk_uid')
    node = ProxyProperty('node')
    raid_state = ProxyProperty('raid_state')
    raid_type = ProxyProperty('raid_type')
    bay = ProxyProperty('bay')
    byte_per_sector = ProxyProperty('byte_per_sector')
    disk_type = ProxyProperty('disk_type')
    rpm = ProxyProperty('rpm')
    model = ProxyProperty('model')
    serialnr = ProxyProperty('serialnr')
    firmware = ProxyProperty('firmware')
    poweron_hours = ProxyProperty('poweron_hours')
    grown_defect_list_count = ProxyProperty('grown_defect_list_count')
    total_bytes = ProxyProperty('total_bytes')
