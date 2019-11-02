import math
import random
import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rocket Test"
SPRITE_SCALE_PLAYER = 0.25
SPRITE_SCALE_PLANETS = 0.35
SPRITE_SCALE_BOX = 0.2
SPRITE_SCALE_PROJECTILE_DOT = 0.3
PROJECTILE_DOT_FREQ = 10
GRAV_CONST = 100

DRAW_VELOCITY = False # warning: laggy
DRAW_PATH = True

def make_star_field(star_count):
    """ Make a bunch of circles for stars. """

    shape_list = arcade.ShapeElementList()

    for star_no in range(star_count):
        x = random.randrange(SCREEN_WIDTH)
        y = random.randrange(SCREEN_HEIGHT)
        radius = random.randrange(1, 4)
        brightness = random.randrange(128, 256)
        color = (brightness, brightness, brightness)
        shape = arcade.create_rectangle_filled(x, y, radius, radius, color)
        shape_list.append(shape)

    return shape_list

# Finds gravitational acceleration between two objects, given their position and the larger object's mass
def find_velocity(x1, y1, x2, y2, mass):

    delta_x = x2 - x1
    delta_y = y2 - y1
    distance = math.sqrt(pow(delta_x, 2) + pow(delta_y, 2))

    # g = GM / d^2, so calculate g
    g = GRAV_CONST * mass / pow(distance, 2)

    # Split g into x and y
    gx = g * delta_x / distance
    gy = g * delta_y / distance

    return (gx, gy)

class MyGame(arcade.Window):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Set the working directory (where we expect to find files) to the same
        # directory this .py file is in. You can leave this out of your own
        # code, but it is needed to easily run the examples using "python -m"
        # as mentioned at the top of this program.
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        # Variables that will hold sprite lists
        self.player_list = None
        self.planet_list = None
        self.projectile_list = None
        self.path_list = None
        self.stars = make_star_field(250)

        # Set up the player info
        self.player_sprite = None

        # Variable for drawing
        self.draw_frame = 0

        arcade.set_background_color(arcade.color.BLACK)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.planet_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()
        self.path_list = arcade.ShapeElementList()

        # Set up planets
        planet1 = arcade.Sprite("images/planet_01.png", scale=SPRITE_SCALE_PLANETS)
        planet1.center_x = 600
        planet1.center_y = 300
        planet1.collision_radius = 40

        planet2 = arcade.Sprite("images/planet_02.png", scale=SPRITE_SCALE_PLANETS)
        planet2.center_x = 200
        planet2.center_y = 300
        planet2.collision_radius = 40

        self.planet_list.append(planet1)
        self.planet_list.append(planet2)

        # Set up the player
        self.player_sprite = arcade.Sprite("images/character.jpeg", scale=SPRITE_SCALE_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Draw everything """
        self.draw_frame += 1

        arcade.start_render()
        self.player_list.draw()
        self.planet_list.draw()
        self.stars.draw()
        self.projectile_list.draw()
        self.path_list.draw()

        if DRAW_PATH:
            if self.draw_frame % PROJECTILE_DOT_FREQ == 0:
                for projectile in self.projectile_list:
                    path_dot = arcade.create_rectangle_filled(projectile.center_x, projectile.center_y, 10, 10, arcade.color.LIGHT_SEA_GREEN)
                    self.path_list.append(path_dot)

        # draw text on its velocity
        if DRAW_VELOCITY:
            for projectile in self.projectile_list:
                velocity_x = f"velocity (x): {round(projectile.velocity[0], 2)}"
                velocity_y = f"velocity (y): {round(projectile.velocity[1], 2)}"
                arcade.draw_text(velocity_x, projectile.center_x + 10, projectile.center_y + 10, arcade.color.WHITE, 14)
                arcade.draw_text(velocity_y, projectile.center_x + 10, projectile.center_y - 10, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        projectile = arcade.Sprite("images/box.png", scale=SPRITE_SCALE_BOX)
        projectile.center_x = x
        projectile.center_y = y
        projectile.velocity = (3, 3)

        self.projectile_list.append(projectile)

        # reset projectile path list upon click
        self.path_list = arcade.ShapeElementList()

    # def on_mouse_release(self, x: float, y: float, button: int,
    #                      modifiers: int):


    def on_update(self, delta_time):
        """ Movement and game logic """

        # Used to update a projectile's velocity
        def update_projectile_velocity(x, y, velocity_x, velocity_y):
            # Check its acceleration due to every planet and add it together
            for planet in self.planet_list:
                velocity_change = find_velocity(x, y, planet.center_x, planet.center_y, planet.collision_radius)
                velocity_x += velocity_change[0]
                velocity_y += velocity_change[1]

            return (velocity_x, velocity_y)

        for projectile in self.projectile_list:
            # update projectile depending on its velocity
            projectile.update()
            # change its velocity based on where the other planets are
            projectile.velocity = update_projectile_velocity(projectile.center_x, projectile.center_y, projectile.velocity[0], projectile.velocity[1])

        # Remove all projectiles that have collided with a planet
        for planet in self.planet_list:
            projectile_hit_list = arcade.check_for_collision_with_list(planet, self.projectile_list)

            # Loop through each colliding projectile and remove it.
            for projectile in projectile_hit_list:
                projectile.remove_from_sprite_lists()


def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()