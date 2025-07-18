from OpenGL.GL import *
from OpenGL.GLU import *

class Primitives:
    _quadric = None

    @staticmethod
    def _get_quadric():
        """Cria uma instância de 'quadric' se ainda não existir."""
        if Primitives._quadric is None:
            Primitives._quadric = gluNewQuadric()
        return Primitives._quadric

    @staticmethod
    def draw_cube():
        """Desenha um cubo unitário centrado na origem com normais corretas para iluminação."""
        vertices = [
            [ 0.5,  0.5, -0.5], [-0.5,  0.5, -0.5], [-0.5, -0.5, -0.5], [ 0.5, -0.5, -0.5],
            [ 0.5,  0.5,  0.5], [-0.5,  0.5,  0.5], [-0.5, -0.5,  0.5], [ 0.5, -0.5,  0.5]
        ]
        faces = [
            (0, 1, 2, 3), (4, 5, 6, 7), (0, 3, 7, 4), 
            (1, 5, 6, 2), (0, 4, 5, 1), (3, 2, 6, 7)
        ]
        normals = [
            ( 0,  0, -1), ( 0,  0,  1), ( 1,  0,  0), 
            (-1,  0,  0), ( 0,  1,  0), ( 0, -1,  0)
        ]
        glBegin(GL_QUADS)
        for i, face in enumerate(faces):
            glNormal3fv(normals[i])
            for vertex_index in face:
                glVertex3fv(vertices[vertex_index])
        glEnd()

    @staticmethod
    def draw_cylinder(base, top, height, slices, stacks):
        """Desenha um cilindro."""
        quad = Primitives._get_quadric()
        gluCylinder(quad, base, top, height, slices, stacks)

    @staticmethod
    def draw_sphere(radius, slices, stacks):
        """Desenha uma esfera."""
        quad = Primitives._get_quadric()
        gluSphere(quad, radius, slices, stacks)