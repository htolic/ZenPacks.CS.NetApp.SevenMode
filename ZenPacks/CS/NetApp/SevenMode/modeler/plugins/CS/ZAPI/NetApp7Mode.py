import logging
log = logging.getLogger('zen.NetApp.SevenMode')

from Products.DataCollector.plugins.CollectorPlugin import PythonPlugin
from Products.DataCollector.plugins.DataMaps import ObjectMap, RelationshipMap
from Products.ZenUtils.Utils import prepId

from ZenPacks.CS.NetApp.SevenMode.lib.NaElement import NaElement
from ZenPacks.CS.NetApp.SevenMode.lib.ZenOntap import ZenOntap, FailResponse

class NetApp7Mode(PythonPlugin):
    deviceProperties = PythonPlugin.deviceProperties + (
        'zNetAppFiler',
        'zNetAppUser',
        'zNetAppPassword',
        'zNetAppTransport',
        )

    perfGet = {
        # object names
        'system': {
            # instances
            'system':
                # counters
                ['serial_no',
                 'system_id',
                 'hostname',
                 'ontap_version',
                 'system_model'
                ],
            },
        }

    def collect(self, device, unused):

        if device.zNetAppFiler == '':
            device.zNetAppFiler = device.manageIp

        server = ZenOntap(
            device.zNetAppFiler,
            device.zNetAppUser,
            device.zNetAppPassword,
            device.zNetAppTransport)
        
        ###############################################
        # collect general system data
        results = {}

        # prepare request
        request = NaElement('perf-object-get-instances')
        for perf, instances in self.perfGet.iteritems():
            request.child_add_string('objectname', perf)
            reqinst = NaElement('instances')
            for instance, counters in instances.iteritems():
                reqinst.child_add_string('instance', instance)
                reqcnts = NaElement('counters')
                for counter in counters:
                    reqcnts.child_add_string('counter', counter)
                request.child_add(reqcnts)
            request.child_add(reqinst)

        # request data
        try:
            response = server.get(request)
        except FailResponse, e:
            log.warning(e)
            return

        # get data from response
        if response.child_get('instances') is not None:
            elements = response \
                      .child_get('instances') \
                      .child_get('instance-data') \
                      .child_get('counters') \
                      .children_get()
        
        # put data to results
        for element in elements:
            name, value = element.children_get()
            dkey = name.element['content']
            dvalue = value.element['content']
            results[dkey] = dvalue

        #############################################
        # collect components data

        # request
        request = NaElement('aggr-list-info')
        request.child_add_string('verbose', 'true')
        try:
            response = server.get(request)
        except FailResponse, e:
            log.warning(e)
            return

        ##############################################
        # collect aggregates data
        results['aggregates'] = {}
        aggregates = response.child_get('aggregates')
        for aggr in aggregates.children_get():
            agname = aggr.child_get_string('name')
            results['aggregates'][agname] = {
                'name': agname,
                'state': aggr.child_get_string('state'),
                'mount_state': aggr.child_get_string('mount-state'),
                'raid_size': aggr.child_get_string('raid-size'),
                'raid_status': aggr.child_get_string('raid-status'),
                'disk_count': aggr.child_get_string('disk-count'),
                'volume_count': aggr.child_get_string('volume-count'),
                'plex_count': aggr.child_get_string('plex-count'),
                'total_bytes': aggr.child_get_int('size-total'),
                }

            ############################################
            # collect plexes data
            results['aggregates'][agname] \
                   ['plexes'] = {}
            
            # get data from response
            plexes = aggr.child_get('plexes')
            for plex in plexes.children_get():
                plname = plex.child_get_string('name')
                results['aggregates'][agname]['plexes'][plname] = {
                    'name': plname,
                    'state': plex.child_get_string('is-online'),
                    }

                #######################################
                # collect RAID groups data
                results['aggregates'][agname] \
                       ['plexes'][plname] \
                       ['raid_groups'] = {}

                # get data from response
                rgroups = plex.child_get('raid-groups')
                for rgroup in rgroups.children_get():
                    rgname = rgroup.child_get_string('name')
                    results['aggregates'][agname]['plexes'][plname]['raid_groups'][rgname] = {
                        'name': rgname,
                        }
                
                    ######################################
                    # collect disks data
                    results['aggregates'][agname] \
                           ['plexes'][plname] \
                           ['raid_groups'][rgname] \
                           ['disks']= {}

                    # get data from response
                    rdisks = rgroup.child_get('disks')
                    for rdisk in rdisks.children_get():
                        rdiskname = rdisk.child_get_string('name')

                        # request
                        request = NaElement('disk-list-info')
                        request.child_add_string('disk', rdiskname)
                        response = server.get(request)

                        disks = response.child_get('disk-details')
                        for disk in disks.children_get():
                            results['aggregates'][agname]['plexes'][plname]['raid_groups'][rgname]['disks'][rdiskname] = {
                                'name': rdiskname,
                                'node': disk.child_get_string('node'),
                                'disk_uid': disk.child_get_string('disk-uid'),
                                'raid_state': disk.child_get_string('raid-state'),
                                'raid_type': disk.child_get_string('raid-type'),
                                'bay': disk.child_get_string('bay'),
                                'byte_per_sector': disk.child_get_string('bytes-per-sector'),
                                'disk_type': disk.child_get_string('disk-type'),
                                'rpm': disk.child_get_string('rpm'),
                                'model': disk.child_get_string('disk-model'),
                                'serialnr': disk.child_get_string('serial-number'),
                                'firmware': disk.child_get_string('firmware-revision'),
                                'poweron_hours': disk.child_get_string('poweron-hours'),
                                'grown_defect_list_count': disk.child_get_string('grown-defect-list-count'),
                                'total_bytes': disk.child_get_int('physical-space'),
                                }

            ##################################
            # collect volumes data
            results['volumes'] = {}

            volumes = aggr.child_get('volumes')
            for volume in volumes.children_get():
                volumename = volume.child_get_string('name')
                
                # request
                request = NaElement('volume-list-info')
                request.child_add_string('volume', volumename)
                response = server.get(request)

                volumes = response.child_get('volumes')
                for volume in volumes.children_get():
                    results['volumes'][volumename] = {
                        'name': volumename,
                        'type': volume.child_get_string('type'),
                        'block_type': volume.child_get_string('block-type'),
                        'volume_state': volume.child_get_string('state'),
                        'mirror_status': volume.child_get_string('mirror-status'),
                        'inconsistent': volume.child_get_string('is-inconsistent'),
                        'unrecoverable': volume.child_get_string('is-unrecoverable'),
                        'invalid': volume.child_get_string('is-invalid'),
                        'total_bytes': volume.child_get_int('size-total'),
                        }

            ##################################
            # collect spare disks data
            results['spare_disks'] = {}

            # request
            request = NaElement('disk-list-info')
            response = server.get(request)

            disks = response.child_get('disk-details')
            for disk in disks.children_get():
                raid_state = disk.child_get_string('raid-state')
                if raid_state != 'present':
                    diskname = disk.child_get_string('name')
                    results['spare_disks'][diskname] = {
                        'name': diskname,
                        'node': disk.child_get_string('node'),
                        'disk_uid': disk.child_get_string('disk-uid'),
                        'raid_state': raid_state,
                        'raid_type': disk.child_get_string('raid-type'),
                        'bay': disk.child_get_string('bay'),
                        'byte_per_sector': disk.child_get_string('bytes-per-sector'),
                        'disk_type': disk.child_get_string('disk-type'),
                        'rpm': disk.child_get_string('rpm'),
                        'model': disk.child_get_string('disk-model'),
                        'serialnr': disk.child_get_string('serial-number'),
                        'firmware': disk.child_get_string('firmware-revision'),
                        'grown_defect_list_count': disk.child_get_string('grown-defect-list-count'),
                        'total_bytes': disk.child_get_int('physical-space'),
                        }
                    if raid_state != 'partner':
                        results['spare_disks'][diskname]['poweron_hours'] = disk.child_get_string('poweron-hours')
                    else:
                        results['spare_disks'][diskname]['poweron_hours'] = '0'
                        

        #log.info(results)
        return results

    def process(self, device, results, unused):
        maps = []

        # NetAppDevice
        maps.append(self.objectMap(dict(
            renameDevice = results['hostname'],
            setHWSerialNumber = results['serial_no'],
            setHWTag = results['system_id'],
            setHWProductKey = results['system_model'],
            setOSProductKey = results['ontap_version'].split(':')[0],
            )))

        # Aggregate Component
        maps.extend(self.getAggsRelMaps(
            results['aggregates'],
            results['volumes'],
            results['spare_disks']
            ))

        return maps

    def getAggsRelMaps(self, aggregates, volumes, spare_disks):
        obj_maps = []
        rel_maps = []

        for name, data in aggregates.iteritems():
            aggr_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = aggr_id,
                aggr_name = name,
                aggr_state = data['state'],
                mount_state = data['mount_state'],
                raid_size = data['raid_size'],
                raid_status = data['raid_status'],
                disk_count = data['disk_count'],
                volume_count = data['volume_count'],
                plex_count = data['plex_count'],
                total_bytes = data['total_bytes'],
                )))

            # Plex Component
            rel_maps.extend(self.getPlexesRelMaps(
                aggregates[name]['plexes'],
                'aggregates/{0}'.format(aggr_id)
                ))

            # Volume component
            # TODO: put each volume to its aggregate only
            #       now it works only when one aggregate is configured
            rel_maps.extend(self.getVolumesRelMaps(
                volumes,
                'aggregates/{0}'.format(aggr_id)
                ))

            # SpareDisk component
            rel_maps.extend(self.getSpareDisksRelMaps(
                spare_disks,
                'aggregates/{0}'.format(aggr_id)
                ))

        return [RelationshipMap(
            relname = 'aggregates',
            modname = 'ZenPacks.CS.NetApp.SevenMode.Aggregate',
            objmaps = obj_maps)] + rel_maps

    def getPlexesRelMaps(self, plexes, compname):
        obj_maps = []
        rel_maps = []

        for name, data in plexes.iteritems():
            plx_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = plx_id,
                plex_name = name,
                plex_state = bool(data['state']),
                )))

            # RaidGroup component
            rel_maps.extend(self.getRaidGroupsRelMaps(
                plexes[name]['raid_groups'],
                '{0}/plexes/{1}'.format(compname, plx_id)
                ))

        return [RelationshipMap(
            compname = compname,
            relname = 'plexes',
            modname = 'ZenPacks.CS.NetApp.SevenMode.Plex',
            objmaps = obj_maps)] + rel_maps

    def getRaidGroupsRelMaps(self, rgroups, compname):
        obj_maps = []
        rel_maps = []

        for name, data in rgroups.iteritems():
            rg_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = rg_id,
                rg_name = name,
                )))

            # Disk component
            rel_maps.extend(self.getDisksRelMaps(
                rgroups[name]['disks'],
                '{0}/raid_groups/{1}'.format(compname, rg_id)
                ))

        return [RelationshipMap(
            compname = compname,
            relname = 'raid_groups',
            modname = 'ZenPacks.CS.NetApp.SevenMode.RaidGroup',
            objmaps = obj_maps)] + rel_maps

    def getDisksRelMaps(self, disks, compname):
        obj_maps = []

        for name, data in disks.iteritems():
            disk_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = disk_id,
                disk_name = name,
                disk_uid = data['disk_uid'],
                node = data['node'],
                raid_state = data['raid_state'],
                raid_type = data['raid_type'],
                bay = data['bay'],
                byte_per_sector = data['byte_per_sector'],
                disk_type = data['disk_type'],
                rpm = data['rpm'],
                model = data['model'],
                serialnr = data['serialnr'],
                firmware = data['firmware'],
                poweron_hours = data['poweron_hours'],
                grown_defect_list_count = data['grown_defect_list_count'],
                total_bytes = data['total_bytes'],
                )))

        return [RelationshipMap(
            compname = compname,
            relname = 'disks',
            modname = 'ZenPacks.CS.NetApp.SevenMode.Disk',
            objmaps = obj_maps)]

    def getVolumesRelMaps(self, volumes, compname):
        obj_maps = []
        
        for name, data in volumes.iteritems():
            vol_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = vol_id,
                volume_name = name,
                volume_type = data['type'],
                block_type = data['block_type'],
                volume_state = data['volume_state'],
                mirror_status = data['mirror_status'],
                inconsistent = data['inconsistent'],
                unrecoverable = data['unrecoverable'],
                invalid = data['invalid'],
                total_bytes = data['total_bytes'],
                )))

        return [RelationshipMap(
            compname = compname,
            relname = 'volumes',
            modname = 'ZenPacks.CS.NetApp.SevenMode.Volume',
            objmaps = obj_maps)]

    def getSpareDisksRelMaps(self, spares, compname):
        obj_maps = []

        for name, data in spares.iteritems():
            spare_id = prepId(name)
            obj_maps.append(ObjectMap(data=dict(
                id = spare_id,
                sparedisk_name = name,
                node = data['node'],
                disk_uid = data['disk_uid'],
                raid_state = data['raid_state'],
                raid_type = data['raid_type'],
                bay = data['bay'],
                byte_per_sector = data['byte_per_sector'],
                disk_type = data['disk_type'],
                rpm = data['rpm'],
                model = data['model'],
                serialnr = data['serialnr'],
                firmware = data['firmware'],
                poweron_hours = data['poweron_hours'],
                grown_defect_list_count = data['grown_defect_list_count'],
                total_bytes = data['total_bytes'],
                )))

        return [RelationshipMap(
            compname = compname,
            relname = 'spare_disks',
            modname = 'ZenPacks.CS.NetApp.SevenMode.SpareDisk',
            objmaps = obj_maps)]
