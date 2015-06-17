from panda3d.bullet import BulletRigidBodyNode, BulletTriangleMesh, \
    BulletTriangleMeshShape, BulletGhostNode
from ya2.gameobject import Phys


class _Phys(Phys):
    '''This class models the physics component of a track.'''

    def __init__(self, mdt):
        Phys.__init__(self, mdt)

        def find_geoms(name):
            def sibling_names(node):
                siblings = node.getParent().getChildren()
                return [child.getName() for child in siblings]

            # the list of geoms which have siblings named 'name'
            named_geoms = [
                geom for geom in mdt.gfx.model.findAllMatches('**/+GeomNode')
                if any([s.startswith(name) for s in sibling_names(geom)])]
            in_vec = [name in named_geom.getName() for named_geom in named_geoms]
            indexes = [i for i, el in enumerate(in_vec) if el]
            return [named_geoms[i].node().getGeom(0) for i in indexes]

        for geom_name in ['Road', 'Wall']:
            geom = find_geoms(geom_name)
            if geom:
                geom = geom[0]
                mesh = BulletTriangleMesh()
                mesh.addGeom(geom)
                shape = BulletTriangleMeshShape(mesh, dynamic=False)
                np = eng.world_np.attachNewNode(BulletRigidBodyNode(geom_name))
                np.node().addShape(shape)
                eng.world_phys.attachRigidBody(np.node())
                np.node().notifyCollisions(True)

        for geom_name in ['Goal']:
            geom = find_geoms(geom_name)
            if geom:
                geom = geom[0]
                mesh = BulletTriangleMesh()
                mesh.addGeom(geom)
                shape = BulletTriangleMeshShape(mesh, dynamic=False)
                ghost = BulletGhostNode(geom_name)
                ghost.addShape(shape)
                ghostNP = eng.world_np.attachNewNode(ghost)
                eng.world_phys.attachGhost(ghost)
                ghostNP.node().notifyCollisions(True)

        for geom_name in ['Slow']:
            geoms = find_geoms(geom_name)
            for geom in geoms:
                mesh = BulletTriangleMesh()
                mesh.addGeom(geom)
                shape = BulletTriangleMeshShape(mesh, dynamic=False)
                ghost = BulletGhostNode(geom_name)
                ghost.addShape(shape)
                ghostNP = eng.world_np.attachNewNode(ghost)
                eng.world_phys.attachGhost(ghost)
                ghostNP.node().notifyCollisions(True)
