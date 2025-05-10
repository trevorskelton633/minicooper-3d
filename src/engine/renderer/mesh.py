import ctypes
import re
import glm
import numpy as np

from OpenGL.GL import *
from PIL import Image


class VertexArray:
    def __init__(self, vertices, normals=True, texcoords=True):
        self.length = len(vertices)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        self.bind()

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        stride = 3

        if normals:
            stride += 3

        if texcoords:
            stride += 2

        stride = stride * ctypes.sizeof(ctypes.c_float)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        if normals:
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(1)

        if texcoords:
            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(2)

        self.unbind()

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

    def bind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)

    def unbind(self):
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, 0)

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
        self.model_matrix = glm.mat4(1.0)

    def bind(self):
        self.vertex_array.bind()
        self.mesh.bind()

    def unbind(self):
        self.mesh.unbind()
        self.vertex_array.unbind()

    def draw(self):
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertex_array))

    def destroy(self):
        self.vertex_array.destroy()


class PlaneMesh:
    def __init__(self, texture_file=None):
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
        self.model_matrix = glm.mat4(1.0)

        self.texture = None
        if texture_file:
            image = Image.open(texture_file)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = image.convert("RGBA").tobytes()

            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height,
                        0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def bind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        self.vertex_array.bind()
        self.mesh.bind()

    def unbind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, 0)
        self.mesh.unbind()
        self.vertex_array.unbind()

    def draw(self, shader):
        self.bind()
        glDrawElements(GL_TRIANGLES, len(self.mesh), GL_UNSIGNED_INT, None)
        self.unbind()

    def destroy(self):
        self.mesh.destroy()
        self.vertex_array.destroy()


class CubeMesh:
    def __init__(self, texture_file=None):
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
        self.model_matrix = glm.mat4(1.0)

        self.texture = None
        if texture_file:
            image = Image.open(texture_file)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = image.convert("RGBA").tobytes()

            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height,
                        0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def bind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        self.vertex_array.bind()
        self.mesh.bind()

    def unbind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, 0)
        self.mesh.unbind()
        self.vertex_array.unbind()

    def draw(self, shader):
        self.bind()
        glDrawElements(GL_TRIANGLES, len(self.mesh), GL_UNSIGNED_INT, None)
        self.unbind()

    def destroy(self):
        self.mesh.destroy()
        self.vertex_array.destroy()


class CustomMesh:
    def __init__(self, model_file, texture_file=None):
        with open(model_file) as f:
            vertex_count = int(f.readline().strip())

            vertices = []
            for _ in range(vertex_count):
                vertices += (list(map(float, f.readline().strip().split())))
            self.vertex_array = VertexArray(np.array(vertices, dtype=np.float32), True, True)

            index_count = int(f.readline().strip())

            indices = []
            for _ in range(index_count):
                indices += (list(map(int, f.readline().strip().split())))
            self.mesh = ElementBuffer(self.vertex_array, np.array(indices, dtype=np.uint32))

            group_count = int(f.readline().strip())

            group_re = re.compile(r'(?P<group_start>\d+) (?P<group_end>\d+) (?P<group_name>[\w ]+)')
            self.groups = []
            for _ in range(group_count):
                matches = group_re.search(f.readline().strip())
                if matches:
                    name, start, end = matches['group_name'], int(matches['group_start']), int(matches['group_end'])
                    # 3 is how many indices per vertex
                    self.groups.append({'start': start*3, 'count': (end-start)*3, 'name': name})

        # normalize vertices model_matrix
        vertices = np.array(vertices, dtype=np.float32).reshape((-1, 3))
        min_vals = vertices.min(axis=0)
        max_vals = vertices.max(axis=0)

        center = (min_vals + max_vals) / 2.0
        size = max_vals - min_vals
        max_dim = np.max(size)

        self.model_matrix = glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(1.0 / max_dim)), -glm.vec3(*center))

        self.texture = None
        if texture_file:
            image = Image.open(texture_file)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            img_data = image.convert("RGBA").tobytes()

            self.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture)

            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image.width, image.height,
                        0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)
            glGenerateMipmap(GL_TEXTURE_2D)

            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    def bind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, self.texture)
        self.vertex_array.bind()
        self.mesh.bind()

    def unbind(self):
        if self.texture:
            glBindTexture(GL_TEXTURE_2D, 0)
        self.mesh.unbind()
        self.vertex_array.unbind()

    def draw(self, shader):
        self.bind()
        for group in self.groups:
            # 4 is sizeof(GL_UNSIGNED_INT)
            glDrawElements(GL_TRIANGLES, group['count'], GL_UNSIGNED_INT, ctypes.c_void_p(group['start'] * 4))
        self.unbind()

    def destroy(self):
        self.mesh.destroy()
        self.vertex_array.destroy()