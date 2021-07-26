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
    "version": (1, 2, 1),
    "blender": (2, 83, 0),
    "location": "TopBar",
    "category": "System",
    "wiki_url": "https://github.com/kromar/blender_CollectionMaster",
    "tracker_url": "https://github.com/kromar/blender_CollectionMaster/issues",
}


def prefs():
    ''' load addon preferences to reference in code'''
    user_preferences = bpy.context.preferences
    return user_preferences.addons[__package__].preferences 

class CM_PT_CollectionMaster(Panel):    
    bl_label = 'Collection Master'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'CoMa'

    def draw(self, context):       
        prefix = prefs().collection_prefix.replace(",", " ").split()        
        layout = self.layout    
        for i in prefix:
            if not prefs().collection_color == 'NONE':            
                layout.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
            else:    
                layout.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i


class CollectionMaster_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    
    button_input: StringProperty()
    collection_visible: BoolProperty(
        name="collection_visible",
        description="collection_visible",
        default=False)

    def execute(self, context):        
        print("button_input", self.button_input)
        if self.collection_visible:
            self.collection_visible = False
        else:
            self.collection_visible = True  
        self.toggle_visibilty(self.collection_visible)    

        return{'FINISHED'}
    
    def toggle_visibilty(self, visible=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input):
                collection.hide_viewport = visible   

                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
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
        
    use_color: BoolProperty(
        name="use_color",
        description="change use_color",
        default=True)

    def list_populate(self, context):
        colors = [('NONE', '', '', 'OUTLINER_COLLECTION', 0), 
                    ('COLOR_01', '','', 'COLLECTION_COLOR_01', 1), 
                    ('COLOR_02', '','', 'COLLECTION_COLOR_02', 2), 
                    ('COLOR_03', '','', 'COLLECTION_COLOR_03', 3), 
                    ('COLOR_04', '','', 'COLLECTION_COLOR_04', 4), 
                    ('COLOR_05', '','', 'COLLECTION_COLOR_05', 5), 
                    ('COLOR_06', '','', 'COLLECTION_COLOR_06', 6),
                    ('COLOR_07', '','', 'COLLECTION_COLOR_07', 7), 
                    ('COLOR_08', '','', 'COLLECTION_COLOR_08', 8), 
                ]
        return colors

    collection_color: EnumProperty(
        items=list_populate,
        name="collection_color", 
        description="collection_color")
        
    
    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True 
        layout.prop(self, 'use_color') 
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
