from OpenGL.GL import *
from pathlib import Path


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

    def set_float(self, uniform, value):
        glUniform1f(glGetUniformLocation(self.program, uniform), value)

    def set_vec3(self, uniform, x, y, z):
        glUniform3f(glGetUniformLocation(self.program, uniform), x, y, z)

    def set_mat4(self, uniform, mat):
        glUniformMatrix4fv(glGetUniformLocation(self.program, uniform), 1, GL_FALSE, mat)

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

    def destroy(self):
        glDeleteProgram(self.program)

class ColorShader(Shader):
    def __init__(self, r=0.9, g=0.9, b=0.9, opacity=1.0):
        super().__init__('simple/vert.glsl', 'simple/frag.glsl')

        self.set_color(r, g, b)
        self.set_opacity(opacity)

    def set_color(self, r, g, b):
        self.use()
        self.set_vec3('uColor', r, g, b)

    def set_opacity(self, a):
        self.use()
        self.set_float('uOpacity', a)

class TextureShader(Shader):
    def __init__(self):
        super().__init__('texture/vert.glsl', 'texture/frag.glsl')