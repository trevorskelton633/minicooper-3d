from pathlib import Path

from src.engine.renderer import *


GAME_TITLE = 'Mini Cooper 3D'
SCREEN_RESOLUTION = (800, 600)


def main():
    window = Window(GAME_TITLE, SCREEN_RESOLUTION)

    simple_shader = SimpleShader()
    model = TriangleModel()
    # model = SquareModel()

    # model = CustomModel(Path(__file__).resolve().parent/'assets'/'models'/'custom'/'mini-cooper.model')

    while not window.should_close:
        window.poll_events()
        window.clear()

        simple_shader.use()
        model.draw()

        window.update()

    model.destroy()
    window.close()


if __name__ == '__main__':
    main()
    # test()
