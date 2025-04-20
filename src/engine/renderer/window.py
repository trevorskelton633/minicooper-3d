import pygame
from pygame.locals import *

from OpenGL.GL import *

class Window:
    def __init__(self, title, resolution):
        pygame.init()
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
        pygame.display.set_mode(resolution, DOUBLEBUF | OPENGL)
        pygame.display.set_caption(title)

        self.clock = pygame.time.Clock()
        self.should_close = False

    def update(self):
        pygame.display.flip()
        self.clock.tick(60)

    def poll_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.should_close = True

    def clear(self, r=0.1, g=0.1, b=0.1, a=1.0):
        glClearColor(r, g, b, a)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def close(self):
        pygame.quit()