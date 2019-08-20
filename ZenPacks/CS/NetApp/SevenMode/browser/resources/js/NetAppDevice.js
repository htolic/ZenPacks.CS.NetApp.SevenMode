Ext.onReady(function() {
    var DEVICE_OVERVIEW_ID = 'deviceoverviewpanel_summary';
    Ext.ComponentMgr.onAvailable(DEVICE_OVERVIEW_ID, function(){
        var overview = Ext.getCmp(DEVICE_OVERVIEW_ID);
        overview.removeField('memory');
    });
});


(function(){

var ZC = Ext.ns('Zenoss.component');

ZC.registerName(
    'NetAppAggregate',
    _t('Aggregate'),
    _t('Aggregates'));

ZC.NetAppAggregatePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppAggregate',
            autoExpandColumn: 'aggr_name',
            sortInfo: {
                field: 'aggr_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'aggr_name'},
                {name: 'aggr_state'},
                {name: 'mount_state'},
                {name: 'raid_size'},
                {name: 'raid_status'},
                {name: 'disk_count'},
                {name: 'volume_count'},
                {name: 'plex_count'},
                {name: 'total_bytes'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'aggr_name',
                dataIndex: 'aggr_name',
                header: _t('Aggregate Name'),
                sortable: true
            },{
                id: 'aggr_state',
                dataIndex: 'aggr_state',
                header: _t('Aggregate State'),
                sortable: true,
                width: 120
            },{
                id: 'mount_state',
                dataIndex: 'mount_state',
                header: _t('Mount State'),
                sortable: true,
                width: 120
            },{
                id: 'raid_size',
                dataIndex: 'raid_size',
                header: _t('RAID Size'),
                sortable: true,
                width: 120
            },{
                id: 'raid_status',
                dataIndex: 'raid_status',
                header: _t('RAID Status'),
                sortable: true,
                width: 120
            },{
                id: 'disk_count',
                dataIndex: 'disk_count',
                header: _t('Disk Count'),
                sortable: true,
                width: 120
            },{
                id: 'volume_count',
                dataIndex: 'volume_count',
                header: _t('Volume Count'),
                sortable: true,
                width: 120
            },{
                id: 'plex_count',
                dataIndex: 'plex_count',
                header: _t('Plex Count'),
                sortable: true,
                width: 120
            },{
                id: 'total_bytes',
                dataIndex: 'total_bytes',
                header: _t('Total Bytes'),
                renderer: Zenoss.render.bytesString,
                sortable: true,
                width: 120
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppAggregatePanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppAggregatePanel', ZC.NetAppAggregatePanel);


ZC.registerName(
    'NetAppPlex',
    _t('Plex'),
    _t('Plexes'));

ZC.NetAppPlexPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppPlex',
            autoExpandColumn: 'plex_name',
            sortInfo: {
                field: 'plex_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'plex_name'},
                {name: 'plex_state'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'plex_name',
                dataIndex: 'plex_name',
                header: _t('Plex Name'),
                sortable: true
            },{
                id: 'plex_state',
                dataIndex: 'plex_state',
                header: _t('Plex State'),
                renderer: Zenoss.render.pingStatus,
                sortable: true,
                width: 120
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppPlexPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppPlexPanel', ZC.NetAppPlexPanel);


ZC.registerName(
    'NetAppRaidGroup',
    _t('RAID Group'),
    _t('RAID Groups'));

ZC.NetAppRaidGroupPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppRaidGroup',
            autoExpandColumn: 'rg_name',
            sortInfo: {
                field: 'rg_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'rg_name'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'rg_name',
                dataIndex: 'rg_name',
                header: _t('RAID Group Name'),
                sortable: true
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppRaidGroupPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppRaidGroupPanel', ZC.NetAppRaidGroupPanel);


ZC.registerName(
    'NetAppDisk',
    _t('Disk'),
    _t('Disks'));

ZC.NetAppDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppDisk',
            autoExpandColumn: 'severity',
            sortInfo: {
                field: 'disk_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'disk_name'},
                {name: 'node'},
                {name: 'raid_state'},
                {name: 'raid_type'},
                {name: 'bay'},
                {name: 'byte_per_sector'},
                {name: 'disk_type'},
                {name: 'rpm'},
                {name: 'model'},
                {name: 'serialnr'},
                {name: 'firmware'},
                {name: 'poweron_hours'},
                {name: 'grown_defect_list_count'},
                {name: 'total_bytes'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'disk_name',
                dataIndex: 'disk_name',
                header: _t('Disk Name'),
                sortable: true,
                width: 80
            },{
                id: 'node',
                dataIndex: 'node',
                header: _t('Node'),
                sortable: true,
                width: 110
            },{
                id: 'raid_state',
                dataIndex: 'raid_state',
                header: _t('RAID State'),
                sortable: true,
                width: 90
            },{
                id: 'raid_type',
                dataIndex: 'raid_type',
                header: _t('RAID Type'),
                sortable: true,
                width: 90
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay'),
                sortable: true,
                width: 50
            },{
                id: 'byte_per_sector',
                dataIndex: 'byte_per_sector',
                header: _t('Byte Per Sector'),
                sortable: true,
                width: 100
            },{
                id: 'disk_type',
                dataIndex: 'disk_type',
                header: _t('Disk Type'),
                sortable: true,
                width: 80
            },{
                id: 'rpm',
                dataIndex: 'rpm',
                header: _t('RPMs'),
                sortable: true,
                width: 70
            },{
                id: 'model',
                dataIndex: 'model',
                header: _t('Model'),
                sortable: true,
                width: 130
            },{
                id: 'serialnr',
                dataIndex: 'serialnr',
                header: _t('Serial Number'),
                sortable: true,
                width: 100
            },{
                id: 'firmware',
                dataIndex: 'firmware',
                header: _t('Firmware'),
                sortable: true,
                width: 80
            },{
                id: 'poweron_hours',
                dataIndex: 'poweron_hours',
                header: _t('Poweron Hours'),
                sortable: true,
                width: 95
            },{
                id: 'grown_defect_list_count',
                dataIndex: 'grown_defect_list_count',
                header: _t('Grown Defect List Count'),
                sortable: true,
                width: 130
            },{
                id: 'total_bytes',
                dataIndex: 'total_bytes',
                header: _t('Total Bytes'),
                renderer: Zenoss.render.bytesString,
                sortable: true,
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppDiskPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppDiskPanel', ZC.NetAppDiskPanel);


ZC.registerName(
    'NetAppVolume',
    _t('Volume'),
    _t('Volumes'));

ZC.NetAppVolumePanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppVolume',
            autoExpandColumn: 'volume_name',
            sortInfo: {
                field: 'volume_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'volume_name'},
                {name: 'volume_type'},
                {name: 'block_type'},
                {name: 'volume_state'},
                {name: 'mirror_status'},
                {name: 'inconsistent'},
                {name: 'unrecoverable'},
                {name: 'invalid'},
                {name: 'total_bytes'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'volume_name',
                dataIndex: 'volume_name',
                header: _t('Volume Name'),
                sortable: true
            },{
                id: 'volume_type',
                dataIndex: 'volume_type',
                header: _t('Volume Type'),
                sortable: true,
                width: 120
            },{
                id: 'block_type',
                dataIndex: 'block_type',
                header: _t('Block Type'),
                sortable: true,
                width: 120
            },{
                id: 'volume_state',
                dataIndex: 'volume_state',
                header: _t('Volume State'),
                sortable: true,
                width: 120
            },{
                id: 'mirror_status',
                dataIndex: 'mirror_status',
                header: _t('Mirror Status'),
                sortable: true,
                width: 120
            },{
                id: 'inconsistent',
                dataIndex: 'inconsistent',
                header: _t('Inconsistent'),
                sortable: true,
                width: 120
            },{
                id: 'unrecoverable',
                dataIndex: 'unrecoverable',
                header: _t('Unrecoverable'),
                sortable: true,
                width: 120
            },{
                id: 'invalid',
                dataIndex: 'invalid',
                header: _t('Invalid'),
                sortable: true,
                width: 120
            },{
                id: 'total_bytes',
                dataIndex: 'total_bytes',
                header: _t('Total Bytes'),
                renderer: Zenoss.render.bytesString,
                sortable: true,
                width: 120
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppVolumePanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppVolumePanel', ZC.NetAppVolumePanel);


ZC.registerName(
    'NetAppSpareDisk',
    _t('Spare Disk'),
    _t('Spare Disks'));

ZC.NetAppSpareDiskPanel = Ext.extend(ZC.ComponentGridPanel, {
    constructor: function(config) {
        config = Ext.applyIf(config||{}, {
            componentType: 'NetAppSpareDisk',
            autoExpandColumn: 'severity',
            sortInfo: {
                field: 'sparedisk_name',
                direction: 'ASC'
            },
            fields: [
                {name: 'uid'},
                {name: 'name'},
                {name: 'status'},
                {name: 'severity'},
                {name: 'usesMonitorAttribute'},
                {name: 'monitor'},
                {name: 'monitored'},
                {name: 'locking'},

                {name: 'sparedisk_name'},
                {name: 'node'},
                {name: 'raid_state'},
                {name: 'raid_type'},
                {name: 'bay'},
                {name: 'byte_per_sector'},
                {name: 'disk_type'},
                {name: 'rpm'},
                {name: 'model'},
                {name: 'serialnr'},
                {name: 'firmware'},
                {name: 'poweron_hours'},
                {name: 'grown_defect_list_count'},
                {name: 'total_bytes'}
            ],
            columns: [{
                id: 'severity',
                dataIndex: 'severity',
                header: _t('Events'),
                renderer: Zenoss.render.severity,
                sortable: true,
                width: 50
            },{
                id: 'sparedisk_name',
                dataIndex: 'sparedisk_name',
                header: _t('Spare Disk Name'),
                sortable: true,
                width: 100
            },{
                id: 'node',
                dataIndex: 'node',
                header: _t('Node'),
                sortable: true,
                width: 110
            },{
                id: 'raid_state',
                dataIndex: 'raid_state',
                header: _t('RAID State'),
                sortable: true,
                width: 90
            },{
                id: 'raid_type',
                dataIndex: 'raid_type',
                header: _t('RAID Type'),
                sortable: true,
                width: 90
            },{
                id: 'bay',
                dataIndex: 'bay',
                header: _t('Bay'),
                sortable: true,
                width: 50
            },{
                id: 'byte_per_sector',
                dataIndex: 'byte_per_sector',
                header: _t('Byte Per Sector'),
                sortable: true,
                width: 100
            },{
                id: 'disk_type',
                dataIndex: 'disk_type',
                header: _t('Disk Type'),
                sortable: true,
                width: 80
            },{
                id: 'rpm',
                dataIndex: 'rpm',
                header: _t('RPMs'),
                sortable: true,
                width: 70
            },{
                id: 'model',
                dataIndex: 'model',
                header: _t('Model'),
                sortable: true,
                width: 130
            },{
                id: 'serialnr',
                dataIndex: 'serialnr',
                header: _t('Serial Number'),
                sortable: true,
                width: 100
            },{
                id: 'firmware',
                dataIndex: 'firmware',
                header: _t('Firmware'),
                sortable: true,
                width: 80
            },{
                id: 'poweron_hours',
                dataIndex: 'poweron_hours',
                header: _t('Poweron Hours'),
                sortable: true,
                width: 95
            },{
                id: 'grown_defect_list_count',
                dataIndex: 'grown_defect_list_count',
                header: _t('Grown Defect List Count'),
                sortable: true,
                width: 130
            },{
                id: 'total_bytes',
                dataIndex: 'total_bytes',
                header: _t('Total Bytes'),
                renderer: Zenoss.render.bytesString,
                sortable: true,
                width: 80
            },{
                id: 'monitored',
                dataIndex: 'monitored',
                header: _t('Monitored'),
                renderer: Zenoss.render.checkbox,
                sortable: true,
                width: 70
            },{
                id: 'locking',
                dataIndex: 'locking',
                header: _t('Locking'),
                renderer: Zenoss.render.locking_icons,
                width: 65
            }]
        });

        ZC.NetAppSpareDiskPanel.superclass.constructor.call(
            this, config);
    }
});

Ext.reg('NetAppSpareDiskPanel', ZC.NetAppSpareDiskPanel);

})();
