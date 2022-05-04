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
from bpy.types import AddonPreferences, Operator, Panel, PropertyGroup
from bpy.props import (EnumProperty, StringProperty, BoolProperty,
                       PointerProperty)


bl_info = {
    "name": "Collection Master",
    "description": "show hide collection",
    "author": "Daniel Grauer",
    "version": (1, 2, 8),
    "blender": (2, 93, 0),
    "location": "View3D > Sidebar > Collection Master",
    "category": "System",
    "wiki_url": "https://github.com/kromar/blender_CollectionMaster",
    "tracker_url": "https://github.com/kromar/blender_CollectionMaster/issues",
}


def prefs():
    ''' load addon preferences to reference in code'''
    user_preferences = bpy.context.preferences
    return user_preferences.addons[__package__].preferences 
 

class VIEW3D_PT_CM(Panel):    
    bl_label = 'Collection Master'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Collection Master'

           
    def draw(self, context):             
        layout = self.layout 
        settings = context.scene.CM 
        column = layout.column(align=True)
        column.prop(settings, 'selected_only', text="Only Selected")

        box = column.box()
        row = box.row(align=True)
        row.label(text="Toggle:")  
        row.prop(settings, 'item_excluded', text="", icon='CHECKBOX_HLT', invert_checkbox=False)
        row.prop(settings, 'item_select', text="", icon='RESTRICT_SELECT_OFF', invert_checkbox=False)
        row.prop(settings, 'item_visible', text="", icon='HIDE_OFF', invert_checkbox=False)
        row.prop(settings, 'item_enabled', text="", icon='RESTRICT_VIEW_OFF', invert_checkbox=False)
        row.prop(settings, 'item_rendered', text="", icon='RESTRICT_RENDER_OFF', invert_checkbox=False)

        box = column.box()
        box.label(text="Restore:")        
        row = box.row(align=True)
        row.operator(operator="scene.collection_master", text="All", emboss=True, depress=False).button_input='ENABLE_ALL'        
                       
        
        #prefix
        box = column.box()
        box.label(text="Prefix:")        
        for i in prefs().collection_prefix.replace(",", " ").split():   
            row = box.row(align=True)
            if not prefs().collection_color == 'NONE':            
                row.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
            else:    
                row.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i
                
        
        #sufix
        box = column.box()
        box.label(text="Suffix:")
        for i in prefs().collection_sufix.replace(",", " ").split():            
            row = box.row(align=True)
            if not prefs().collection_color == 'NONE':            
                row.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
            else:    
                row.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i
                

class CM_PG_Settings(PropertyGroup):
    """General Settings and UI data."""

    selected_only: BoolProperty(
        name="selected_only",
        description="selected_only",
        default=True)  

    item_excluded: BoolProperty(
        name="collection_excluded",
        description="collection_excluded",
        default=False)
    item_select: BoolProperty(
        name="collection_select",
        description="collection_select",
        default=False)
    item_visible: BoolProperty(
        name="collection_visible",
        description="collection_visible",
        default=False)
    item_enabled: BoolProperty(
        name="collection_enabled",
        description="collection_enabled",
        default=False)
    item_rendered: BoolProperty(
        name="collection_rendered",
        description="collection_rendered",
        default=False)


class CM_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    button_input: StringProperty()

    def execute(self, context):   
        
        settings = context.scene.CM      
        #print("Collection Master button_input: ", self.button_input)    
        if self.button_input == 'ENABLE_ALL': 
            if prefs().debug_output:
                print('ENABLE_ALL')
            state = False
            for ob in bpy.data.objects:
                ob.hide_set(state)
                ob.hide_viewport = state
                ob.hide_select = state
                ob.hide_render = state
            
            for coll in bpy.data.collections:
                coll.hide_viewport = state
                coll.hide_select = state
                coll.hide_render = state   

            active_layer = bpy.context.view_layer.name
            vlayer = bpy.context.scene.view_layers[active_layer]
            for ob in vlayer.objects:            
                ob.hide_set(state)
                ob.hide_viewport = state      
            
            for layer in vlayer.layer_collection.children:    
                layer.exclude = state       
                layer.hide_viewport = state                

                def follow_collection(collection):
                    for layer in collection.children: 
                        layer.exclude = state
                        layer.hide_viewport = state
                        if layer.children:
                            follow_collection(layer)
                            
                if layer.children:
                    follow_collection(layer)       
        else:
            if settings.item_excluded:
                self.exclude_viewport() 
            if settings.item_select:
                self.select_viewport() 
            if settings.item_visible:
                self.toggle_visibilty() 
            if settings.item_enabled:
                self.toggle_viewport() 
            if settings.item_rendered:
                self.render_viewport()  

        return{'FINISHED'}
    
      
    def toggle_viewport(self):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                if collection.hide_viewport:
                    collection.hide_viewport = False
                else:
                    collection.hide_viewport = True
                if prefs().debug_output:
                    print("toggle: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_viewport)

        return{'FINISHED'}

        
    def select_viewport(self):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                if collection.hide_select:
                    collection.hide_select = False
                else:                    
                    collection.hide_select = True
                if prefs().debug_output:
                    print("select: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_select)

        return{'FINISHED'}

        
    def render_viewport(self):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                if collection.hide_render:
                    collection.hide_render = False
                else:
                    collection.hide_render = True
                if prefs().debug_output:
                    print("render: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_render)

        return{'FINISHED'}


    def exclude_viewport(self):           
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):
                if ob.hide_set:                
                    ob.hide_set(False)
                else:
                    ob.hide_set(True)
                if prefs().debug_output:
                    print("hide: ", ob.name, self.button_input)  

        #toggle collections
            for layer in vlayer.layer_collection.children:    
                if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                    if layer.exclude:
                        layer.exclude = False
                    else:
                        layer.exclude = True
                    if prefs().debug_output:
                        print("exclude: ", layer.name, self.button_input)   
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input)or layer.name.endswith(self.button_input):
                                if layer.exclude:
                                    layer.exclude = False
                                else:
                                    layer.exclude = True
                            if layer.children:
                                if prefs().debug_output:
                                    print("exclude children: ", layer.children)
                                follow_collection(layer)
                    
                    follow_collection(layer)

        return{'FINISHED'}


    def toggle_visibilty(self):    
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):
                if ob.hide_set:                
                    ob.hide_set(False)
                else:
                    ob.hide_set(True)

            #toggle collections
            for layer in vlayer.layer_collection.children:           
                if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                    if layer.hide_viewport:
                        layer.hide_viewport = False
                    else:
                        layer.hide_viewport = True
                    if prefs().debug_output:
                        print("visibility: ", layer.name) 
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                                if layer.hide_viewport:
                                    layer.hide_viewport = False
                                else:
                                    layer.hide_viewport = True
                            if layer.children:
                                if prefs().debug_output:
                                    print(layer.children)
                                follow_collection(layer)                    
                    follow_collection(layer)

        return{'FINISHED'}

        
panels = (
        VIEW3D_PT_CM,
        )


def update_panel(self, context):
    message = ": Updating Panel locations has failed"
    try:
        for panel in panels:
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)

        for panel in panels:
            panel.bl_category = prefs().category
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__package__, message, e))
        pass


class CM_Preferences(AddonPreferences):
    #bl_idname = __package__
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __name__

    category: StringProperty(
            name="Tab Category",
            description="Choose a name for the category of the panel",
            default="Collection Master",
            update=update_panel
            )

    collection_prefix: StringProperty(
        name="Prefix", 
        description="collection_prefix", 
        subtype='NONE',
        default="Physics_, BL_",
        update=VIEW3D_PT_CM.draw) 
        
    collection_sufix: StringProperty(
        name="Sufix", 
        description="collection_sufix", 
        subtype='NONE',
        default="_Physics",
        update=VIEW3D_PT_CM.draw)
        
    debug_output: BoolProperty(
        name="debug_output",
        description="debug_output",
        default=False)               

    use_color: BoolProperty(
        name="use_color",
        description="change use_color",
        default=True)
        
    def list_populate(self, context):
        colors = [
            ('NONE', 'White', '', 'OUTLINER_COLLECTION', 0), 
            ('COLOR_01', 'Red','', 'COLLECTION_COLOR_01', 1), 
            ('COLOR_02', 'Orange','', 'COLLECTION_COLOR_02', 2), 
            ('COLOR_03', 'Yellow','', 'COLLECTION_COLOR_03', 3), 
            ('COLOR_04', 'Green','', 'COLLECTION_COLOR_04', 4), 
            ('COLOR_05', 'Blue','', 'COLLECTION_COLOR_05', 5), 
            ('COLOR_06', 'Purple','', 'COLLECTION_COLOR_06', 6),
            ('COLOR_07', 'Pink','', 'COLLECTION_COLOR_07', 7), 
            ('COLOR_08', 'Brown','', 'COLLECTION_COLOR_08', 8), 
            ]
        return colors

    collection_color: EnumProperty(
        items=list_populate,
        name="collection_color", 
        description="collection_color")        
    

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True 
        layout.prop(self, "category", text="Tab Name") 
        row = layout.row(align=False)
        row.prop(self, 'use_color', text="Use Collection Color") 
        row.prop(self, 'collection_color', text="") 
        layout.prop(self, 'collection_prefix')
        layout.prop(self, 'collection_sufix')
        layout.prop(self, 'debug_output') 


classes = (
    CM_PG_Settings,
    CM_OT_run,
    VIEW3D_PT_CM,
    CM_Preferences,
    )

def register():    
    [bpy.utils.register_class(c) for c in classes]
    bpy.types.Scene.CM = PointerProperty(type=CM_PG_Settings)
    update_panel(None, bpy.context)


def unregister():
    del bpy.types.Scene.CM
    [bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
    register()
