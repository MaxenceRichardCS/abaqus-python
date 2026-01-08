from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

executeOnCaeStartup()
Mdb()
model = mdb.models['Model-1']

# =============================================================================
# 1️⃣ Parameter dictionary
# =============================================================================
params = {
    # Plateau (solid)
    'plateau_radius': 15.5,        # [m] radius of the solid plateau
    'plateau_height': 1.7,        # [m] height of the plateau

    # Cone (hollow)
    'cone_height': 25.34,           # [m] height of the hollow cone
    'cone_top_outer_radius': 3.5, # [m] top external radius of the cone
    'cone_bottom_outer_radius': 10, # [m] bottom external radius of the cone
    'cone_thickness': 0.5,        # [m] thickness of the cone shell

    # Cylinder above cone (hollow)
    'cyl_height': 18.0,            # [m] height of the cylinder above the cone
}

# =============================================================================
# 2️⃣ Parameter checks
# =============================================================================
def check_parameters(params):
    if params['cone_thickness'] <= 0:
        raise ValueError("Cone thickness must be positive.")
    if params['cone_top_outer_radius'] <= 0:
        raise ValueError("Cone top outer radius must be positive.")
    if params['cone_bottom_outer_radius'] <= params['cone_thickness']:
        raise ValueError("Cone bottom radius must be larger than thickness.")
    if params['plateau_radius'] <= 0 or params['plateau_height'] <= 0:
        raise ValueError("Plateau dimensions must be positive.")
    if params['cyl_height'] <= 0:
        raise ValueError("Cylinder height must be positive.")

check_parameters(params)

# =============================================================================
# 3️⃣ Function to create GBS fused
# =============================================================================
def create_fused_gbs(model, params):
    """
    Create a GBS assembly with:
        1. Solid plateau
        2. Hollow cone
        3. Hollow cylinder above the cone
    Then fuse all parts into a single solid.
    """
    # Extract parameters
    h_plateau = params['plateau_height']
    r_plateau = params['plateau_radius']
    
    h_cone = params['cone_height']
    r_ext_top_cone = params['cone_top_outer_radius']
    r_ext_bottom_cone = params['cone_bottom_outer_radius']
    t_cone = params['cone_thickness']
    r_int_top_cone = r_ext_top_cone - t_cone
    r_int_bottom_cone = r_ext_bottom_cone - t_cone

    h_cyl = params['cyl_height']
    r_ext_cyl_top = r_ext_top_cone
    r_int_cyl_top = r_ext_cyl_top - t_cone

    # Cumulative heights
    y0 = 0.0
    y1 = y0 + h_plateau
    y2 = y1 + h_cone
    y3 = y2 + h_cyl

    # ----------------------------
    # 1️⃣ Plateau (solid)
    # ----------------------------
    model.ConstrainedSketch(name='__sketch_plateau__', sheetSize=10)
    s = model.sketches['__sketch_plateau__']
    s.ConstructionLine(point1=(0, -1), point2=(0, 10))
    s.Line(point1=(0, y0), point2=(r_plateau, y0))
    s.Line(point1=(r_plateau, y0), point2=(r_plateau, y1))
    s.Line(point1=(r_plateau, y1), point2=(0, y1))
    s.Line(point1=(0, y1), point2=(0, y0))
    plateau = model.Part(name='Plateau', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    plateau.BaseSolidRevolve(angle=360.0, sketch=s)

    # ----------------------------
    # 2️⃣ Hollow cone
    # ----------------------------
    model.ConstrainedSketch(name='__sketch_cone__', sheetSize=10)
    s = model.sketches['__sketch_cone__']
    s.ConstructionLine(point1=(0, -1), point2=(0, 10))
    # Outer contour
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_ext_top_cone, h_cone))
    # Inner contour
    s.Line(point1=(r_int_top_cone, h_cone), point2=(r_int_bottom_cone, 0))
    # Closing lines
    s.Line(point1=(r_ext_top_cone, h_cone), point2=(r_int_top_cone, h_cone))
    s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_int_bottom_cone, 0))
    cone = model.Part(name='Cone_Creux', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cone.BaseSolidRevolve(angle=360.0, sketch=s)

    # ----------------------------
    # 3️⃣ Hollow cylinder above cone
    # ----------------------------
    model.ConstrainedSketch(name='__sketch_cyl__', sheetSize=10)
    s = model.sketches['__sketch_cyl__']
    s.ConstructionLine(point1=(0, -1), point2=(0, 10))
    # Outer
    s.Line(point1=(r_ext_cyl_top, 0), point2=(r_ext_cyl_top, h_cyl))
    # Inner
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_int_cyl_top, h_cyl))
    # Closing
    s.Line(point1=(r_int_cyl_top, h_cyl), point2=(r_ext_cyl_top, h_cyl))
    s.Line(point1=(r_int_cyl_top, 0), point2=(r_ext_cyl_top, 0))
    cyl_top = model.Part(name='Cyl_Haut', dimensionality=THREE_D, type=DEFORMABLE_BODY)
    cyl_top.BaseSolidRevolve(angle=360.0, sketch=s)

    # ----------------------------
    # 4️⃣ Assembly
    # ----------------------------
    a = model.rootAssembly
    a.DatumCsysByDefault(CARTESIAN)

    # Plateau
    a.Instance(name='Plateau-1', part=plateau, dependent=ON)
    # Cone
    a.Instance(name='Cone-1', part=cone, dependent=ON)
    a.translate(instanceList=('Cone-1',), vector=(0.0, h_plateau, 0.0))
    # Cylinder above cone
    a.Instance(name='Cyl_Haut-1', part=cyl_top, dependent=ON)
    a.translate(instanceList=('Cyl_Haut-1',), vector=(0.0, y2, 0.0))

    # ----------------------------
    # 5️⃣ Merge parts into single solid
    # ----------------------------
    merged_part = a.InstanceFromBooleanMerge(
        name='GBS_Fused',
        instances=(a.instances['Plateau-1'], a.instances['Cone-1'], a.instances['Cyl_Haut-1']),
        keepIntersections=True,
        originalInstances=SUPPRESS,
        domain=GEOMETRY
    )

    del model.parts['Plateau']
    del model.parts['Cone_Creux']
    del model.parts['Cyl_Haut']



create_fused_gbs(model, params)
