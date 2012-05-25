"""
Copyright (c) 2012 Shotgun Software, Inc
----------------------------------------------------

App that launches Revolver from inside of Shotgun
"""

import tank
import sys
import os
import platform

class LaunchRevolver(tank.platform.Application):
    def init_app(self):
        entity_types = self.get_setting("entity_types")
        deny_permissions = self.get_setting("deny_permissions")
        deny_platforms = self.get_setting("deny_platforms")
        
        p = {
            "title": "Show in Revolver",
            "entity_types": entity_types,
            "deny_permissions": deny_permissions,
            "deny_platforms": deny_platforms,
            "supports_multiple_selection": False
        }
        
        self.engine.register_command("launch_revolver", self.launch_revolver, p)
    
    def _get_rv_binary(self):
        """
        Returns the RV binary to run
        """
        # get the setting        
        system = platform.system()
        try:
            app_setting = {"Linux": "rv_path_linux", "Darwin": "rv_path_mac", "Windows": "rv_path_windows"}[system]
            app_path = self.get_setting(app_setting)
            if not app_path: raise KeyError()
        except KeyError:
            raise Exception("Platform '%s' is not supported." % system) 
        
        if system == "Darwin":
            # append Contents/MacOS/RV64 to the app bundle path
            app_path = os.path.join(app_path, "Contents/MacOS/RV64") 
        
        return app_path
    
    def launch_revolver(self, entity_type, entity_ids):
        import sg_launch_revolver
        
        if len(entity_ids) != 1:
            raise Exception("This action does not work with multiple selection.")

        ctx = {"type" : entity_type, "id": entity_ids[0]}
        try:
            sg_launch_revolver.revolver.launch_timeline( base_url=self.engine.shotgun.base_url, 
                                                         context=ctx,
                                                         path_to_rv=self._get_rv_binary() )
        except Exception, e:
            self.engine.log_error("Could not launch revolver - check your configuration! "
                                  "Error reported: %s" % e)

    
