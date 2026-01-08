from abaqus import *
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup

executeOnCaeStartup()
Mdb()
model = mdb.models['Model-1']

# =========================
# Paramètres
# =========================
# Plateau plein
h_plateau = 0.6
r_plateau = 3.0

# Cône creux
h_cone = 5.0
r_ext_top_cone = 2.0
epaisseur_cone = 0.4
r_int_top_cone = r_ext_top_cone - epaisseur_cone
r_ext_bottom_cone = 3.0
r_int_bottom_cone = r_ext_bottom_cone - epaisseur_cone

# Cylindre creux au-dessus du cône
h_cyl_haut = 4.0
r_ext_cyl_haut = r_ext_top_cone      # rayon externe = haut du cône
r_int_cyl_haut = r_ext_cyl_haut - epaisseur_cone

# Hauteurs cumulées
y0 = 0.0
y1 = y0 + h_plateau
y2 = y1 + h_cone
y3 = y2 + h_cyl_haut

# =========================
# 1️⃣ Plateau plein
# =========================
model.ConstrainedSketch(name='__sketch_plateau__', sheetSize=10)
s = model.sketches['__sketch_plateau__']
s.ConstructionLine(point1=(0, -1), point2=(0, 10))
s.Line(point1=(0, y0), point2=(r_plateau, y0))
s.Line(point1=(r_plateau, y0), point2=(r_plateau, y1))
s.Line(point1=(r_plateau, y1), point2=(0, y1))
s.Line(point1=(0, y1), point2=(0, y0))

plateau = model.Part(name='Plateau', dimensionality=THREE_D, type=DEFORMABLE_BODY)
plateau.BaseSolidRevolve(angle=360.0, sketch=s)

# =========================
# 2️⃣ Cône creux
# =========================
model.ConstrainedSketch(name='__sketch_cone__', sheetSize=10)
s = model.sketches['__sketch_cone__']
s.ConstructionLine(point1=(0, -1), point2=(0, 10))

# Profil extérieur
s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_ext_top_cone, h_cone))
# Profil intérieur
s.Line(point1=(r_int_top_cone, h_cone), point2=(r_int_bottom_cone, 0))
# Fermeture haut/bas
s.Line(point1=(r_ext_top_cone, h_cone), point2=(r_int_top_cone, h_cone))   # haut
s.Line(point1=(r_ext_bottom_cone, 0), point2=(r_int_bottom_cone, 0))       # bas

cone = model.Part(name='Cone_Creux', dimensionality=THREE_D, type=DEFORMABLE_BODY)
cone.BaseSolidRevolve(angle=360.0, sketch=s)

# =========================
# 3️⃣ Cylindre creux au-dessus du cône
# =========================
model.ConstrainedSketch(name='__sketch_cyl_haut__', sheetSize=10)
s = model.sketches['__sketch_cyl_haut__']
s.ConstructionLine(point1=(0, -1), point2=(0, 10))

# Profil extérieur
s.Line(point1=(r_ext_cyl_haut, 0), point2=(r_ext_cyl_haut, h_cyl_haut))
# Profil intérieur
s.Line(point1=(r_int_cyl_haut, 0), point2=(r_int_cyl_haut, h_cyl_haut))
# Fermeture haut/bas
s.Line(point1=(r_int_cyl_haut, h_cyl_haut), point2=(r_ext_cyl_haut, h_cyl_haut))
s.Line(point1=(r_int_cyl_haut, 0), point2=(r_ext_cyl_haut, 0))

cyl_haut = model.Part(name='Cyl_Haut', dimensionality=THREE_D, type=DEFORMABLE_BODY)
cyl_haut.BaseSolidRevolve(angle=360.0, sketch=s)

# =========================
# 4️⃣ Assembly
# =========================
a = model.rootAssembly
a.DatumCsysByDefault(CARTESIAN)

# Instanciation plateau
a.Instance(name='Plateau-1', part=plateau, dependent=ON)

# Instanciation cône
a.Instance(name='Cone-1', part=cone, dependent=ON)
# Positionner juste sous le plateau
a.translate(instanceList=('Cone-1',), vector=(0.0, h_plateau, 0.0))

# Instanciation cylindre haut
a.Instance(name='Cyl_Haut-1', part=cyl_haut, dependent=ON)
# Positionner juste au-dessus du cône
a.translate(instanceList=('Cyl_Haut-1',), vector=(0.0, y2, 0.0))

print("Plateau plein + cône creux + cylindre haut creux créés et assemblés sans erreur !")
