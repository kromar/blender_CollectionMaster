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
    "version": (1, 2, 9),
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
 
def find_selected():

    print("\n", bpy.context.collection.name)
    for col in bpy.context.collection.children_recursive:
        print(col.name)        
    for ob in bpy.context.collection.all_objects:
        print(ob.name) 


    for collection in bpy.data.collections:        
        print("\n", collection.name)
    for obj in collection.objects:
        print("obj: ", obj.name)    
    for obj in bpy.context.scene.collection.objects:
        print("master obj: ", obj.name)


    # Set the area to the outliner
    area = bpy.context.area
    old_type = area.type 
    area.type = 'OUTLINER'
    # some operations
    ids = bpy.context.selected_ids
    print(ids)
    # Reset the area 
    area.type = old_type   



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

        
    test_item: BoolProperty(
        name="test_item",
        description="test_item",
        default=True)


class CM_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    button_input: StringProperty()
    status: BoolProperty()

    def execute(self, context):   
        settings = context.scene.CM    
        #print("Collection Master button_input: ", self.button_input)    
        if self.button_input == 'ENABLE_ALL': 
            if prefs().debug_output:
                print('ENABLE_ALL')
            #toggle objects
            for ob in bpy.data.objects:
                if settings.item_select:
                    ob.hide_select = self.status
                if settings.item_visible:
                    ob.hide_set(self.status)
                if settings.item_enabled:
                    ob.hide_viewport = self.status                    
                if settings.item_rendered:
                    ob.hide_render = self.status
            #toggle collections
            for coll in bpy.data.collections:
                if settings.item_enabled:
                    coll.hide_viewport = self.status
                if settings.item_select:
                    coll.hide_select = self.status
                if settings.item_rendered:
                    coll.hide_render = self.status               
           
            #toggle collections
            active_layer = bpy.context.view_layer.name
            vlayer = bpy.context.scene.view_layers[active_layer]
            ##TODO: do we still need this object toggle to toggle ALL?
            """ for ob in vlayer.objects: 
                print(ob.name)           
                if settings.item_visible:
                    ob.hide_set(self.status)
                if settings.item_enabled:
                    ob.hide_viewport = self.status  """     
            
            #toggle sub collections
            for layer in vlayer.layer_collection.children:  
                if settings.item_excluded:  
                    layer.exclude = self.status       
                if settings.item_visible:
                    layer.hide_viewport = self.status                

                def follow_collection(collection):
                    for layer in collection.children: 
                        if settings.item_excluded:
                            layer.exclude = self.status
                        if settings.item_visible:
                            layer.hide_viewport = self.status
                        if layer.children:
                            follow_collection(layer)
                            
                if layer.children:
                    follow_collection(layer)   
            if self.status:
                self.status = False
            else:
                self.status = True
            
        else:
            if settings.item_excluded: #exclude
                self.toggle_exclude(self.status) 
            
            if settings.item_select: #hide_select
                self.toggle_select(self.status)  
            
            if settings.item_visible: #hide_set
                self.toggle_visibilty(self.status) 
            
            if settings.item_enabled: #hide_viewport
                self.toggle_enable(self.status)  

            if settings.item_rendered:
                self.render_viewport(self.status)  

            if self.status:
                self.status = False
            else:
                self.status = True

        return{'FINISHED'}
    
    def toggle_exclude(self, status=False):           
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]

        #toggle collections
        for layer in vlayer.layer_collection.children:    
            if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                print("exclude layer: ", layer.name, layer.exclude)
                layer.exclude = status
                if prefs().debug_output:
                    print("exclude: ", layer.name, self.button_input)   
            
            if layer.children:
                def follow_collection(collection):
                    for layer in collection.children: 
                        if layer.name.startswith(self.button_input)or layer.name.endswith(self.button_input):
                            layer.exclude = status
                        if layer.children:
                            if prefs().debug_output:
                                print("exclude children: ", layer.children)
                            follow_collection(layer)
                
                follow_collection(layer)

        return{'FINISHED'}
    
    def toggle_select(self, status=False):   
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:           
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):                                                   
                ob.hide_select = status
                if prefs().debug_output:
                    print("toggle_select: ", ob.name, self.button_input)  

        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_select = status
                if prefs().debug_output:
                    print("toggle_select: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "toggle_select: ", collection.hide_select)

        return{'FINISHED'}

    def toggle_visibilty(self, status=False): 
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]   

        #toggle obejcts        
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):
                ob.hide_set(status)
                if prefs().debug_output:
                    print("toggle_visibilty: ", ob.name, self.button_input)

        #toggle collections
        for layer in vlayer.layer_collection.children:           
            if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                layer.hide_viewport = status
                if prefs().debug_output:
                    print("toggle_visibilty: ", layer.name) 
            
            if layer.children:
                def follow_collection(collection):
                    for layer in collection.children: 
                        if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                            layer.hide_viewport = status
                        if layer.children:
                            if prefs().debug_output:
                                print(layer.children)
                            follow_collection(layer)                    
                follow_collection(layer)

        return{'FINISHED'}
      
    def toggle_enable(self, status=False):   
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
               
        #toggle obejcts
        for ob in vlayer.objects:           
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):                                                   
                ob.hide_viewport = status
                if prefs().debug_output:
                    print("toggle_enable: ", ob.name, self.button_input)

        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_viewport = status
                if prefs().debug_output:
                    print("toggle_enable: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "toggle_enable: ", collection.hide_viewport)

        return{'FINISHED'}
       
    def render_viewport(self, status=False):   
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
             
        #toggle obejcts
        for ob in vlayer.objects:           
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):                                                   
                ob.hide_render = status
                if prefs().debug_output:
                    print("render_viewport: ", ob.name, self.button_input)

        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_render = status
                if prefs().debug_output:
                    print("render_viewport: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_render)

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
