import Globals
import os.path

from Products.ZenModel.ZenPack import ZenPackBase
from Products.CMFCore.DirectoryView import registerDirectory

skinsDir = os.path.join(os.path.dirname(__file__), 'skins')
if os.path.isdir(skinsDir):
    registerDirectory(skinsDir, globals())


class ZenPack(ZenPackBase):
    packZProperties = [
        ('zNetAppFiler', '', 'string'),
        ('zNetAppUser', 'root', 'string'),
        ('zNetAppPassword', '', 'password'),
        ('zNetAppTransport', 'HTTPS', 'string'),
    ]

    def install(self, app):
        sevenMode = app.getDmdRoot(
            'Devices').createOrganizer('Storage/NetApp/7Mode')

        super(ZenPack, self).install(app)

        plugins = [
            'CS.ZAPI.NetApp7Mode',
        ]

        templates = [
            'NetApp7Mode_Device',
        ]

        sevenMode.setZenProperty('zCollectorPlugins', plugins)
        sevenMode.setZenProperty('zDeviceTemplates', templates)
        sevenMode.setZenProperty(
            'zPythonClass', 'ZenPacks.CS.NetApp.SevenMode.NetAppDevice')
        sevenMode.setZenProperty('zSnmpMonitorIgnore', 'true')
        sevenMode.setZenProperty(
            'zIcon', '/zport/dmd/++resource++netapp/img/icon.png')
