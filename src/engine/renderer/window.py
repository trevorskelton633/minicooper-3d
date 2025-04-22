import pygame

from pygame.locals import *
from OpenGL.GL import *


class Window:
    def __init__(self, width=800, height=600, title="OpenGL Window", vsync=True):
        self.width = width
        self.height = height
        self.title = title
        self.running = True

        pygame.init()
        pygame.display.set_caption(title)
        pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        if vsync:
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 1)
        else:
            pygame.display.gl_set_attribute(pygame.GL_SWAP_CONTROL, 0)

        self.clock = pygame.time.Clock()
        self._init_gl()

    def _init_gl(self):
        glEnable(GL_DEPTH_TEST)
        glViewport(0, 0, self.width, self.height)
        glClearColor(0.1, 0.1, 0.1, 1.0)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            self.on_event(event)

    def on_event(self, event):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass

    def clean(self):
        pass

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.handle_events()

            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            self.update(dt)
            self.render()

            pygame.display.flip()

        self.clean()
        pygame.quit()