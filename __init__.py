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
    "version": (1, 2, 4),
    "blender": (2, 83, 0),
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
        for i in prefs().collection_prefix.replace(",", " ").split():
            if not prefs().collection_color == 'NONE':            
                layout.operator(operator="scene.collection_master", text=i, icon='COLLECTION_' + prefs().collection_color, emboss=True, depress=False).button_input=i
            else:    
                layout.operator(operator="scene.collection_master", text=i, icon='OUTLINER_COLLECTION', emboss=True, depress=False).button_input=i


class CollectionMaster_OT_run(Operator):
    bl_idname = "scene.collection_master"
    bl_label = "collection_master"
    bl_description = "toggle visibility of physics collections"
    
    button_input: StringProperty()
        
    item_enabled: BoolProperty(
        name="collection_enabled",
        description="collection_enabled",
        default=False)

    item_rendered: BoolProperty(
        name="collection_rendered",
        description="collection_rendered",
        default=False)

    item_select: BoolProperty(
        name="collection_select",
        description="collection_select",
        default=False)

    item_visible: BoolProperty(
        name="collection_visible",
        description="collection_visible",
        default=False)
        
    item_excluded: BoolProperty(
        name="collection_excluded",
        description="collection_excluded",
        default=False)

    def execute(self, context):        
        #print("Collection Master button_input: ", self.button_input)            
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
            if collection.name.startswith(self.button_input):
                collection.hide_viewport = state
                print(collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                print("Collection: ", collection.name, "Hide: ", collection.hide_viewport)

        return{'FINISHED'}

        
    def select_viewport(self, state=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input):
                collection.hide_select = state
                print(collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                print("Collection: ", collection.name, "Hide: ", collection.hide_select)

        return{'FINISHED'}

        
    def render_viewport(self, state=False):        
        for collection in bpy.data.collections:  
            if collection.name.startswith(self.button_input):
                collection.hide_render = state
                print(collection.name)
                
                #change collection icon color
                if prefs().use_color and prefs().collection_color:
                    collection.color_tag = prefs().collection_color                
                print("Collection: ", collection.name, "Hide: ", collection.hide_render)

        return{'FINISHED'}


    def exclude_viewport(self, state=False):           
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input):
                ob.hide_set(state)

        #toggle collections
            for layer in vlayer.layer_collection.children:  
                print(layer.name)          
                if layer.name.startswith(self.button_input):
                    layer.exclude = state
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input):
                                layer.exclude = state
                            if layer.children:
                                print(layer.children)
                                follow_collection(layer)

        return{'FINISHED'}


    def toggle_visibilty(self, state=False):    
        active_layer = bpy.context.view_layer.name
        vlayer = bpy.context.scene.view_layers[active_layer]
        
        #toggle obejcts
        for ob in vlayer.objects:            
            if ob.name.startswith(self.button_input):
                ob.hide_set(state)

        #toggle collections
            for layer in vlayer.layer_collection.children:  
                print(layer.name)          
                if layer.name.startswith(self.button_input):
                    layer.hide_viewport = state
                
                if layer.children:
                    def follow_collection(collection):
                        for layer in collection.children: 
                            if layer.name.startswith(self.button_input):
                                layer.hide_viewport = state
                            if layer.children:
                                print(layer.children)
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
        name="collection_prefix", 
        description="collection_prefix", 
        subtype='NONE',
        default="Physics_, BL_",
        update=VIEW3D_PT_CollectionMaster.draw) 
        
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
        layout.use_property_split = True 
        layout.prop(self, 'disable_in_viewport')
        layout.prop(self, 'hide_in_viewport')
        layout.prop(self, 'select_in_viewport')
        layout.prop(self, 'exclude_in_viewport')
        layout.prop(self, 'render_in_viewport')
        layout.prop(self, 'use_color') 
        layout.prop(self, 'collection_color') 
        layout.prop(self, 'collection_prefix')
        layout.prop(self, "category", text="Tab Category")        


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
