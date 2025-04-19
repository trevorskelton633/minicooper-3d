import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np
from src.engine.renderer import *

def get_simple_shader():
    return compile_shader_program('simple/vert.glsl', 'simple/frag.glsl')

GAME_TITLE = 'OpenGL 3.3 Triangle'
SCREEN_RESOLUTION = (800, 600)

def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
    pygame.display.set_mode(SCREEN_RESOLUTION, DOUBLEBUF | OPENGL)
    pygame.display.set_caption(GAME_TITLE)

    # Triangle data
    vertices = np.array([
         0.0,  0.5, 0.0,  # Top
        -0.5, -0.5, 0.0,  # Bottom Left
         0.5, -0.5, 0.0   # Bottom Right
    ], dtype=np.float32)

    # Create VBO
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Create VAO
    VAO = glGenVertexArrays(1)
    glBindVertexArray(VAO)

    # Enable vertex attribute
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    shader = get_simple_shader()

    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)

        # clear screen
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # draw triangle
        glUseProgram(shader)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        pygame.display.flip()

        # poll events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()

if __name__ == '__main__':
    main()
