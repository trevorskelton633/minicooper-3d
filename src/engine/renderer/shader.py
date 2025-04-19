from OpenGL.GL import *

def compile_shader(shader_type, path):
    with open(f'shaders/{path}') as f:
        source = f.read()

    shader = glCreateShader(shader_type)
    glShaderSource(shader, source)
    glCompileShader(shader)

    if not glGetShaderiv(shader, GL_COMPILE_STATUS):
        error = glGetShaderInfoLog(shader).decode()
        raise RuntimeError(f'Shader compile failed: {error}')

    return shader

def compile_shader_program(vertex_path, fragment_path):
    vertex_shader = compile_shader(GL_VERTEX_SHADER, vertex_path)
    fragment_shader = compile_shader(GL_FRAGMENT_SHADER, fragment_path)

    program = glCreateProgram()
    glAttachShader(program, vertex_shader)
    glAttachShader(program, fragment_shader)
    glLinkProgram(program)

    if not glGetProgramiv(program, GL_LINK_STATUS):
        error = glGetProgramInfoLog(program).decode()
        raise RuntimeError(f'Shader link failed: {error}')

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return program