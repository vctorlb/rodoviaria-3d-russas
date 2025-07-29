from OpenGL.GL import *
import os

class Goal:
    def __init__(self, position, rotation_y=0, obj_path=None):
        if obj_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(os.path.dirname(current_dir))
            obj_path = os.path.join(project_root, "src", "obj", "Soccergoal.obj")
        self.position = position
        self.rotation_y = rotation_y
        self.vertices, self.textures, self.normals, self.faces = self.load_obj(obj_path)

    def load_obj(self, filename):
        vertices = []
        textures = []
        normals = []
        faces = []

        with open(filename, 'r') as file:
            for line in file:
                if line.startswith('v '):  # vértice
                    parts = line.split()
                    vertex = list(map(float, parts[1:4]))
                    vertices.append(vertex)
                elif line.startswith('vt '):  # textura
                    parts = line.split()
                    texture = list(map(float, parts[1:3]))
                    textures.append(texture)
                elif line.startswith('vn '):  # normal
                    parts = line.split()
                    normal = list(map(float, parts[1:4]))
                    normals.append(normal)
                elif line.startswith('f '):  # face
                    parts = line.split()
                    face = []
                    for part in parts[1:]:
                        vals = part.split('/')
                        v_idx = int(vals[0]) - 1
                        t_idx = int(vals[1]) - 1 if len(vals) > 1 and vals[1] else None
                        n_idx = int(vals[2]) - 1 if len(vals) > 2 and vals[2] else None
                        face.append((v_idx, t_idx, n_idx))
                    faces.append(face)

        return vertices, textures, normals, faces

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.position)
        glRotatef(90, 0, 1, 0)

        glColor3f(1.0, 1.0, 1.0)  # cor branca para a trave

        for face in self.faces:
            if len(face) == 3:
                glBegin(GL_TRIANGLES)
            else:
                glBegin(GL_POLYGON)
            
            for vertex, _, normal in face:
                glVertex3f(*self.vertices[vertex])
            
            glEnd()


        glPopMatrix()
