from pathlib import Path

from OpenGL.GL import *


class Shader:
    def __init__(self, vertex_file, fragment_file):
        vertex_shader = self.compile_shader(GL_VERTEX_SHADER, vertex_file)
        fragment_shader = self.compile_shader(GL_FRAGMENT_SHADER, fragment_file)

        self.program = glCreateProgram()
        glAttachShader(self.program, vertex_shader)
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)

        if not glGetProgramiv(self.program, GL_LINK_STATUS):
            error = glGetProgramInfoLog(self.program).decode()
            raise RuntimeError(f'Shader link failed: {error}')

        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)

    def use(self):
        glUseProgram(self.program)

    def compile_shader(self, shader_type, path):
        with open(Path(__file__).resolve().parent/'shaders'/path) as f:
            source = f.read()

        shader = glCreateShader(shader_type)
        glShaderSource(shader, source)
        glCompileShader(shader)

        if not glGetShaderiv(shader, GL_COMPILE_STATUS):
            error = glGetShaderInfoLog(shader).decode()
            raise RuntimeError(f'Shader compile failed: {error}')

        return shader


class SimpleShader(Shader):
    def __init__(self):
        super().__init__('simple/vert.glsl', 'simple/frag.glsl')