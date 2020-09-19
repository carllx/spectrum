# 使用 terminal 启动获得debug 的log
#  /Applications/Blender.app/Contents/MacOS/Blender


import bpy
fnames = [
    '1、如意宝轮王陀罗尼_splitRows10.json', # 0
    '2_雨宝咒_splitRows60.json', # 1
    '2、消灾吉祥神咒_splitRows7.json', # 2
    '1_般若波罗蜜多咒_splitRows38.json', # 3
    '3_大悲咒_splitRows85.json', # 4
    '4_清心普善咒_splitRows129.json', # 5
    '5_佛顶尊胜陀罗尼咒_splitRows35.json', # 6
    '6_宝箧印陀罗尼咒注音_splitRows38.json', # 7
]
# will_VoicePlan =True
# will_ExtrudeMesh =True
mesh_height = -0.06
plane_thickness = 0.002
slice_num = 49
o_mesh = None
o_plane = None
o_render = None
name = ''

for i, fname in enumerate(fnames):
    
    
    

    # Generate Voice Plane
    #------------
    node_textIn = bpy.data.node_groups["1_voice_plane"].nodes["Text in+.002"]
    node_textIn.file_pointer = bpy.data.texts[fnames[i]]
    name =  node_textIn.text.split('_sp')[0]
    node_textIn.autoreload = True
    bpy.ops.node.sverchok_update_current(node_group="1_voice_plane")
    bpy.data.node_groups["1_voice_plane"].nodes["Viewer Draw Mk3"].activate = False
    # Bake -- wave plane, 生成 'Sv_0' 的mesh
    bpy.ops.node.sverchok_mesh_baker_mk3(idname="Viewer Draw Mk3", idtree="1_voice_plane")
    o_mesh = bpy.data.objects['Sv_0']
    o_mesh.name = 'mesh_'+name
    





    ## Extrude Mesh (ops)
    ##------------------------
    o_mesh.select_set(True)
    bpy.context.view_layer.objects.active = o_mesh# Operator bpy.ops.object.editmode_toggle.poll() failed, context is incorrect
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_mode( type  = 'FACE' )
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move( TRANSFORM_OT_translate={"value":(0, 0, mesh_height)})
    # 拉平底部
    bpy.ops.transform.resize(value=(1, 1, 0), orient_type='GLOBAL')
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='SELECT')
    # 矫正 Normal
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.object.mode_set(mode='OBJECT')



    ## ## Slice plane to Mesh (sv)
    ## #------------------------
    ## # select mesh
    sv_sketch = bpy.data.node_groups["2_sclice"]
    sv_sketch.nodes["Objects in"].get_objects_from_scene(o_mesh)
    bpy.ops.node.sverchok_update_current(node_group="2_sclice")
    sv_sketch.nodes["Viewer Draw Mk3"].activate = False
    if sv_sketch.nodes["Line.001"].num != slice_num:
        sv_sketch.nodes["Line.001"].num = slice_num

    bpy.ops.node.sverchok_mesh_baker_mk3(idname="Viewer Draw Mk3", idtree="2_sclice")
    # hide mesh
    o_mesh.hide_viewport = True
    o_mesh.hide_render = True
    # copy mesh rename,"plansxxxxx"  -- name
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

    # # extrude for rendering
    # #------------------------
    o_render.select_set(True)
    bpy.context.view_layer.objects.active = o_render
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.extrude_region_move(MESH_OT_extrude_region={"use_normal_flip":False, "mirror":False}, TRANSFORM_OT_translate={"value":(0, plane_thickness, 0), "orient_type":'GLOBAL', "orient_matrix":((1, 0, 0), (0, 1, 0), (0, 0, 1)), "orient_matrix_type":'GLOBAL', "constraint_axis":(False, True, False), "mirror":False, "use_proportional_edit":False, "proportional_edit_falloff":'SMOOTH', "proportional_size":1, "use_proportional_connected":False, "use_proportional_projected":False, "snap":False, "snap_target":'CLOSEST', "snap_point":(0, 0, 0), "snap_align":False, "snap_normal":(0, 0, 0), "gpencil_strokes":False, "cursor_transform":False, "texture_space":False, "remove_on_cancel":False, "release_confirm":False, "use_accurate":False})
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.mesh.select_all(action='SELECT')
    bpy.ops.mesh.normals_make_consistent(inside=False)
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.mode_set(mode='OBJECT')
    

    # # rendering
    # #------------------------
    mat = bpy.data.materials.get("METALL")
    o_render.data.materials.append(mat)

    export_path = '/Users/yamlam/Documents/GitHub/spectrum/exports'

    bpy.context.scene.render.film_transparent = True

    bpy.context.scene.camera = bpy.context.scene.objects["CameraSide"]
    bpy.context.scene.render.filepath = '%s/%s-s%d-Side99.png'%(export_path,name,slice_num )
    bpy.ops.render.render(write_still = True)

    bpy.context.scene.camera = bpy.context.scene.objects["CameraFront"]
    bpy.context.scene.render.filepath = '%s/%s-s%d-Front.png'%(export_path,name,slice_num )
    bpy.ops.render.render(write_still = True)

    bpy.context.scene.camera = bpy.context.scene.objects["Camera43"]
    bpy.context.scene.render.filepath = '%s/%s-s%d-Side43.png'%(export_path,name,slice_num )
    bpy.ops.render.render(write_still = True)

    o_plane.hide_viewport = True
    o_plane.hide_render = True


    # # clean
    # #------------------------
    objs = bpy.data.objects
    objs.remove(o_mesh, do_unlink=True)
    objs.remove(o_render, do_unlink=True)
    
    ## export
    o_plane.select_set(True)
    bpy.data.objects['Text'].select_set(True)
    target_file = '%s/%s-s%d.obj'%(export_path,name,slice_num )
    bpy.ops.export_scene.obj(
        filepath=target_file,
        check_existing=True,
        axis_forward='-Z',
        axis_up='Y',
        filter_glob="*.obj;*.mtl",
        use_selection=True,
        use_animation=False,
        use_mesh_modifiers=True,
        use_edges=True,
        use_smooth_groups=False,
        use_smooth_groups_bitflags=False,
        use_normals=True,
        use_uvs=True,
        use_materials=True,
        use_triangles=False,
        use_nurbs=False,
        use_vertex_groups=False,
        use_blen_objects=True,
        group_by_object=False,
        group_by_material=False,
        keep_vertex_order=False,
        global_scale=1,
        path_mode='AUTO'
     )
    o_plane.select_set(False)
    bpy.data.objects['Text'].select_set(False)

