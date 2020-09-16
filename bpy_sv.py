import bpy

# names = [
#     '1_般若波罗蜜多咒',
#     '1、如意宝轮王陀罗尼',
#     '2_雨宝咒',
#     '2、消灾吉祥神咒',
#     '3_大悲咒',
#     '3、功德宝山神咒',
#     '4_清心普善咒',
#     '4、准提神咒',
#     '5_佛顶尊胜陀罗尼咒',
#     '5、圣无量寿决定光明王陀罗尼',
#     '6_宝箧印陀罗尼咒注音',
#     '6、药师灌顶真言',
#     '7、观音灵感真言',,,,
# ]
# name = names[0]
node_textIn = bpy.data.node_groups["plan_from_wave"].nodes["Text in+.002"]
name =  node_textIn.text.split('_sp')[0]
node_textIn.autoreload = True
bpy.ops.node.sverchok_update_current(node_group="plan_from_wave")
bpy.data.node_groups["plan_from_wave"].nodes["Viewer Draw Mk3"].activate = False
# Bake wave plane, 生成 'Sv_0' 的mesh
bpy.ops.node.sverchok_mesh_baker_mk3(idname="Viewer Draw Mk3", idtree="plan_from_wave")
o_mesh = bpy.data.objects['Sv_0']
o_mesh.name = 'mesh_'+name




    

##extrude face
##------------------------
o_mesh.select_set(True)
bpy.context.view_layer.objects.active = o_mesh# Operator bpy.ops.object.editmode_toggle.poll() failed, context is incorrect
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_mode( type  = 'FACE' )
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate={"value":(0, 0, -0.04)})
# 拉平底部
bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL')
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_all(action='SELECT')
# 矫正 Normal
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.object.mode_set(mode='OBJECT')







# ## 1.sv slice
# #------------------------
# # select mesh
bpy.data.node_groups["sclice"].nodes["Objects in"].get_objects_from_scene(o_mesh)
bpy.ops.node.sverchok_update_current(node_group="sclice")
bpy.data.node_groups["sclice"].nodes["Viewer Draw Mk3"].activate = True
bpy.data.node_groups["sclice"].nodes["Viewer Draw Mk3"].activate = False
bpy.ops.node.sverchok_mesh_baker_mk3(idname="Viewer Draw Mk3", idtree="sclice")
# hide mesh
o_mesh.hide_viewport = True
o_mesh.hide_render = True

# ## copy mesh rename,"plansxxxxx"
# #-----------------------------
# copy
o_plane = bpy.data.objects['Sv_0']
o_render = o_plane.copy()
o_render.data = o_plane.data.copy()
# bpy.context.collection.objects.link(o_render)
bpy.context.scene.collection.objects.link(o_render)
o_plane.name = 'planes_'+name
o_plane.hide_viewport = True
o_plane.hide_render = True
o_render.name = 'render_'+name
# #bpy.ops.object.duplicate_move(OBJECT_OT_duplicate={"linked":False, "mode":'TRANSLATION'}, TRANSFORM_OT_translate={"value":(0, 0, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, False, False), "mirror":True, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})

# # extrude
# #------------------------
o_render.select_set(True)
bpy.context.view_layer.objects.active = o_render
bpy.ops.object.mode_set(mode='EDIT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, 0.002, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.mesh.select_all(action='SELECT')
bpy.ops.mesh.normals_make_consistent(inside=False)
bpy.ops.mesh.select_all(action='DESELECT')
bpy.ops.object.mode_set(mode='OBJECT')


# # render
# #------------------------
# name = r"1_般若波罗蜜多咒"
mat = bpy.data.materials.get("METALL")
o_render.data.materials.append(mat)

export_path = '/Users/yamlam/Documents/GitHub/spectrum/exports'

bpy.context.scene.render.film_transparent = True

bpy.context.scene.camera = bpy.context.scene.objects["CameraSide"]
bpy.context.scene.render.filepath = '%s/%s_side.png'%(export_path,name )
bpy.ops.render.render(write_still = True)

bpy.context.scene.camera = bpy.context.scene.objects["CameraFront"]
bpy.context.scene.render.filepath = '%s/%s_front.png'%(export_path,name )
bpy.ops.render.render(write_still = True)

bpy.context.scene.camera = bpy.context.scene.objects["Camera43"]
bpy.context.scene.render.filepath = '%s/%s_Side43.png'%(export_path,name )
bpy.ops.render.render(write_still = True)