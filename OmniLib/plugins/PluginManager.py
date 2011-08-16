import OmniLib
import OmniLib.debug
import os,sys

# HTTP_PLUGINS.append(__import__("libmiddler.plugins.http.%s"%filename[:-3], None, None, "libmiddler.plugins.http"))

def LoadPlugins(category):
    ret_plugins = []
    plugins_dir = os.curdir + "/" + "OmniLib" + "/" + "plugins" + "/" + category + "/"
    #plugin_files = os.listdir(plugins_dir)
    plugins_dir=plugins_dir[2:]
    OmniLib.debug.debug("DEBUG: plugins dir=" + plugins_dir)

    for plugin in os.listdir(plugins_dir):
	if(plugin[-3:] == ".py" and plugin[1] != "_"):
	    OmniLib.debug.debug("DEBUG: loading " + ("OmniLib.plugins." + category + "." + plugin[:-3]))
	    ret_plugins.append(__import__(("OmniLib.plugins." + category + "." + plugin[:-3]), None, None, ("OmniLib.plugins." + category)))
	    
    return ret_plugins

# TODO: fix this up, seems makeshift
def LoadPlugins_ext(e):
    return (__import__(("OmniLib.plugins." + "ext" + "." + e[:-3]), None, None, ("OmniLib.plugins." + "ext")))
    
# This function allows the plugin to override any attributes of the caller (parent) - EXPERIMENTAL
def PluginSync(parent, plugin):
    print "parent:" + str(parent.__dict__)
    print "plugin:" + str(plugin.__dict__)
    for parent_key in parent.__dict__.keys():
	for plugin_key in plugin.__dict__.keys():
	    if plugin_key == parent_key and plugin_key != '__doc__' and plugin_key != '__module__':
		parent.__dict__[plugin_key] = plugin.__dict__[plugin_key]
