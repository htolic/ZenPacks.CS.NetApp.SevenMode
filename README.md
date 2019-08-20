# NetApp 7-Mode ZenPack

The ZenPack provides monitoring for NetApp data storage devices running ONTAP 7-Mode. Data is collected through ZAPI and ZAPI uses XML and HTTP to communicate with NetApp. NetApp Manageability SDK (NMSDK) provides wrapper around ZAPI in Python. This ZenPack is using these wrapper libraries. I hope I managed to get non-blocking code while waiting for the responses from the NetApp. Python Collector and deferreds are used through code, I hope I did that in a right way.

<a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-01.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-01.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-02.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-02.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-03.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-03.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-04.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-04.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-05.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-05.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-06.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-06.png" width="200px" height="200px" /></a><a target="_blank" href="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-07.png"><img src="https://raw.githubusercontent.com/htolic/ZenPacks.CS.NetApp.SevenMode/master/screenshots/ss-07.png" width="200px" height="200px" /></a>

## Releases

Version 1.0.0 - [Download](https://github.com/htolic/ZenPacks.CS.NetApp.SevenMode/releases/download/v1.0.0/ZenPacks.CS.NetApp.SevenMode-1.0.0-py2.7.egg)

- Released: 2019-02-26
- Requires [PythonCollector ZenPack](https://www.zenoss.com/product/zenpacks/pythoncollector) (>=1.10.1)
- Compatible with Zenoss 4.2.5, Zenoss 6.2.1

## Table of contents

- [NetApp 7-Mode ZenPack](#netapp-7-mode-zenpack)
  - [Releases](#releases)
  - [Table of contents](#table-of-contents)
  - [Features](#features)
    - [Device: NetApp 7-Mode](#device-netapp-7-mode)
    - [Component: Aggregates](#component-aggregates)
    - [Component: Disks](#component-disks)
    - [Component: Plexes](#component-plexes)
    - [Component: RAID Groups](#component-raid-groups)
    - [Component: Spare Disks](#component-spare-disks)
    - [Component: Volumes](#component-volumes)
  - [Usage](#usage)
  - [Changelog](#changelog)

## Features

### Device: NetApp 7-Mode

- Creates Device Class /Storage/NetApp/7Mode
- Creates Event Class /Events/Storage/NetApp
- Adds Modeler Plugin CS.ZAPI.NetApp7Mode
  - Models information about device (serial_no, system_id, system_model, ontap_version)
  - Models information about components:
    - Aggregates (name, state, mount_state, raid_size, raid_status, disk_count, volume_count, plex_count, total_bytes)
    - Disks (name, disk_uid, node, raid_state, raid_type, bay, byte_per_sector, disk_type, rpm, model, serialnr, firmware, poweron_hours, grown_defect_list_count, total_bytes)
    - Plexes (name, state)
    - RAID Groups (name)
    - Spare Disks (name, node, disk_uid, raid_state, raid_type, bay, byte_per_sector, disk_type, rpm, model, serialnr, firmware, poweron_hours, grown_defect_list_count, total_bytes)
    - Volumes (name, type, block_type, volume_state, mirror_status, inconsistent, unrecoverable, invalid, total_bytes)
- Configuration Properties set on class /Storage/NetApp/7Mode
  - zDeviceTemplates - value: NetApp7Mode_Device
  - zPythonClass - value: ZenPacks.CS.NetApp.SevenMode.NetAppDevice
  - zIcon - value: /zport/dmd/++resource++netapp/img/icon.png
  - zSnmpMonitorIgnore - value: true
- New Configuration Properties
  - zNetAppFiler - default: [empty] (if empty, device.manageIp is used)
  - zNetAppTransport - default: HTTPS
  - zNetAppUser - default: root
  - zNetAppPassword - default: [empty]
- Monitoring Template
  - Python datasource_plugin: NetAppDeviceDSP
  - Data Points collected and Graph Definitions:
    - Graph "CPU Utilization" - cpu_pct
    - Graph "Protocol Ops" - nfs_ops, cifs_ops, http_ops, fcp_ops, iscsi_ops
    - Graph "Read-Write Ops" - read_ops, write_ops, total_ops
    - Graph "Latency" - sys_read_latency, sys_write_latency, sys_avg_latency
    - Graph "Network data" - net_data_recv, net_data_sent
    - Graph "Disk data" - disk_data_read, disk_data_written
    - Not displayed on any graph - sysUpTime
  - Thresholds:
    - high CPU utilization
      - Type: MinMaxThreshold
      - Condition: cpu_pct > 50
      - Triggers: Critical severity event in Event Class /Storage/NetApp

### Component: Aggregates

- Monitoring Template
  - Python datasource_plugin: NetAppAggregateDSP
  - Data Points collected and Graph Definitions:
    - Graph "Space Usage" - size_used, size_available
    - Graph "Percent Used" - percentage_used
    - Graph "Read-Write Data" - user_reads, user_writes
  - Thresholds:
    - high aggregate usage
      - Type: MinMaxThreshold
      - Condition: percentage_used > 90
      - Triggers: Critical severity event in Event Class /Storage/NetApp

### Component: Disks

- Monitoring Template
  - Python datasource_plugin: NetAppDiskDSP
  - Data Points collected and Graph Definitions:
    - Graph "Space Usage" - size_used, size_available
    - Graph "Percent Used" - percentage_used
    - Graph "Read-Write Data" - user_reads, user_writes
  - Thresholds:
    - high disk usage
      - Type: MinMaxThreshold
      - Condition: percentage_used > 98
      - Triggers: Critical severity event in Event Class /Storage/NetApp

### Component: Plexes

- No Monitoring Template available as no usable data is provided through ZAPI
- Only "Plex State" collected by modelling the device

### Component: RAID Groups

- No Monitoring Template available as no usable data is provided through ZAPI

### Component: Spare Disks

- Monitoring Template
  - Python datasource_plugin: NetAppSpareDiskDSP
  - Data Points collected and Graph Definitions:
    - Graph "Space Usage" - size_used, size_available
    - Graph "Percent Used" - percentage_used
  - Thresholds:
    - high disk usage
      - Type: MinMaxThreshold
      - Condition: percentage_used > 98
      - Triggers: Critical severity event in Event Class /Storage/NetApp

### Component: Volumes

- Monitoring Template
  - Python datasource_plugin: NetAppVolumeDSP
  - Data Points collected and Graph Definitions:
    - Graph "Space Usage" - size_used, size_available
    - Graph "Percent Used" - percentage_used
    - Graph "Latency" - read_latency, write_latency, avg_latency
    - Graph "Read-Write Data" - read_data, write_data
  - Thresholds:
    - high volume usage
      - Type: MinMaxThreshold
      - Condition: percentage_used > 70
      - Triggers: Critical severity event in Event Class /Storage/NetApp

## Usage

First make sure you are using supported Zenoss version and have ZenPack dependencies on right version installed. Then proceed to download and install this ZenPack using a standard procedure for your version of Zenoss.

This ZenPack monitors NetApp storage devices running only ONTAP 7-Mode. It is tested against NetApp Release 8.2.3 7-Mode. NetApp C-Mode is not supported with this ZenPack and it will not work.

After installation the device class /Storage/NetApp/7Mode is created. Go ahead and modify Configuration Properties for this device class. Look for properties that have name starting with zNetApp.

- zNetAppFiler: This is IP address where ZAPI listens for API requests. Leave this empty if IP address you enter when adding device is the same as IP address of NetApp Controller management interface (this is where ZAPI usually listens). If you ever need to change this property, change it per device of course.
- zNetAppTransport: This will either be HTTP (if ZAPI listens on port TCP/80) or HTTPS (if ZAPI listens on port TCP/443). Check your network configuration and firewall rules so Zenoss can reach Filer on either HTTP or HTTPS.
- zNetAppUser: This defaults to root. If you have user prepared especially for Zenoss monitoring then use that user. The user must have privilege to make queries to ZAPI.
- zNetAppPassword: Enter a password related to user that you use in zNetAppUser property.

Go ahead, add your devices to /Storage/NetApp/7Mode and wait for modelling to finish. If everything goes well, you should see components showing up on device details page. In a couple of minutes the graph data should start populating too.

## Changelog

Version 1.0.0

- Initial release