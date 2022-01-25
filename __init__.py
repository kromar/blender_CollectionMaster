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
    "version": (1, 2, 7),
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
 

class VIEW3D_PT_CollectionMaster(Panel):    
    bl_label = 'Collection Master'
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Collection Master'

           
    def draw(self, context):             
        layout = self.layout  
        column = layout.column(align=True)   
        #main
        column.label(text="Restore")
        row = column.row(align=True)
        row.operator(operator="scene.collection_master", text="All", emboss=True, depress=False).button_input='ENABLE_ALL' 
        row.operator(operator="scene.collection_master", text="", icon='CHECKBOX_HLT').item_excluded
        row.operator(operator="scene.collection_master", text="", icon='RESTRICT_SELECT_OFF').item_select
        row.operator(operator="scene.collection_master", text="", icon='HIDE_OFF').item_visible
        row.operator(operator="scene.collection_master", text="", icon='RESTRICT_VIEW_OFF').item_enabled
        row.operator(operator="scene.collection_master", text="", icon='RESTRICT_RENDER_OFF').item_rendered
                
        
        
        #prefix
        column.label(text="Prefix")        
        for i in prefs().collection_prefix.replace(",", " ").split():            
            row = column.row(align=True)
            if not prefs().collection_color == 'NONE':            
                row.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
                
                row.operator(operator="scene.collection_master", text="", icon='CHECKBOX_HLT').item_excluded
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_SELECT_OFF').item_select
                row.operator(operator="scene.collection_master", text="", icon='HIDE_OFF').item_visible
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_VIEW_OFF').item_enabled
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_RENDER_OFF').item_rendered
            else:    
                row.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i
                
                row.operator(operator="scene.collection_master", text="", icon='CHECKBOX_HLT').item_excluded
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_SELECT_OFF').item_select
                row.operator(operator="scene.collection_master", text="", icon='HIDE_OFF').item_visible
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_VIEW_OFF').item_enabled
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_RENDER_OFF').item_rendered
        
        
        #sufix
        column.label(text="Suffix")
        for i in prefs().collection_sufix.replace(",", " ").split():            
            row = column.row(align=True)
            if not prefs().collection_color == 'NONE':            
                row.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
                
                row.operator(operator="scene.collection_master", text="", icon='CHECKBOX_HLT').item_excluded
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_SELECT_OFF').item_select
                row.operator(operator="scene.collection_master", text="", icon='HIDE_OFF').item_visible
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_VIEW_OFF').item_enabled
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_RENDER_OFF').item_rendered
            else:    
                row.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i
                
                row.operator(operator="scene.collection_master", text="", icon='CHECKBOX_HLT').item_excluded
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_SELECT_OFF').item_select
                row.operator(operator="scene.collection_master", text="", icon='HIDE_OFF').item_visible
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_VIEW_OFF').item_enabled
                row.operator(operator="scene.collection_master", text="", icon='RESTRICT_RENDER_OFF').item_rendered



class CollectionMaster_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    
    button_input: StringProperty()

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


    def execute(self, context):        
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
            if prefs().disable_in_viewport:
                if self.item_enabled:
                    self.item_enabled = False
                else:
                    self.item_enabled = True  
                self.toggle_viewport(self.item_enabled)
                
            if prefs().render_in_viewport:
                if self.item_rendered:
                    self.item_rendered = False
                else:
                    self.item_rendered = True  
                self.render_viewport(self.item_rendered)    
            
            if prefs().select_in_viewport:
                if self.item_select:
                    self.item_select = False
                else:
                    self.item_select = True  
                self.select_viewport(self.item_select)    

            if prefs().hide_in_viewport:
                if self.item_visible:
                    self.item_visible = False
                else:
                    self.item_visible = True  
                self.toggle_visibilty(self.item_visible)  
            
            if prefs().exclude_in_viewport:
                if self.item_excluded:
                    self.item_excluded = False
                else:
                    self.item_excluded = True  
                self.exclude_viewport(self.item_excluded)    

        return{'FINISHED'}
    
      
    def toggle_viewport(self, state=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_viewport = state
                if prefs().debug_output:
                    print("toggle: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_viewport)

        return{'FINISHED'}

        
    def select_viewport(self, state=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_select = state
                if prefs().debug_output:
                    print("select: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_select)

        return{'FINISHED'}

        
    def render_viewport(self, state=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input) or collection.name.endswith(self.button_input):
                collection.hide_render = state
                if prefs().debug_output:
                    print("render: ", collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                if prefs().debug_output:
                    print("Collection: ", collection.name, "Hide: ", collection.hide_render)

        return{'FINISHED'}


    def exclude_viewport(self, state=False):           
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        print("exclude state:", state)
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):
                ob.hide_set(state)
                if prefs().debug_output:
                    print("hide: ", ob.name, self.button_input)  

        #toggle collections
            for layer in vlayer.layer_collection.children:    
                if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                    layer.exclude = state
                    if prefs().debug_output:
                        print("exclude: ", layer.name, self.button_input)   
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input)or layer.name.endswith(self.button_input):
                                layer.exclude = state
                            if layer.children:
                                if prefs().debug_output:
                                    print("exclude children: ", layer.children)
                                follow_collection(layer)
                    
                    follow_collection(layer)


        return{'FINISHED'}


    def toggle_visibilty(self, state=False):    
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input) or ob.name.endswith(self.button_input):
                ob.hide_set(state)

        #toggle collections
            for layer in vlayer.layer_collection.children:           
                if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                    layer.hide_viewport = state
                    if prefs().debug_output:
                        print("visibility: ", layer.name) 
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input) or layer.name.endswith(self.button_input):
                                layer.hide_viewport = state
                            if layer.children:
                                if prefs().debug_output:
                                    print(layer.children)
                                follow_collection(layer)                    
                    follow_collection(layer)

        return{'FINISHED'}

        
panels = (
        VIEW3D_PT_CollectionMaster,
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


class CollectionMasterPreferences(AddonPreferences):
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
        update=VIEW3D_PT_CollectionMaster.draw) 
        
    collection_sufix: StringProperty(
        name="Sufix", 
        description="collection_sufix", 
        subtype='NONE',
        default="_Physics",
        update=VIEW3D_PT_CollectionMaster.draw)
        
    debug_output: BoolProperty(
        name="debug_output",
        description="debug_output",
        default=False)
        
    toggle_text: BoolProperty(
        name="toggle_text",
        description="toggle_text",
        default=False)

    use_color: BoolProperty(
        name="use_color",
        description="change use_color",
        default=True)



    disable_in_viewport: BoolProperty(
        name="disable_in_viewport",
        description="disable_in_viewport",
        default=False)
        
    select_in_viewport: BoolProperty(
        name="select_in_viewport",
        description="select_in_viewport",
        default=False)

    render_in_viewport: BoolProperty(
        name="render_in_viewport",
        description="render_in_viewport",
        default=False)
        
    hide_in_viewport: BoolProperty(
        name="hide_in_viewport",
        description="hide_in_viewport",
        default=True)        
        
    exclude_in_viewport: BoolProperty(
        name="exclude_in_viewport",
        description="exclude_in_viewport",
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
        layout.use_property_split = False 
        row = layout.row(align=True)
        if self.toggle_text:            
            if self.exclude_in_viewport:
                row.prop(self, 'exclude_in_viewport', icon="CHECKBOX_HLT")
            else: 
                row.prop(self, 'exclude_in_viewport', icon="CHECKBOX_DEHLT")

            if self.select_in_viewport:
                row.prop(self, 'select_in_viewport', icon='RESTRICT_SELECT_OFF')
            else: 
                row.prop(self, 'select_in_viewport', icon='RESTRICT_SELECT_ON')
                
            if self.hide_in_viewport:
                row.prop(self, 'hide_in_viewport', icon='HIDE_OFF')
            else:            
                row.prop(self, 'hide_in_viewport', icon='HIDE_ON')

            if self.disable_in_viewport:
                row.prop(self, 'disable_in_viewport', icon='RESTRICT_VIEW_OFF')
            else:
                row.prop(self, 'disable_in_viewport', icon='RESTRICT_VIEW_ON')

            if self.render_in_viewport:
                row.prop(self, 'render_in_viewport', icon='RESTRICT_RENDER_OFF')
            else:            
                row.prop(self, 'render_in_viewport', icon='RESTRICT_RENDER_ON')
        
        else:    
            if self.exclude_in_viewport:
                row.prop(self, 'exclude_in_viewport', text='', icon="CHECKBOX_HLT")
            else: 
                row.prop(self, 'exclude_in_viewport',  text='', icon="CHECKBOX_DEHLT")

            if self.select_in_viewport:
                row.prop(self, 'select_in_viewport',  text='', icon='RESTRICT_SELECT_OFF')
            else: 
                row.prop(self, 'select_in_viewport',  text='', icon='RESTRICT_SELECT_ON')
                
            if self.hide_in_viewport:
                row.prop(self, 'hide_in_viewport',  text='', icon='HIDE_OFF')
            else:            
                row.prop(self, 'hide_in_viewport',  text='', icon='HIDE_ON')

            if self.disable_in_viewport:
                row.prop(self, 'disable_in_viewport',  text='', icon='RESTRICT_VIEW_OFF')
            else:
                row.prop(self, 'disable_in_viewport', text='',  icon='RESTRICT_VIEW_ON')

            if self.render_in_viewport:
                row.prop(self, 'render_in_viewport',  text='', icon='RESTRICT_RENDER_OFF')
            else:            
                row.prop(self, 'render_in_viewport',  text='', icon='RESTRICT_RENDER_ON')
            
        layout.prop(self, 'toggle_text')

        layout.prop(self, 'use_color') 
        layout.prop(self, 'collection_color') 
        layout.prop(self, 'collection_prefix')
        layout.prop(self, 'collection_sufix')
        layout.prop(self, "category", text="Tab Category")      
        
        layout.prop(self, 'debug_output') 


classes = (
    CollectionMaster_OT_run,
    VIEW3D_PT_CollectionMaster,
    CollectionMasterPreferences,
    )

def register():    
    [bpy.utils.register_class(c) for c in classes]
    update_panel(None, bpy.context)


def unregister():
    [bpy.utils.unregister_class(c) for c in classes]

if __name__ == "__main__":
    register()
