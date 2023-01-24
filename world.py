import math
import random
from pixel import Pixel

SIZE_X = 500
SIZE_Y = 500
NUM_PIXELS = 200
RADIUS_MAX = 100
ACCEL_MOD = 0.01
MIN_DISTANCE = 20
# COLOR_ATTR_MATRIX = [[0.8, -0.2, 0.3], [1, -0.2, 0.5], [-0.3, 0.6, -0.5]]
DRAG = 0.9
BUFFER_ZONE = 1
MAX_ACCEL = 0.08


class World:
    def __init__(self):
        self.pixels = self.generate_pixels()
        self.color_matrix = [[0.9,1,-0.8],[-0.8,0.9,1],[1,-0.8,0.9]]
        self.attraction_matrix = None

    def generate_pixels(self):
        pixels = []
        for _ in range(0, NUM_PIXELS):
            pixels.append(
                Pixel(
                    random.randint(0, SIZE_X),
                    random.randint(0, SIZE_Y),
                    random.choice(range(0, 3)),
                    SIZE_X,
                    SIZE_Y,
                )
            )
        # pixels.append(Pixel(100, 100, COLORS[0]))
        # pixels.append(Pixel(50, 100, COLORS[1]))

        return pixels

    def update_world(self, dt):
        self.apply_accelerations()
        self.update_pixels(dt)

    def apply_accelerations(self):
        for pixel in self.pixels:
            accel_x, accel_y = self.calculate_acceleration(pixel)
            pixel.apply_accel(accel_x, accel_y)

    def calculate_acceleration(self, pixel_a):
        accel_x, accel_y = 0, 0
        for pixel_b in self.pixels:
            if self.check_if_pixels_too_far(pixel_a, pixel_b):
                continue
            diff_accel_x, diff_accel_y = self.calculate_accel_between_pixels(
                pixel_a, pixel_b
            )
            accel_x += diff_accel_x
            accel_y += diff_accel_y
        return accel_x, accel_y

    @staticmethod
    def generate_color_matrix():
        m, n = 3, 3
        color_matrix = [[0] * n for i in range(m)]
        for i in range(0, 3):
            for j in range(0, 3):
                color_matrix[i][j] = random.uniform(-1, 1)
                print(color_matrix[i][j], end=" ")
            print()

        return color_matrix
    @staticmethod
    def check_if_pixels_too_far(pixel_a, pixel_b):
        if pixel_a.pos_x is pixel_b.pos_x and pixel_a.pos_y is pixel_b.pos_y:
            return True
        if (
            abs(pixel_a.pos_x - pixel_b.pos_x) > RADIUS_MAX
            or abs(pixel_a.pos_y - pixel_b.pos_y) > RADIUS_MAX
        ):
            return True
        return False

    def calculate_accel_between_pixels(self, pixel_a, pixel_b):
        distance = self.calculate_distance(pixel_a, pixel_b)
        angle = self.calculate_angle(pixel_a, pixel_b)
        x_mod, y_mod = self.calculate_mods(pixel_a, pixel_b)
        color_mod = self.get_color_mod(pixel_a, pixel_b)
        accel_x = 0
        accel_y = 0

        # check too close
        if distance > RADIUS_MAX:
            accel_x = 0
            accel_y = 0
        else:
            if distance > 0:
                if distance < MIN_DISTANCE - BUFFER_ZONE:
                    accel_x = -math.cos(angle) * 1 / distance * ACCEL_MOD
                    accel_y = - math.sin(angle) * 1 / distance * ACCEL_MOD
                else:
                    accel_x = math.cos(angle) * 1 / distance * ACCEL_MOD * color_mod
                    accel_y = math.sin(angle) * 1 / distance * ACCEL_MOD * color_mod
                if distance > MIN_DISTANCE - BUFFER_ZONE and distance < MIN_DISTANCE:
                    accel_x = 0
                    accel_y = 0

        accel_x, accel_y = self.limit_accelerations(accel_x, accel_y)
        return accel_x * x_mod, accel_y * y_mod

    def get_color_mod(self, pixel_a, pixel_b):
        return self.color_matrix[pixel_a.color][pixel_b.color]

    @staticmethod
    def limit_accelerations(accel_x, accel_y):
        if accel_x > MAX_ACCEL:
            accel_x = MAX_ACCEL
        if accel_y > MAX_ACCEL:
            accel_y = MAX_ACCEL
        if accel_x < -MAX_ACCEL:
            accel_x = -MAX_ACCEL
        if accel_y < -MAX_ACCEL:
            accel_y = -MAX_ACCEL
        return accel_x, accel_y

    @staticmethod
    def calculate_mods(pixel_a, pixel_b):
        if pixel_a.pos_x < pixel_b.pos_x:
            return 1, 1
        else:
            return -1, -1

    @staticmethod
    def calculate_distance(pixel_a, pixel_b):
        return math.sqrt(
            (pixel_a.pos_x - pixel_b.pos_x) ** 2 + (pixel_a.pos_y - pixel_b.pos_y) ** 2
        )

    @staticmethod
    def calculate_angle(pixel_a, pixel_b):
        if abs(pixel_b.pos_x - pixel_a.pos_x) < 0.0001:
            if pixel_a.pos_y < pixel_b.pos_y:
                return -math.pi / 2
            else:
                return math.pi / 2
        return math.atan(
            (pixel_b.pos_y - pixel_a.pos_y) / (pixel_b.pos_x - pixel_a.pos_x)
        )

    def update_pixels(self, dt):
        for pixel in self.pixels:
            pixel.update(dt, DRAG)
