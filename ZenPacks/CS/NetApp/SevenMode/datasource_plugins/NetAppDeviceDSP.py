import time
import logging
log = logging.getLogger('zen.netAppDeviceDSP')

from xml.etree import ElementTree
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredList
from Products.ZenEvents import ZenEventClasses
from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
from ZenPacks.CS.NetApp.SevenMode.lib.ZenOntap import *
from ZenPacks.CS.NetApp.SevenMode.Utils import Utils

class NetAppDeviceDSP(PythonDataSourcePlugin, Utils):
    """Python Datasource Plugin to collect graph data for NetApp device."""
 
    proxy_attributes = (
        'zNetAppFiler',
        'zNetAppUser',
        'zNetAppPassword',
        'zNetAppTransport',
        )

    def _generate_request(self, perfGet):
      request = NaElement('perf-object-get-instances')
      for perf, instances in perfGet.iteritems():
        request.child_add_string('objectname', perf)
        reqinst = NaElement('instances')
        for instance, counters in instances.iteritems():
          reqinst.child_add_string('instance', instance)
          reqcnts = NaElement('counters')
          for counter in counters:
            reqcnts.child_add_string('counter', counter[0])
            try:
              reqcnts.child_add_string('counter', counter[2])
            except:
              pass
          request.child_add(reqcnts)
        request.child_add(reqinst)
      return request

    def _get_elements(self, defs):
      naElements = []
      for success, result in defs:
        if success:
          status = result.results_status()
          if status == 'passed':
            naElements.append(result)
          elif status == 'failed':
            log.error('%s', result.results_reason())
        else:
          log.error(result.printTraceback())
          return None
      return naElements

    def _get_nodes(self, naElements):
      nodes = {}
      for result in naElements:
        if result.child_get('instances') is not None:
          ts = int(result.child_get_string('timestamp'))
          nodes[ts] = result \
            .child_get('instances') \
            .child_get('instance-data') \
            .child_get('counters') \
            .children_get()
      return nodes

    @inlineCallbacks
    def collect(self, config):
        ds0 = config.datasources[0]
        if ds0.zNetAppFiler == '':
          ds0.zNetAppFiler = ds0.manageIp

        server = ZenOntap(ds0.zNetAppFiler,
                          ds0.zNetAppUser,
                          ds0.zNetAppPassword,
                          ds0.zNetAppTransport)

        perfGet = {
          # object names
          'system': {
            # instances
            'system':
              # counters
              [('avg_processor_busy', 'PERCT', 'cpu_elapsed_time1'),
               ('nfs_ops', 'RATE'),
               ('cifs_ops', 'RATE'),
               ('http_ops', 'RATE'),
               ('fcp_ops', 'RATE'),
               ('iscsi_ops', 'RATE'),
               ('sys_read_latency', 'AVERAGE', 'read_ops'),
               ('sys_write_latency', 'AVERAGE', 'write_ops'),
               ('sys_avg_latency', 'AVERAGE', 'total_ops'),
               ('net_data_recv', 'RATE'),
               ('net_data_sent', 'RATE'),
               ('disk_data_read', 'RATE'),
               ('disk_data_written', 'RATE'),
               ('uptime', 'RAW'),
              ],
            },
          }

        results = {}
        request = self._generate_request(perfGet)

        ##############
        response1 = server.invoke_elem_async(request)
        deferreds = [response1]
        defs = yield DeferredList(deferreds, consumeErrors=True)
        naElements = self._get_elements(defs)
        if naElements is None:
          returnValue(None)
        tsnodes1 = self._get_nodes(naElements)
        
        for ts, nodes in tsnodes1.iteritems():
          results[ts] = {}
          for node in nodes:
            name, value = node.children_get()
            dkey = name.element['content']
            dvalue = value.element['content']
            results[ts][dkey] = float(dvalue)
        ###############
        time.sleep(1)
        ###############
        response2 = server.invoke_elem_async(request)
        deferreds = [response2]
        defs = yield DeferredList(deferreds, consumeErrors=True)
        naElements = self._get_elements(defs)
        if naElements is None:
          returnValue(None)
        tsnodes2 = self._get_nodes(naElements)

        for ts, nodes in tsnodes2.iteritems():
          results[ts] = {}
          for node in nodes:
            name, value = node.children_get()
            dkey = name.element['content']
            dvalue = value.element['content']
            results[ts][dkey] = float(dvalue)
        ###############

        log.debug('RAW: %s', results)
        returnValue(results)

    def onResult(self, result, config):
        """
        Called first for success and error.
        """

        if result is None:
          return False

        t1, t2 = sorted(result.keys())
	log.debug('TIME: %s %s', t1, t2)

        result['cpu_pct'] = self._percent(
          result[t2]['avg_processor_busy'], result[t1]['avg_processor_busy'],
          result[t2]['cpu_elapsed_time1'], result[t1]['cpu_elapsed_time1'])
        result['nfs_ops'] = self._rate(
          result[t2]['nfs_ops'], result[t1]['nfs_ops'],
          t2, t1)
        result['cifs_ops'] = self._rate(
          result[t2]['cifs_ops'], result[t1]['cifs_ops'],
          t2, t1)
        result['http_ops'] = self._rate(
          result[t2]['http_ops'], result[t1]['http_ops'],
          t2, t1)
        result['fcp_ops'] = self._rate(
          result[t2]['fcp_ops'], result[t1]['fcp_ops'],
          t2, t1)
        result['iscsi_ops'] = self._rate(
          result[t2]['iscsi_ops'], result[t1]['iscsi_ops'],
          t2, t1)
        result['read_ops'] = self._rate(
          result[t2]['read_ops'], result[t1]['read_ops'],
          t2, t1)
        result['write_ops'] = self._rate(
          result[t2]['write_ops'], result[t1]['write_ops'],
          t2, t1)
        result['total_ops'] = self._rate(
          result[t2]['total_ops'], result[t1]['total_ops'],
          t2, t1)
        result['sys_read_latency'] = self._average(
          result[t2]['sys_read_latency'], result[t1]['sys_read_latency'],
          result[t2]['read_ops'], result[t1]['read_ops'])
        result['sys_write_latency'] = self._average(
          result[t2]['sys_write_latency'], result[t1]['sys_write_latency'],
          result[t2]['write_ops'], result[t1]['write_ops'])
        result['sys_avg_latency'] = self._average(
          result[t2]['sys_avg_latency'], result[t1]['sys_avg_latency'],
          result[t2]['total_ops'], result[t1]['total_ops'])
        result['net_data_recv'] = (1024./8) * self._rate(
          result[t2]['net_data_recv'], result[t1]['net_data_recv'],
          t2, t1)
        result['net_data_sent'] = (1024./8) * self._rate(
          result[t2]['net_data_sent'], result[t1]['net_data_sent'],
          t2, t1)
        result['disk_data_read'] = (1024./8) * self._rate(
          result[t2]['disk_data_read'], result[t1]['disk_data_read'],
          t2, t1)
        result['disk_data_written'] = (1024./8) * self._rate(
          result[t2]['disk_data_written'], result[t1]['disk_data_written'],
          t2, t1)
        result['uptime'] = result[t2]['uptime'] * 100

	log.debug('ON RESULT: %s', result)
        return result
 
    def onSuccess(self, result, config):
        """
        Called only on success. After onResult, before onComplete.
        """
        data = self.new_data()
        ts = time.time()
        
        graphPoints = data['values'][None]
        graphPoints['device_cpu_pct'] = (result['cpu_pct'], ts)
        graphPoints['device_nfs_ops'] = (result['nfs_ops'], ts)
        graphPoints['device_cifs_ops'] = (result['cifs_ops'], ts)
        graphPoints['device_http_ops'] = (result['http_ops'], ts)
        graphPoints['device_fcp_ops'] = (result['fcp_ops'], ts)
        graphPoints['device_iscsi_ops'] = (result['iscsi_ops'], ts)
        graphPoints['device_read_ops'] = (result['read_ops'], ts)
        graphPoints['device_write_ops'] = (result['write_ops'], ts)
        graphPoints['device_total_ops'] = (result['total_ops'], ts)
        graphPoints['device_sys_read_latency'] = (result['sys_read_latency'], ts)
        graphPoints['device_sys_write_latency'] = (result['sys_write_latency'], ts)
        graphPoints['device_sys_avg_latency'] = (result['sys_avg_latency'], ts)
        graphPoints['device_net_data_recv'] = (result['net_data_recv'], ts)
        graphPoints['device_net_data_sent'] = (result['net_data_sent'], ts)
        graphPoints['device_disk_data_read'] = (result['disk_data_read'], ts)
        graphPoints['device_disk_data_written'] = (result['disk_data_written'], ts)
        graphPoints['device_sysUpTime'] = (result['uptime'], ts)
        
        return data
 
    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        return {
            'events': [{
                'summary': 'error: %s' % result,
                'eventKey': 'netappdevice_datasource_result',
                'severity': 4,
                }],
            }
