class Pixel:
    def __init__(self, pos_x, pos_y, color, bounds_x, bounds_y):
        self.vel_x = 0
        self.vel_y = 0
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.color = color
        self.bounds_x = bounds_x
        self.bounds_y = bounds_y

    def apply_accel(self, accel_x, accel_y):
        self.vel_x += accel_x
        self.vel_y += accel_y

    def update(self, dt, drag):
        self.vel_x *= drag
        self.vel_y *= drag
        self.pos_x += self.vel_x * dt
        self.pos_y += self.vel_y * dt

        if self.pos_x > self.bounds_x:
            self.pos_x = self.bounds_x
            self.vel_x *= -1
            self.vel_x -= 0.1
        if self.pos_y > self.bounds_y:
            self.pos_y = self.bounds_y
            self.vel_y *= -1
            self.vel_y -= 0.1
        if self.pos_x < 0:
            self.pos_x = 0
            self.vel_x *= -1
            self.vel_x += 0.1
        if self.pos_y < 0:
            self.pos_y = 0
            self.vel_y *= -1
            self.vel_y += 0.1
