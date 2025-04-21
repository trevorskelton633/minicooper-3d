from pathlib import Path

import glm

from src.engine.renderer import *


GAME_TITLE = 'Mini Cooper 3D'
SCREEN_RESOLUTION = (800, 600)


def main():
    window = Window(GAME_TITLE, SCREEN_RESOLUTION)

    material = BasicMaterial()

    # mesh = TriangleMesh()
    # mesh = PlaneMesh()
    mesh = CubeMesh()
    # mesh = CustomMesh(Path(__file__).resolve().parent/'assets'/'models'/'custom'/'mini-cooper.model')

    model = Model(mesh, material)

    camera = FreeFlyCamera()

    while not window.should_close:
        window.poll_events()
        window.clear()

        fov = 45.0
        projection = glm.perspective(glm.radians(fov), window.width / window.height, 0.1, 100.0)

        # # Keyboard movement
        # if key_is_pressed("W"):
        #     camera.process_keyboard("FORWARD", delta_time)
        # if key_is_pressed("S"):
        #     camera.process_keyboard("BACKWARD", delta_time)
        # if key_is_pressed("A"):
        #     camera.process_keyboard("LEFT", delta_time)
        # if key_is_pressed("D"):
        #     camera.process_keyboard("RIGHT", delta_time)
        # if key_is_pressed("SPACE"):
        #     camera.process_keyboard("UP", delta_time)
        # if key_is_pressed("LEFT_SHIFT"):
        #     camera.process_keyboard("DOWN", delta_time)

        # # Mouse movement
        # camera.process_mouse_movement(mouse_dx, -mouse_dy)

        model.project(projection, camera)

        model.translate(glm.vec3(0.0, 0.0, 0.0))
        model.rotate(window.get_time() * 45, glm.vec3(0.0, 1.0, 1.0))
        model.scale(glm.vec3(1.0, 1.0, 1.0))

        model.draw()

        window.update()

    model.destroy()
    window.close()


if __name__ == '__main__':
    main()