import glm
import numpy as np

from src.engine.renderer import *


class CubeModel(Model):
    def __init__(self):
        super().__init__()

        self.shaders = {
            'texture': TextureShader()
        }

    def load_model(self):
        return parse_custom_mesh(Path(__file__).resolve().parent/'assets'/'models'/'custom'/'cube.model')

    def load_textures(self):
        return [load_texture(Path(__file__).resolve().parent/'assets'/'textures'/'container.jpg')]

    def draw(self, projection, view):
        self.shaders['texture'].use()

        self.shaders['texture'].set_mat4('uProjection', projection)
        self.shaders['texture'].set_mat4('uView', view)
        self.shaders['texture'].set_mat4('uModel', np.array(self.final_model_matrix.to_list(), dtype=np.float32))

        glBindTexture(GL_TEXTURE_2D, self.textures[0])
        for group in self.mesh_groups:
            offset = group['start'] * ctypes.sizeof(ctypes.c_uint)
            glDrawElements(GL_TRIANGLES, group['count'], GL_UNSIGNED_INT, ctypes.c_void_p(offset))
        glBindTexture(GL_TEXTURE_2D, 0)

class MiniCooperModel(Model):
    def __init__(self):
        super().__init__()

        self.shaders = {
            'color': ColorShader(),
            'texture': TextureShader()
        }

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
			'Brakes': (0.75, 0.75, 0.75),
            'Rear View Mirror': (0.1, 0.1, 0.1),
            'Interior': (0.1, 0.1, 0.1),
            'Driver': (0.2235, 1.0, 0.0784),
            'Chair': (0.68, 0.68, 0.68),
            'Windows': (0.1, 0.1, 0.1)
        }

    def load_model(self):
        return parse_custom_mesh(Path(__file__).resolve().parent/'assets'/'models'/'custom'/'mini-cooper.model')

    def load_textures(self):
        return [load_texture(Path(__file__).resolve().parent/'assets'/'textures'/'mini-cooper.png')]

    def draw(self, projection, view):
        for group in self.mesh_groups:
            if group['name'] in self.colormap:
                self.shaders['color'].use()

                self.shaders['color'].set_mat4('uProjection', projection)
                self.shaders['color'].set_mat4('uView', view)
                self.shaders['color'].set_mat4('uModel', np.array(self.final_model_matrix.to_list(), dtype=np.float32))

                if group['name'] == 'Windows':
                    glEnable(GL_BLEND)
                    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
                    self.shaders['color'].set_opacity(0.3)
                else:
                    glDisable(GL_BLEND)

                self.shaders['color'].set_color(*self.colormap[group['name']])

                offset = group['start'] * ctypes.sizeof(ctypes.c_uint)
                glDrawElements(GL_TRIANGLES, group['count'], GL_UNSIGNED_INT, ctypes.c_void_p(offset))
            else:
                glBindTexture(GL_TEXTURE_2D, self.textures[0])
                self.shaders['texture'].use()

                self.shaders['texture'].set_mat4('uProjection', projection)
                self.shaders['texture'].set_mat4('uView', view)
                self.shaders['texture'].set_mat4('uModel', np.array(self.final_model_matrix.to_list(), dtype=np.float32))

                offset = group['start'] * ctypes.sizeof(ctypes.c_uint)
                glDrawElements(GL_TRIANGLES, group['count'], GL_UNSIGNED_INT, ctypes.c_void_p(offset))
                glBindTexture(GL_TEXTURE_2D, 0)


class App(Window):
    def __init__(self, width=800, height=600, title="Mini Cooper 3D", vsync=True):
        super().__init__(width, height, title, vsync)

        self.camera = FreeCamera(glm.vec3(0.0, 0.0, 2.0))
        # pygame.mouse.set_visible(False)
        # pygame.event.set_grab(True)

        self.angle = 0

        self.render_mode = 0

        # self.model = CubeModel()
        self.model = MiniCooperModel()

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
        glClearColor(0.68, 0.68, 0.68, 1.0)

        projection = np.array(glm.perspective(glm.radians(self.camera.fov), self.width / self.height, 0.1, 1000.0).to_list())
        view = np.array(self.camera.get_view_matrix().to_list())

        self.model.rotate(-60, glm.vec3(1.0, 0.0, 0.0))
        self.model.rotate(self.angle, glm.vec3(0.0, 0.0, 1.0))
        self.model.render(projection, view)

    def clean(self):
        self.model.destroy()


if __name__ == '__main__':
    App().run()