import os, sys
import webbrowser
import threading
import time
import requests
import django
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application 
import cherrypy
from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler




os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

class DjangoApplication(object):
    HOST = "127.0.0.1"
    PORT = 8020

    with open(os.path.join(settings.BASE_DIR, "config.ini"), "r") as cfg:    
        content = cfg.readlines()
        HOST = content[0][12:-1].strip(" ")
        PORT = int(content[1][6:-1].strip(" "))   

    def open_browser(self):
        while True:
            try:
                c = requests.get('http://' + self.HOST + ':' +  str(self.PORT) + '/')
                if c.status_code == 200:
                    webbrowser.open_new_tab('http://' + self.HOST + ':' +  str(self.PORT) + '/')
                    break
            except Exception as e:
                time.sleep(0.2)     
        
    def mount_static(self, url, root):
        """
        :param url: Relative url
        :param root: Path to static files root
        """
        config = {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': root,
            'tools.expires.on': True,
            'tools.expires.secs': 86400
        }
        cherrypy.tree.mount(None, url, {'/': config})

    def run(self):
        cherrypy.config.update({
            'server.socket_host': self.HOST,
            'server.socket_port': self.PORT,
            'engine.autoreload_on': False,
            'log.screen': True
        })
        self.mount_static(settings.STATIC_URL, settings.STATIC_ROOT)
        #cherrypy.process.plugins.PIDFile(cherrypy.engine, os.path.join(settings.BASE_DIR, 'IRCapp.pid')).subscribe()
        cherrypy.log("Loading and serving Django application")
        cherrypy.tree.graft(WSGIHandler())
        cherrypy.engine.start()
        
        t = threading.Thread(target=self.open_browser())
        t.deamon = True
        t.start()        

        cherrypy.engine.block()

if __name__ == '__main__':
            
    from ircapp.models import *
    from ircapp.download import *
    from ircapp.forms import *
    from ircapp.logs import *
    application = get_wsgi_application()    
    
    if sys.platform == "win32":
        if not os.path.isdir(os.path.join(os.environ["LOCALAPPDATA"], "IRCapp")):
            os.makedirs(os.path.join(os.environ["LOCALAPPDATA"], "IRCapp"))
            
    log().clear()
    #from django.core.management import execute_from_command_line
    #execute_from_command_line()
    try:
        Download_Settings.objects.all().delete()
    except:
        call_command('migrate', verbosity=0)#displaying stdout will result into an error in a GUI frozen application with cx freeze
        Download_Settings.objects.all().delete()
    finally:
        Download_Settings().save()
        if Download_Ongoing.objects.all().count() > 0:        
            if not Download_Ongoing.objects.latest("id").active:
                Download_Ongoing.objects.all().delete()            
            else:
                obj = Download_Ongoing.objects.latest("id")
                obj.status = "Interrupted"
                obj.save()            
                
        if Quick_Download.objects.all().count() == 0:
            Quick_Download().save()
        if Quick_Download_Excludes.objects.all().count() == 0:        
            Quick_Download_Excludes(excludes="ts").save()
            Quick_Download_Excludes(excludes="cam").save()

    
                
    
    DjangoApplication().run() 

