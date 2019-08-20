from Products.Zuul.form import schema
from Products.Zuul.interfaces.device import IDeviceInfo
from Products.Zuul.interfaces.component import IComponentInfo
from Products.Zuul.utils import ZuulMessageFactory as _t


class INetAppDeviceInfo(IDeviceInfo):
    """Info"""


class IAggregateInfo(IComponentInfo):
    aggr_name = schema.TextLine(title=_t('Aggregate Name'))
    aggr_state = schema.TextLine(title=_t('Aggregate State'))
    mount_state = schema.TextLine(title=_t('Mount State'))
    raid_size = schema.Int(title=_t('RAID Size'))
    raid_status = schema.TextLine(title=_t('RAID Status'))
    disk_count = schema.Int(title=_t('Disk Count'))
    volume_count = schema.Int(title=_t('Volume Count'))
    plex_count = schema.Int(title=_t('Plex Count'))
    total_bytes = schema.Int(title=_t('Total Bytes'))


class IPlexInfo(IComponentInfo):
    plex_name = schema.TextLine(title=_t('Plex Name'))
    plex_state = schema.Bool(title=_t('Plex State'))


class IRaidGroupInfo(IComponentInfo):
    rg_name = schema.TextLine(title=_t('RAID Group Name'))


class IDiskInfo(IComponentInfo):
    disk_name = schema.TextLine(title=_t('Disk Name'))
    disk_uid = schema.TextLine(title=_t('Disk UID'))
    node = schema.TextLine(title=_t('Node'))
    raid_state = schema.TextLine(title=_t('RAID State'))
    raid_type = schema.TextLine(title=_t('RAID Type'))
    bay = schema.Int(title=_t('Bay'))
    byte_per_sector = schema.Int(title=_t('Byte Per Sector'))
    disk_type = schema.TextLine(title=_t('Disk Type'))
    rpm = schema.Int(title=_t('RPMs'))
    model = schema.TextLine(title=_t('Model'))
    serialnr = schema.TextLine(title=_t('Serial Number'))
    firmware = schema.TextLine(title=_t('Firmware'))
    poweron_hours = schema.Int(title=_t('Poweron Hours'))
    grown_defect_list_count = schema.Int(title=_t('Grown Defect List Count'))
    total_bytes = schema.Int(title=_t('Total Bytes'))


class IVolumeInfo(IComponentInfo):
    volume_name = schema.TextLine(title=_t('Volume Name'))
    volume_type = schema.TextLine(title=_t('Volume Type'))
    block_type = schema.TextLine(title=_t('Block Type'))
    volume_state = schema.TextLine(title=_t('Volume State'))
    mirror_status = schema.TextLine(title=_t('Mirror Status'))
    inconsistent = schema.TextLine(title=_t('Inconsistent'))
    unrecoverable = schema.TextLine(title=_t('Unrecoverable'))
    invalid = schema.TextLine(title=_t('Invalid'))
    total_bytes = schema.Int(title=_t('Total Bytes'))


class ISpareDiskInfo(IComponentInfo):
    sparedisk_name = schema.TextLine(title=_t('Spare Disk Name'))
    disk_uid = schema.TextLine(title=_t('Disk UID'))
    node = schema.TextLine(title=_t('Node'))
    raid_state = schema.TextLine(title=_t('RAID State'))
    raid_type = schema.TextLine(title=_t('RAID Type'))
    bay = schema.Int(title=_t('Bay'))
    byte_per_sector = schema.Int(title=_t('Byte Per Sector'))
    disk_type = schema.TextLine(title=_t('Disk Type'))
    rpm = schema.Int(title=_t('RPMs'))
    model = schema.TextLine(title=_t('Model'))
    serialnr = schema.TextLine(title=_t('Serial Number'))
    firmware = schema.TextLine(title=_t('Firmware'))
    poweron_hours = schema.Int(title=_t('Poweron Hours'))
    grown_defect_list_count = schema.Int(title=_t('Grown Defect List Count'))
    total_bytes = schema.Int(title=_t('Total Bytes'))
