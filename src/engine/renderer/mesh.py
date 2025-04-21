import ctypes
import re
import numpy as np

from OpenGL.GL import *

class VertexArray:
    def __init__(self, vertices, normals=True, texcoords=True):
        self.length = len(vertices)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        stride = 3

        if normals:
            stride += 3

        if texcoords:
            stride += 2

        stride = stride * ctypes.sizeof(ctypes.c_float)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))

        if normals:
            glEnableVertexAttribArray(1)
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))

        if texcoords:
            glEnableVertexAttribArray(2)
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))

        glBindVertexArray(0)

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

    def __len__(self):
        return self.length

    def destroy(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])


class ElementBuffer:
    def __init__(self, vertex_array, indices):
        self.length = len(indices)

        self.ebo = glGenBuffers(1)

        vertex_array.bind()

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        vertex_array.unbind()

    def __len__(self):
        return self.length

    def destroy(self):
        glDeleteBuffers(1, [self.ebo])


class TriangleMesh:
    def __init__(self):
        self.vertices =  np.array([
            0.0,  0.5, 0.0,  # Top
            -0.5, -0.5, 0.0,  # Bottom Left
            0.5, -0.5, 0.0   # Bottom Right
        ], dtype=np.float32)

        self.vertex_array = VertexArray(self.vertices, False, False)

    def draw(self):
        self.vertex_array.bind()
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_array))
        self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()


class PlaneMesh:
    def __init__(self):
        self.vertices = np.array([
            # Position           # Normal         # TexCoord
            -0.5, 0.0, -0.5,      0.0, 1.0, 0.0,    0.0, 0.0,  # Bottom-left
            0.5, 0.0, -0.5,      0.0, 1.0, 0.0,    1.0, 0.0,  # Bottom-right
            0.5, 0.0,  0.5,      0.0, 1.0, 0.0,    1.0, 1.0,  # Top-right
            -0.5, 0.0,  0.5,      0.0, 1.0, 0.0,    0.0, 1.0   # Top-left
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 3,  # first triangle
            1, 2, 3   # second triangle
        ], dtype=np.uint32)

        self.vertex_array = VertexArray(self.vertices)
        self.mesh = ElementBuffer(self.vertex_array, self.indices)

    def draw(self):
        self.vertex_array.bind()
        glDrawElements(GL_TRIANGLES, len(self.mesh), GL_UNSIGNED_INT, None)
        self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()
        self.mesh.destroy()


class CubeMesh:
    def __init__(self):
        self.vertices = np.array([
            # Position           # Normal            # TexCoords

            # Back face
            -0.5, -0.5, -0.5,     0.0,  0.0, -1.0,     0.0, 0.0,
            0.5, -0.5, -0.5,     0.0,  0.0, -1.0,     1.0, 0.0,
            0.5,  0.5, -0.5,     0.0,  0.0, -1.0,     1.0, 1.0,
            -0.5,  0.5, -0.5,     0.0,  0.0, -1.0,     0.0, 1.0,

            # Front face
            -0.5, -0.5,  0.5,     0.0,  0.0,  1.0,     0.0, 0.0,
            0.5, -0.5,  0.5,     0.0,  0.0,  1.0,     1.0, 0.0,
            0.5,  0.5,  0.5,     0.0,  0.0,  1.0,     1.0, 1.0,
            -0.5,  0.5,  0.5,     0.0,  0.0,  1.0,     0.0, 1.0,

            # Left face
            -0.5, -0.5, -0.5,    -1.0,  0.0,  0.0,     0.0, 0.0,
            -0.5, -0.5,  0.5,    -1.0,  0.0,  0.0,     1.0, 0.0,
            -0.5,  0.5,  0.5,    -1.0,  0.0,  0.0,     1.0, 1.0,
            -0.5,  0.5, -0.5,    -1.0,  0.0,  0.0,     0.0, 1.0,

            # Right face
            0.5, -0.5, -0.5,     1.0,  0.0,  0.0,     0.0, 0.0,
            0.5, -0.5,  0.5,     1.0,  0.0,  0.0,     1.0, 0.0,
            0.5,  0.5,  0.5,     1.0,  0.0,  0.0,     1.0, 1.0,
            0.5,  0.5, -0.5,     1.0,  0.0,  0.0,     0.0, 1.0,

            # Bottom face
            -0.5, -0.5, -0.5,     0.0, -1.0,  0.0,     0.0, 0.0,
            0.5, -0.5, -0.5,     0.0, -1.0,  0.0,     1.0, 0.0,
            0.5, -0.5,  0.5,     0.0, -1.0,  0.0,     1.0, 1.0,
            -0.5, -0.5,  0.5,     0.0, -1.0,  0.0,     0.0, 1.0,

            # Top face
            -0.5,  0.5, -0.5,     0.0,  1.0,  0.0,     0.0, 0.0,
            0.5,  0.5, -0.5,     0.0,  1.0,  0.0,     1.0, 0.0,
            0.5,  0.5,  0.5,     0.0,  1.0,  0.0,     1.0, 1.0,
            -0.5,  0.5,  0.5,     0.0,  1.0,  0.0,     0.0, 1.0,
        ], dtype=np.float32)

        self.indices = np.array([
            # Back face
            0, 1, 2,
            2, 3, 0,

            # Front face
            4, 5, 6,
            6, 7, 4,

            # Left face
            0, 4, 7,
            7, 3, 0,

            # Right face
            1, 5, 6,
            6, 2, 1,

            # Bottom face
            0, 1, 5,
            5, 4, 0,

            # Top face
            3, 2, 6,
            6, 7, 3
        ], dtype=np.uint32)

        self.vertex_array = VertexArray(self.vertices)
        self.mesh = ElementBuffer(self.vertex_array, self.indices)

    def draw(self):
        self.vertex_array.bind()
        glDrawElements(GL_TRIANGLES, len(self.mesh), GL_UNSIGNED_INT, None)
        self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()
        self.mesh.destroy()


class CustomMesh:
    def __init__(self, file):
        with open(file) as f:
            vertex_count = int(f.readline().strip())
            vertex_stride = 8
            vertices = np.empty(vertex_count * vertex_stride, dtype=np.float32)
            for i in range(0, vertex_count * vertex_stride, vertex_stride):
                x, y, z, nx, ny, nz, u, v = map(float, f.readline().strip().split())
                vertices[i] = x
                vertices[i+1] = y
                vertices[i+2] = z
                vertices[i+3] = nx
                vertices[i+4] = ny
                vertices[i+5] = nz
                vertices[i+6] = u
                vertices[i+7] = v
            self.vertex_array = VertexArray(vertices)

            face_count = int(f.readline().strip())
            faces = [tuple(map(int, f.readline().strip().split())) for _ in range(face_count)]

            mesh_count = int(f.readline().strip())

            mesh_re = re.compile(r'(?P<mesh_start>\d+) (?P<mesh_end>\d+) (?P<mesh_name>[\w ]+)')
            self.meshs = {}
            for _ in range(mesh_count):
                matches = mesh_re.search(f.readline().strip())
                if matches:
                    name, start, end = matches['mesh_name'], int(matches['mesh_start']), int(matches['mesh_end'])
                    indices = np.empty((end-start) * 3, dtype=np.uint32)
                    for i in range(0, end-start, 3):
                        idx1, idx2, idx3 = faces[start+i]
                        indices[i] = idx1
                        indices[i+1] = idx2
                        indices[i+2] = idx3

                    self.meshs[name] = ElementBuffer(self.vertex_array, indices)

    def draw(self):
        for mesh in self.meshs.values():
            self.vertex_array.bind()
            glDrawElements(GL_TRIANGLES, len(mesh), GL_UNSIGNED_INT, None)
            self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()
        for mesh in self.meshs.values():
            mesh.destroy()