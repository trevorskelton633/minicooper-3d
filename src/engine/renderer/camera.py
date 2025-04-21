import glm

class FreeFlyCamera:
    def __init__(self, position=glm.vec3(0.0, 0.0, 3.0), speed=5.0, sensitivity=0.1):
        self.position = position
        self.front = glm.vec3(0.0, 0.0, -1.0)
        self.up = glm.vec3(0.0, 1.0, 0.0)
        self.right = glm.cross(self.front, self.up)

        self.world_up = glm.vec3(0.0, 1.0, 0.0)

        self.yaw = -90.0
        self.pitch = 0.0
        self.roll = 0.0  # For free-fly

        self.speed = speed
        self.sensitivity = sensitivity

        self.update_vectors()

    def get_view_matrix(self):
        return glm.lookAt(self.position, self.position + self.front, self.up)

    # def process_keyboard(self, direction, delta_time):
    #     velocity = self.speed * delta_time
    #     if direction == "FORWARD":
    #         self.position += self.front * velocity
    #     if direction == "BACKWARD":
    #         self.position -= self.front * velocity
    #     if direction == "LEFT":
    #         self.position -= self.right * velocity
    #     if direction == "RIGHT":
    #         self.position += self.right * velocity
    #     if direction == "UP":
    #         self.position += self.world_up * velocity
    #     if direction == "DOWN":
    #         self.position -= self.world_up * velocity

    # def process_mouse_movement(self, xoffset, yoffset, constrain_pitch=True):
    #     xoffset *= self.sensitivity
    #     yoffset *= self.sensitivity

    #     self.yaw += xoffset
    #     self.pitch += yoffset

    #     if constrain_pitch:
    #         self.pitch = max(-89.0, min(89.0, self.pitch))

    #     self.update_vectors()

    def update_vectors(self):
        # Convert angles to direction
        front = glm.vec3()
        front.x = glm.cos(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        front.y = glm.sin(glm.radians(self.pitch))
        front.z = glm.sin(glm.radians(self.yaw)) * glm.cos(glm.radians(self.pitch))
        self.front = glm.normalize(front)

        self.right = glm.normalize(glm.cross(self.front, self.world_up))
        self.up = glm.normalize(glm.cross(self.right, self.front))