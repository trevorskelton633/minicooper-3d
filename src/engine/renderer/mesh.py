import ctypes
import re
import glm

import numpy as np

from OpenGL.GL import *


def parse_custom_mesh(path):
    with open(path) as f:
        vertex_count = int(f.readline().strip())
        vertices = [list(map(float, f.readline().strip().split())) for _ in range(vertex_count)]

        index_count = int(f.readline().strip())
        indices = [list(map(int, f.readline().strip().split())) for _ in range(index_count)]

        group_re = re.compile(r'(?P<group_start>\d+) (?P<group_end>\d+) (?P<group_name>[\w ]+)')
        group_count = int(f.readline().strip())
        groups = []
        for _ in range(group_count):
            matches = group_re.search(f.readline().strip())
            if matches:
                name, start, end = matches['group_name'], int(matches['group_start']), int(matches['group_end'])
                offset = 3 # 3 indices per triangle
                groups.append({
                    'start': start * offset,
                    'count': (end - start) * offset,
                    'name': name
                })

        return np.array(vertices, dtype=np.float32), np.array(indices, dtype=np.uint32), groups

class Model:
    def __init__(self):
        self.vertices, self.indices, self.mesh_groups = self.load_model()
        self.textures = self.load_textures()

        self._init_gl()

        self.translate_matrix = glm.mat4(1.0)
        self.rotate_matrix = glm.mat4(1.0)
        self.scale_matrix = glm.mat4(1.0)
        self.model_matrix = self._normalize_model()

        del self.vertices
        del self.indices

    def load_model(self):
        pass

    def load_textures(self):
        pass

    def _init_gl(self):
        self.gl_vertices = VertexArray(self.vertices, stride=8)
        self.gl_indices = ElementBuffer(self.gl_vertices, self.indices)

    def _normalize_model(self):
        vertices = self.vertices.reshape((-1, 3))
        min_vals = vertices.min(axis=0)
        max_vals = vertices.max(axis=0)

        center = (min_vals + max_vals) / 2.0
        size = max_vals - min_vals
        max_dim = np.max(size)

        return glm.translate(glm.scale(glm.mat4(1.0), glm.vec3(1.0 / max_dim)), -glm.vec3(*center))

    def scale(self, magnitude):
        self.scale_matrix = glm.scale(self.scale_matrix, magnitude)

    def rotate(self, angle, axis):
        self.rotate_matrix = glm.rotate(self.rotate_matrix, glm.radians(angle), axis)

    def translate(self, position):
        self.translate_matrix = glm.translate(self.translate_matrix, position)

    def render(self, projection, view):
        self.gl_vertices.bind()
        self.gl_indices.bind()

        self.final_model_matrix = self.translate_matrix * self.rotate_matrix * self.scale_matrix * self.model_matrix

        self.draw(projection, view)

        self.translate_matrix = glm.mat4(1.0)
        self.rotate_matrix = glm.mat4(1.0)
        self.scale_matrix = glm.mat4(1.0)

        self.gl_indices.unbind()
        self.gl_vertices.unbind()

    def destroy(self):
        for shader in self.shaders.values():
            shader.destroy()

        for texture in self.textures:
            glDeleteTextures(1, texture)

        self.gl_indices.destroy()
        self.gl_vertices.destroy()


class VertexArray:
    def __init__(self, vertices, stride=3):
        self.length = len(vertices)

        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        self.bind()

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)

        if stride == 5:
            # no normal
            glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, stride * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(1)
        elif stride == 6:
            # no texcoord
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(1)
        elif stride == 8:
            # normal and texcoord
            glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(3 * ctypes.sizeof(ctypes.c_float)))
            glEnableVertexAttribArray(1)

            glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride * ctypes.sizeof(ctypes.c_float), ctypes.c_void_p(6 * ctypes.sizeof(ctypes.c_float)))
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