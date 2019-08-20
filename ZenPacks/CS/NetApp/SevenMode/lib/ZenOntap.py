#!/usr/bin/env python
import time, base64
import twisted.web.client
from NaServer import *

class FailResponse(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class ZenOntap(NaServer):
  
  def __init__(self, server, user, pwd, transport):
    super(self.__class__, self).__init__(server, 1, 0)
    self.set_admin_user(user, pwd)
    self.set_transport_type(transport)
    self._set_api_version()

  def _set_api_version(self):
    api = self.invoke('system-get-ontapi-version')
    self.major_version = api.child_get_string('major-version')
    self.minor_version = min(17, api.child_get_string('minor-version'))

  def get_api_version(self):
    return '{0}.{1}'.format(self.major_version, self.minor_version)

  def invoke_elem_async(self, req):
    server = self.server
    port = self.port
    ttype = self.transport_type.lower()
    url = self.url
    xmlrequest = req.toEncodedString()
    user = self.user
    password = self.password
    vf = self.vfiler
    oid = self.originator_id

    vfiler = 'vfiler="{0}" '.format(vf) if vf != '' else ''
    origid = 'originator_id="{0}" '.format(oid) if oid != '' else ''

    url = '{0}://{1}:{2}{3}'.format(ttype, server, port, url)
    method = 'POST'
    uname_pass = '{0}:{1}'.format(user, password)
    base64auth = base64.encodestring(uname_pass)[:-1]
    content = (
      '<?xml version="1.0" encoding="utf-8"?>',
      '<!DOCTYPE netapp SYSTEM "{0}">'.format(self.dtd),
      '<netapp {0}{1}'.format(vfiler, origid),
      'version="{0}.{1}" '.format(self.major_version, self.minor_version),
      'xmlns="{0}">'.format(ZAPI_xmlns),
      xmlrequest,
      '</netapp>',
      )
    content = '{0}{1}{2}{3}{4}{5}{6}'.format(*content)
    headers = {
      'Content-type': 'text/xml; charset="UTF-8"',
      'Authorization': 'Basic {0}'.format(base64auth),
      'Content-length': len(content),
      }

    def process_result(raw):
      return self.parse_xml(raw)

    return twisted.web.client.getPage(
      url, method = method, headers = headers,
      postdata = content).addCallback(process_result)

  def get(self, element):
    response = self.invoke_elem(element)
    if response.results_status() == 'failed':
      err = '[{0}] {1}'
      err = err.format(response.results_errno(), response.results_reason())
      raise FailResponse(err)
    else:
      return response


if __name__ == '__main__':
  from twisted.internet import reactor, defer
  from NaElement import NaElement

  def callback(results):
    reactor.stop()
    naElements = []
    for success, result in results:
      if success:
        status = result.results_status()
        if status == 'passed':
          naElements.append(result)
        elif status == 'failed':
          print result.results_reason()
      else:
        print result.printTraceback()
    return naElements

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

  server = ZenOntap('8.8.8.8', 'un', 'pw', 'HTTPS')

  request = NaElement('perf-object-get-instances')
  for perf, instances in perfGet.iteritems():
    request.child_add_string('objectname', perf)
    reqinst = NaElement('instances')
    for instance, counters in instances.iteritems():
      reqinst.child_add_string('instance', instance)
      reqcnts = NaElement('counters')
      for counter in counters:
        reqcnts.child_add_string('counter', counter)
      request.child_add(reqcnts)
    request.child_add(reqinst)

  response = server.invoke_elem_async(request)
  deferreds = [response]
  naElements = defer.DeferredList(deferreds, consumeErrors=True).addCallback(callback)
  reactor.run()

  nodes = []
  for result in naElements.__dict__['result']:
    if result.child_get('instances') is not None:
      print result.child_get_string('timestamp')
      nodes.extend(result \
             .child_get('instances') \
             .child_get('instance-data') \
             .child_get('counters') \
             .children_get())

  perf = {}
  for node in nodes:
    name, value = node.children_get()
    dkey = name.element['content']
    dvalue = value.element['content']
    perf[dkey] = dvalue

  print perf
