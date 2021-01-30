# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

import bpy
from bpy.types import AddonPreferences, Operator, Panel
from bpy.props import BoolProperty, StringProperty, EnumProperty


bl_info = {
    "name": "Collection Master",
    "description": "show hide collection",
    "author": "Daniel Grauer",
    "version": (1, 1, 0),
    "blender": (2, 83, 0),
    "location": "TopBar",
    "category": "System",
    "wiki_url": "https://github.com/kromar/blender_CollectionMaster",
    "tracker_url": "https://github.com/kromar/blender_CollectionMaster/issues",
}


class CM_PT_CollectionMaster(Panel):    
    bl_label = 'Collection Master'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CoMa'

    def draw(self, context):
        pref = context.preferences.addons[__package__.split(".")[0]].preferences 
        
        layout = self.layout           
        layout.operator(operator="scene.collection_master", text=pref.collection_prefix, icon='COLLECTION_COLOR_03', emboss=True, depress=False)
            

class CollectionMaster_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    


    def execute(self, context):        
        pref = context.preferences.addons[__package__.split(".")[0]].preferences

        for collection in bpy.data.collections:            
            prefix = pref.collection_prefix.replace(",", " ").split() # breaks response into words
           
            if any(collection.name.startswith(s) for s in prefix):
                if collection.hide_viewport:
                    collection.hide_viewport = False
                else:            
                    collection.hide_viewport = True
                if pref.collection_color:
                    collection.color_tag = 'COLOR_03'                 
                print("Collection: ", collection.name, "Hide: ", collection.hide_viewport)

        
        return{'FINISHED'}



class CollectionMasterPreferences(AddonPreferences):
    bl_idname = __package__

    collection_prefix: StringProperty(
        name="collection_prefix", 
        description="collection_prefix", 
        subtype='NONE',
        default="Physics_",
        update=CM_PT_CollectionMaster.draw) 
        
    collection_color: BoolProperty(
        name="collection_color",
        description="change collection_color",
        default=True)
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True 
        layout.prop(self, 'collection_color') 
        layout.prop(self, 'collection_prefix')
        


classes = (
    CollectionMaster_OT_run,
    CM_PT_CollectionMaster,
    CollectionMasterPreferences,
    )

def register():    
    [bpy.utils.register_class(c) for c in classes]


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
    register()
