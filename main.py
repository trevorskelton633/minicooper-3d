import glm
import numpy as np

from pathlib import Path
from src.engine.renderer import *


class App(Window):
    def __init__(self, width=800, height=600, title="Mini Cooper 3D", vsync=True):
        super().__init__(width, height, title, vsync)

        self.material = SimpleMaterial()

        self.mesh = CustomMesh(Path(__file__).resolve().parent/'assets'/'models'/'custom'/'mini-cooper.model')

        self.camera = FreeCamera(glm.vec3(0.0, 0.0, 500.0))
        # pygame.mouse.set_visible(False)
        # pygame.event.set_grab(True)

        self.angle = 0

        self.render_mode = 0

        self.colormap = {
            'Upper Driver Wiper': (0.2, 0.2, 0.2),
			'Upper Passenger Wiper': (0.2, 0.2, 0.2),
			'Lower Driver Wiper': (0.2, 0.2, 0.2),
			'Lower Passenger Wiper': (0.2, 0.2, 0.2),
			'Rear Wiper': (0.2, 0.2, 0.2),
			'Vents': (0.1, 0.1, 0.1),
			'License': (0.94, 0.64, 0.19),
			'Front Driver Rim': (0.75, 0.75, 0.75),
			'Front Passenger Rim': (0.75, 0.75, 0.75),
			'Rear Driver Rim': (0.75, 0.75, 0.75),
			'Rear Passenger Rim': (0.75, 0.75, 0.75),
			'Front Driver Tire': (0.1, 0.1, 0.1),
			'Front Passenger Tire': (0.1, 0.1, 0.1),
			'Rear Driver Tire': (0.1, 0.1, 0.1),
			'Rear Passenger Tire': (0.1, 0.1, 0.1),
			'Brakes': (0.75, 0.75, 0.75)
        }

    def on_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                self.render_mode = (self.render_mode + 1) % 3
                if self.render_mode == 0:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
                    print("Render Mode: FILL")
                elif self.render_mode == 1:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
                    print("Render Mode: WIREFRAME")
                elif self.render_mode == 2:
                    glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
                    glPointSize(5.0)
                    print("Render Mode: POINTS")
        # elif event.type == pygame.MOUSEMOTION:
        #     dx, dy = event.rel
        #     self.camera.process_mouse_movement(dx, dy)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:
               self.camera.process_scroll(5)
            elif event.button == 5:
                self.camera.process_scroll(-5)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.camera.process_keyboard(keys, dt)

        self.angle += dt * 45

    def render(self):
        self.material.use()

        projection = glm.perspective(glm.radians(self.camera.fov), self.width / self.height, 0.1, 10000.0)

        self.material.set_mat4('uProjection', np.array(projection.to_list()))
        self.material.set_mat4('uView', np.array(self.camera.get_view_matrix().to_list()))

        model_mat = glm.mat4(1.0)
        model_mat = glm.translate(model_mat, glm.vec3(0.0, 0.0, 0.0))
        model_mat = glm.rotate(model_mat, glm.radians(-60), glm.vec3(1.0, 0.0, 0.0))
        model_mat = glm.rotate(model_mat, glm.radians(self.angle), glm.vec3(0.0, 0.0, 1.0))
        model_mat = glm.scale(model_mat, glm.vec3(1.0, 1.0, 1.0))
        self.material.set_mat4('uModel', np.array(model_mat.to_list(), dtype=np.float32))

        self.mesh.bind()
        for group in self.mesh.groups:
            if group['name'] in self.colormap:
                self.material.set_color(*self.colormap[group['name']])
            else:
                self.material.set_color(0.9, 0.9, 0.9)
            glDrawElements(GL_TRIANGLES, group['count'], GL_UNSIGNED_INT, ctypes.c_void_p(group['start'] * 4))
        self.mesh.unbind()

    def clean(self):
        self.mesh.destroy()
        self.material.destroy()


if __name__ == '__main__':
    App().run()