"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

App that launches Screening Room from inside of Shotgun
"""

import tank
import sys
import os

class LaunchScreeningRoom(tank.platform.Application):
    def init_app(self):
        deny_permissions = self.get_setting("deny_permissions")
        deny_platforms = self.get_setting("deny_platforms")
        
        p = {
            "title": "Show in Screening Room",
            "entity_types": ["Version"],
            "deny_permissions": deny_permissions,
            "deny_platforms": deny_platforms,
            "supports_multiple_selection": False
        }
        
        self.engine.register_command("launch_screeningroom", self.launch_screeningroom, p)
    
    def _get_rv_binary(self):
        """
        Returns the RV binary to run
        """
        # get the setting        
        system = sys.platform
        try:
            app_setting = {"linux2": "rv_path_linux", "darwin": "rv_path_mac", "win32": "rv_path_windows"}[system]
            app_path = self.get_setting(app_setting)
            if not app_path: raise KeyError()
        except KeyError:
            raise Exception("Platform '%s' is not supported." % system) 
        
        if system == "darwin":
            # append Contents/MacOS/RV64 to the app bundle path
            app_path = os.path.join(app_path, "Contents/MacOS/RV64") 
        
        return app_path
    
    def launch_screeningroom(self, entity_type, entity_ids):
        tk_shotgun_launchscreeningroom = self.import_module("tk_shotgun_launchscreeningroom")
        
        if len(entity_ids) != 1:
            raise Exception("This action does not work with multiple selection.")

        ctx = {"type" : entity_type, "id": entity_ids[0]}
        try:
            tk_shotgun_launchscreeningroom.screeningroom.launch_timeline(base_url=self.shotgun.base_url, 
                                                            context=ctx,
                                                            path_to_rv=self._get_rv_binary())
        except Exception, e:
            self.log_error("Could not launch Screening Room - check your configuration! "
                            "Error reported: %s" % e)

    
