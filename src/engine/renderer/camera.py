import glm
import pygame


class FreeCamera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 5.0), yaw=-90, pitch=0, speed=5.0, fov=45.0):
        self.position = position
        self.yaw = yaw
        self.pitch = pitch
        self.speed = speed
        self.fov = fov

        self.front = glm.vec3(0, 0, -1)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.world_up = glm.vec3(0, 1, 0)

        self.mouse_sensitivity = 0.1
        self.update_vectors()

    def update_vectors(self):
        # Calculate new front vector
        rad_yaw = glm.radians(self.yaw)
        rad_pitch = glm.radians(self.pitch)

        front = glm.vec3(
            glm.cos(rad_yaw) * glm.cos(rad_pitch),
            glm.sin(rad_pitch),
            glm.sin(rad_yaw) * glm.cos(rad_pitch)
        )
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    def process_mouse_movement(self, dx, dy):
        self.yaw += dx * self.mouse_sensitivity
        self.pitch -= dy * self.mouse_sensitivity
        self.pitch = max(-89.9, min(89.9, self.pitch))
        self.update_vectors()

    def process_scroll(self, y_offset):
        self.fov = glm.clamp(self.fov - y_offset, 10.0, 10000.0)

    def process_keyboard(self, keys, dt):
        velocity = self.speed * dt
        if keys[pygame.K_w]:
            self.position += self.front * velocity
        if keys[pygame.K_z]:
            self.position -= self.front * velocity
        if keys[pygame.K_x]:
            self.position -= self.right * velocity
        if keys[pygame.K_c]:
            self.position += self.right * velocity
        if keys[pygame.K_q]:
            self.position += self.world_up * velocity
        if keys[pygame.K_e]:
            self.position -= self.world_up * velocity
