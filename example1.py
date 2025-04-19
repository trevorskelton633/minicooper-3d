import pygame
from pygame.locals import *
from OpenGL.GL import *
import numpy as np

def load_shader(shader_type, source):
    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    # Check for compile errors
    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f"Shader compile failed: {error}")
    return shader

def create_shader_program(vertex_src, fragment_src):
    vertex_shader = load_shader(GL_VERTEX_SHADER, vertex_src)
    fragment_shader = load_shader(GL_FRAGMENT_SHADER, fragment_src)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    # Check for linking errors
    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f"Shader link failed: {error}")

    # Cleanup
    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program

def main():
    pygame.init()
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
    pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)
    pygame.display.set_caption("OpenGL 3.3 Triangle")

    with open("shaders/vert.glsl") as f:
        vertex_src = f.read()
    with open("shaders/frag.glsl") as f:
        fragment_src = f.read()

    shader = create_shader_program(vertex_src, fragment_src)
    glUseProgram(shader)

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

    # Main loop
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader)
        glBindVertexArray(VAO)
        glDrawArrays(GL_TRIANGLES, 0, 3)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
