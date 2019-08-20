import time
import logging
log = logging.getLogger('zen.netAppAggregateDSP')

from xml.etree import ElementTree
from twisted.internet.defer import inlineCallbacks, returnValue, DeferredList
from Products.ZenEvents import ZenEventClasses
from ZenPacks.zenoss.PythonCollector.datasources.PythonDataSource \
    import PythonDataSourcePlugin
from ZenPacks.CS.NetApp.SevenMode.lib.ZenOntap import *
from ZenPacks.CS.NetApp.SevenMode.Utils import Utils

class NetAppAggregateDSP(PythonDataSourcePlugin, Utils):
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

        perfGet = {
          'aggregate': 
            dict.fromkeys(
              [ds.component for ds in config.datasources],
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
            results[ts][component] = {}
            for node in nodes:
              name, value = node.children_get()
              dkey = name.element['content']
              dvalue = value.element['content']
              results[ts][component][dkey] = float(dvalue)
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
            results[ts][component] = {}
            for node in nodes:
              name, value = node.children_get()
              dkey = name.element['content']
              dvalue = value.element['content']
              results[ts][component][dkey] = float(dvalue)
        ###############

        request = NaElement('aggr-list-info')
        request.child_add_string('verbose', 'true')
        response = server.invoke_elem_async(request)
        deferreds = [response]
        defs = yield DeferredList(deferreds, consumeErrors=True)
        naElements = self._get_elements(defs)
        if naElements is None:
          returnValue(None)
        aggregates = naElements[0].child_get('aggregates')
        for aggregate in aggregates.children_get():
          component = aggregate.child_get_string('name')
          results[ts][component]['size_used'] = aggregate.child_get_int('size-used')
          results[ts][component]['size_available'] = aggregate.child_get_int('size-available')
          results[ts][component]['percentage_used'] = aggregate.child_get_int('size-percentage-used')

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
          result[component]['size_available'] = result[t2][component]['size_available']
          result[component]['percentage_used'] = result[t2][component]['percentage_used']

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
          graphPoints['aggregate_user_reads'] = (result[component]['user_reads'], ts)
          graphPoints['aggregate_user_writes'] = (result[component]['user_writes'], ts)
          graphPoints['aggregate_size_used'] = (result[component]['size_used'], ts)
          graphPoints['aggregate_size_available'] = (result[component]['size_available'], ts)
          graphPoints['aggregate_percentage_used'] = (result[component]['percentage_used'], ts)

        return data
 
    def onError(self, result, config):
        """
        Called only on error. After onResult, before onComplete.
        """
        return {
            'events': [{
                'summary': 'error: %s' % result,
                'eventKey': 'netappaggregate_datasource_result',
                'severity': 4,
                }],
            }
