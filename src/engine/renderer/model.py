import re
import numpy as np

from OpenGL.GL import *

class VertexArray:
    def __init__(self, vertices):
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)

        glBindVertexArray(self.vao)

        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        glBindVertexArray(0)

    def bind(self):
        glBindVertexArray(self.vao)

    def unbind(self):
        glBindVertexArray(0)

    def destroy(self):
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])


class ElementBuffer:
    def __init__(self, vertex_array, indices):
        self.ebo = glGenBuffers(1)

        vertex_array.bind()

        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        vertex_array.unbind()

    def destroy(self):
        glDeleteBuffers(1, [self.ebo])


class TriangleModel:
    def __init__(self):
        self.vertices =  np.array([
            0.0,  0.5, 0.0,  # Top
            -0.5, -0.5, 0.0,  # Bottom Left
            0.5, -0.5, 0.0   # Bottom Right
        ], dtype=np.float32)

        self.vertex_array = VertexArray(self.vertices)

    def draw(self):
        self.vertex_array.bind()
        glDrawArrays(GL_TRIANGLES, 0, len(self.vertices))
        self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()


class SquareModel:
    def __init__(self):
        self.vertices = np.array([
            0.5,  0.5, 0.0,  # top right
            0.5, -0.5, 0.0,  # bottom right
            -0.5, -0.5, 0.0,  # bottom left
            -0.5,  0.5,  0.0   # top left
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 3,  # first triangle
            1, 2, 3   # second triangle
        ], dtype=np.uint32)

        self.vertex_array = VertexArray(self.vertices)
        self.elem_buffer = ElementBuffer(self.vertex_array, self.indices)

    def draw(self):
        self.vertex_array.bind()
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        self.vertex_array.unbind()

    def destroy(self):
        self.vertex_array.destroy()
        self.elem_buffer.destroy()


class CustomModel:
    def __init__(self, file):
        with open(file) as f:
            vertex_count = int(f.readline().strip())

            # TODO: use numpy arrays
            self.vertices = []
            self.normals = []
            self.tex_coords = []
            for _ in range(vertex_count):
                x, y, z, nx, ny, nz, u, v = tuple(map(float, f.readline().strip().split()))
                self.vertices.append((x, y, z))
                self.normals.append((nx, ny, nz))
                self.tex_coords.append((u, v))

            index_count = int(f.readline().strip())

            self.indices = [tuple(map(int, f.readline().strip().split())) for _ in range(index_count)]

            geom_count = int(f.readline().strip())

            self.geom_re = re.compile(r'(?P<geom_start>\d+) (?P<geom_end>\d+) (?P<geom_name>[\w ]+)')
            self.geoms = []
            for _ in range(geom_count):
                matches = self.geom_re.search(f.readline().strip())
                if matches:
                    self.geoms.append((int(matches['geom_start']), int(matches['geom_end']), matches['geom_name']))

    def draw(self):
        pass

    def destroy(self):
        # TODO:
        # glDeleteVertexArrays(1, [self.vao])
        # glDeleteBuffers(1, [self.vbo])
        pass