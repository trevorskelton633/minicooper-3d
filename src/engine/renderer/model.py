import glm
import numpy as np

class Model:
    def __init__(self, mesh, material):
        self.mesh = mesh
        self.material = material

        self.scale_mat = glm.mat4(1.0)
        self.rotate_mat = glm.mat4(1.0)
        self.translate_mat = glm.mat4(1.0)

        self.projection_mat = glm.mat4(1.0)
        self.view_mat = glm.mat4(1.0)

    def scale(self, value):
        self.scale_mat = glm.scale(glm.mat4(1.0), value)

    def rotate(self, angle, axis):
        self.rotate_mat = glm.rotate(glm.mat4(1.0), glm.radians(angle), axis)

    def translate(self, value):
        self.translate_mat = glm.translate(glm.mat4(1.0), value)

    def project(self, projection, camera):
        self.projection_mat = projection
        self.view_mat = camera.get_view_matrix()

    def draw(self):
        self.material.use()

        self.material.set_mat4('projection', np.array(self.projection_mat.to_list()))
        self.material.set_mat4('view', np.array(self.view_mat.to_list()))

        model_mat = glm.mat4(1.0) * self.translate_mat * self.rotate_mat * self.scale_mat
        self.material.set_mat4('model', np.array(model_mat.to_list(), dtype=np.float32))

        self.mesh.draw()

    def destroy(self):
        self.mesh.destroy()
        self.material.destroy()