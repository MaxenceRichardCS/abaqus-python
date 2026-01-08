from abaqus import mdb
from abaqusConstants import *
from caeModules import *
from driverUtils import executeOnCaeStartup


## Améliorer la taille du seed part 

def MeshGBS():
    p = mdb.models['Model-1'].parts['GBS_Fused']
    p.seedPart(size=2.2)
    p.setMeshControls(regions=p.cells, elemShape=TET, technique=FREE)
    p.setElementType(regions=(p.cells,),
                    elemTypes=(mesh.ElemType(C3D20R),
                                mesh.ElemType(C3D15),
                                mesh.ElemType(C3D10)))
    p.generateMesh()

def MeshTower():

    p = mdb.models['Model-1'].parts['Tower']

    p.seedPart(size=2.5, deviationFactor=0.1, minSizeFactor=0.1)

    p.setMeshControls(
        regions=p.cells,
        elemShape=HEX,
        technique=SWEEP
    )

    elemType1 = mesh.ElemType(elemCode=C3D8R)    # linéaire
    elemType2 = mesh.ElemType(elemCode=C3D20R)   # quadratique

    p.setElementType(
        regions=(p.cells,),
        elemTypes=(elemType1, elemType2)
    )

    p.generateMesh()


