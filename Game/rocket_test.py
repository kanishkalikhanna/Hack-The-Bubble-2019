import random
import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Rocket Test"
SPRITE_SCALE_PLAYER = 0.05
SPRITE_SCALE_PLANETS = 0.5
SPRITE_SCALE_BOX = 1


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

        # Set up the player info
        self.player_sprite = None
        #
        # # Don't show the mouse cursor
        # self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.planet_list = arcade.SpriteList()
        self.projectile_list = arcade.SpriteList()

        # Set up planets
        planet1 = arcade.Sprite("images/planet_01.png", scale=SPRITE_SCALE_PLANETS)
        planet1.center_x = 600
        planet1.center_y = 300

        planet2 = arcade.Sprite("images/planet_02.png", scale=SPRITE_SCALE_PLANETS)
        planet2.center_x = 200
        planet2.center_y = 300

        self.planet_list.append(planet1)
        self.planet_list.append(planet2)

        # Set up the player
        self.player_sprite = arcade.Sprite("images/character.png", scale=SPRITE_SCALE_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Draw everything """
        arcade.start_render()
        self.player_list.draw()
        self.planet_list.draw()
        self.projectile_list.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_mouse_press(self, x, y, button, modifiers):
        projectile = arcade.Sprite("images/box.png", scale=SPRITE_SCALE_BOX)
        projectile.center_x = x
        projectile.center_y = y
        projectile.velocity = (random.random(), random.random())

        self.projectile_list.append(projectile)

    def on_update(self, delta_time):
        """ Movement and game logic """

        # Generate a list of all sprites that collided with the player.
        planet_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.planet_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        for planet in planet_hit_list:
            planet.remove_from_sprite_lists()




def main():
    """ Main method """
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()