import time
import logging
log = logging.getLogger('zen.netAppDiskDSP')

from xml.etree import ElementTree
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredList
from Products.ZenEvents import ZenEventClasses
from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
from ZenPacks.CS.NetApp.SevenMode.lib.ZenOntap import *
from ZenPacks.CS.NetApp.SevenMode.Utils import Utils

class NetAppDiskDSP(PythonDataSourcePlugin, Utils):
    """Python Datasource Plugin to collect graph data for NetApp device."""
 
    proxy_attributes = (
        'zNetAppFiler',
        'zNetAppUser',
        'zNetAppPassword',
        'zNetAppTransport',
        )

    @classmethod
    def params(cls, datasource, context):
        return {'diskUID': context.disk_uid}

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
      for element in naElements:
        if element.child_get('instances') is not None:
          ts = int(element.child_get_string('timestamp'))
          nodes[ts] = {}
          for instance in element.child_get('instances').children_get():
            nameEl, perfEl = instance.children_get()
            name = instance.child_get_string('name')
            nodes[ts][name] = perfEl.children_get()
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

        map = {}
        for ds in config.datasources:
          map[ds.params['diskUID']] = ds.component

        perfGet = {
          'disk': 
            dict.fromkeys(
              [ds.params['diskUID'] for ds in config.datasources],
              [
                ('user_reads', 'RATE'),
                ('user_writes', 'RATE'),
              ]
            )
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

        for ts, components in tsnodes1.iteritems():
          results[ts] = {}
          for component, nodes in components.iteritems():
            results[ts][map[component]] = {}
            for node in nodes:
              name, value = node.children_get()
              dkey = name.element['content']
              dvalue = value.element['content']
              results[ts][map[component]][dkey] = float(dvalue)
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

        for ts, components in tsnodes2.iteritems():
          results[ts] = {}
          for component, nodes in components.iteritems():
            results[ts][map[component]] = {}
            for node in nodes:
              name, value = node.children_get()
              dkey = name.element['content']
              dvalue = value.element['content']
              results[ts][map[component]][dkey] = float(dvalue)
        ###############
        
        request = NaElement('disk-list-info')
        response = server.invoke_elem_async(request)
        deferreds = [response]
        defs = yield DeferredList(deferreds, consumeErrors=True)
        naElements = self._get_elements(defs)
        if naElements is None:
          returnValue(None)
        disks = naElements[0].child_get('disk-details')
        for disk in disks.children_get():
          if disk.child_get_string('raid-state') == 'present':
            component = disk.child_get_string('name')
            results[ts][component]['size_total'] = disk.child_get_int('physical-space')
            results[ts][component]['size_used'] = disk.child_get_int('used-space')
        log.debug('%s', results)
        returnValue(results)

    def onResult(self, result, config):
        """
        Called first for success and error.
        """
        
        if result is None:
          return False

        t1, t2 = sorted(result.keys())
        components = [ds.component for ds in config.datasources]
        
        for component in components:
          result[component] = {}
          result[component]['user_reads'] = self._rate(
            result[t2][component]['user_reads'], result[t1][component]['user_reads'],
            t2, t1)
          result[component]['user_writes'] = self._rate(
            result[t2][component]['user_writes'], result[t1][component]['user_writes'],
            t2, t1)
          
          result[component]['size_used'] = result[t2][component]['size_used']
          result[component]['size_available'] = result[t2][component]['size_total'] - result[t2][component]['size_used']
          result[component]['percentage_used'] = int(100. * result[t2][component]['size_used'] / result[t2][component]['size_total'])
        #log.debug('%s', result)
        return result
 
    def onSuccess(self, result, config):
        """
        Called only on success. After onResult, before onComplete.
        """
        
        data = self.new_data()
        ts = time.time()
        components = [ds.component for ds in config.datasources]
        
        for component in components:
          graphPoints = data['values'][component]
          graphPoints['disk_user_reads'] = (result[component]['user_reads'], ts)
          graphPoints['disk_user_writes'] = (result[component]['user_writes'], ts)
          graphPoints['disk_size_used'] = (result[component]['size_used'], ts)
          graphPoints['disk_size_available'] = (result[component]['size_available'], ts)
          graphPoints['disk_percentage_used'] = (result[component]['percentage_used'], ts)
        
        return data
 
    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        return {
            'events': [{
                'summary': 'error: %s' % result,
                'eventKey': 'netappdisk_datasource_result',
                'severity': 4,
                }],
            }
