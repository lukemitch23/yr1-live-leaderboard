import pyglet
import random
from pyglet.window import key, mouse
from OutputLeaderboard import *

class GameConfig:
    def __init__(self):
        self.width = 720
        self.height = 1080
        self.resource_path = 'resources'
        self.font_path = 'resources/fonts/Pixeltype.ttf'
        self.shared_state = SharedState()

        # Resource path
        pyglet.resource.path = [self.resource_path]
        pyglet.resource.reindex()

difficulty_settings = {
    'easy': {'num_faults': 1},
    'medium': {'num_faults': 2},
    'hard': {'num_faults': 3}
}

class SharedState:
    def __init__(self):
        self.time = 60
        self.game_state = 'start'
        self.difficulty = 'easy'
        self.num_faults = difficulty_settings[self.difficulty]['num_faults']
        self.total_score = 0

    def update_difficulty(self, difficulty):
        self.difficulty = difficulty
        self.num_faults = difficulty_settings[difficulty]['num_faults']

    def update_game_state(self, new_state):
        self.game_state = new_state

    def print_game_state(self, dt):
        print(f"Game State: {self.game_state}, Difficulty: {self.difficulty}, Time: {self.time}, Total Score: {self.total_score}")

class Render:
    def __init__(self, game_config, width, height):
        self.game_config = game_config
        self.shared_state = game_config.shared_state
        display = pyglet.display.get_display()
        screens = display.get_screens()
        self.screen = screens[0]
        self.width = width
        self.height = height
        self.window = pyglet.window.Window(width=self.width, height=self.height, screen=self.screen)
        self.window.set_location(self.screen.x, self.screen.y)
        self.start_batch = pyglet.graphics.Batch()
        self.game_batch = pyglet.graphics.Batch()
        self.quiz_batch =pyglet.graphics.Batch()
        self.end_batch = pyglet.graphics.Batch()


    def update(self, dt):
        pass

    def batch_add_sprite(self, image, name, move_x, move_y, batch):
        img = pyglet.resource.image(image)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        sprite = pyglet.sprite.Sprite(img, x=move_x, y=move_y, batch=batch)
        setattr(self, name, sprite)
        print(f"Sprite {name} added at ({move_x}, {move_y})")
        return sprite

    def load_and_anchor_image(self, image):
        img = pyglet.resource.image(image)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        return img
    
    def batch_add_label(self, text, size, name, batch):
        label = pyglet.text.Label(text,
                                  font_name='Arial',
                                  font_size=size,
                                  x=self.width // 2, y=self.height // 2,
                                  anchor_x='center', anchor_y='center', batch=batch)
        setattr(self, name, label)

    def update_batch(self, batch):
        batch = pyglet.graphics.Batch()


class Window(Render):
    def __init__(self, game_config, width, height):
        super().__init__(game_config, width, height)

    def on_draw(self):
        self.window.clear()
        if self.shared_state.game_state == 'start':
            self.start_batch.draw()
        elif self.shared_state.game_state == 'game':
            self.game.background_sprite.draw()  # Draw the background image first
            self.game_batch.draw()
            self.game.draw_hitbox()  # Draw hitbox for the bolt
            for fault in self.game.faults:
                fault.draw_hitbox()  # Draw hitbox for each fault
        elif self.shared_state.game_state == 'quiz':
            self.quiz_batch.draw()
        elif self.shared_state.game_state == 'end':
            self.end_batch.draw()
            self.send_score.draw()



class StartScreen:
    def __init__(self, render, game_config):
        self.render = render
        self.game_config = game_config
        self.shared_state = game_config.shared_state
        self.start_batch = render.start_batch
        self.background = pyglet.shapes.Rectangle(x=0, y=0, width=720, height=1080, color=(50, 50, 255),
                                                  batch=self.start_batch)
        
        # Load images and set anchors to center using the new method
        self.easyup_img = self.render.load_and_anchor_image('loads/easy button up.png')
        self.easydown_img = self.render.load_and_anchor_image('loads/easy button down.png')
        self.medup_img = self.render.load_and_anchor_image('loads/medium button up.png')
        self.meddown_img = self.render.load_and_anchor_image('loads/medium button down.png')
        self.hardup_img = self.render.load_and_anchor_image('loads/hard button up.png')
        self.harddown_img = self.render.load_and_anchor_image('loads/hard button down.png')
        self.plane_img = self.render.load_and_anchor_image('moveable sprites/plane.png')
        self.title_img = self.render.load_and_anchor_image('logo.png')

        # Create sprites using batch_add_sprite method
        self.easyup_sprite = self.render.batch_add_sprite('loads/easy button up.png', 'easyup_sprite', 180, game_config.height * 0.3, self.start_batch)
        self.medup_sprite = self.render.batch_add_sprite('loads/medium button up.png', 'medup_sprite', 360, game_config.height * 0.3, self.start_batch)
        self.hardup_sprite = self.render.batch_add_sprite('loads/hard button up.png', 'hardup_sprite', 540, game_config.height * 0.3, self.start_batch)
        self.plane_sprite = self.render.batch_add_sprite('moveable sprites/plane.png', 'plane_sprite', 0, 400, self.start_batch)
        self.title_sprite = self.render.batch_add_sprite('logo.png', 'title_sprite', game_config.width / 2, game_config.height * 0.9, self.start_batch)

        self.plane_sprite.scale = 1.5
        self.plane_speed = 200
        self.plane_direction = 1
        self.title_sprite.scale = 4

        self.labels = [
            pyglet.text.Label('Press 1 for Easy',
                              font_name='Pixeltype',
                              font_size=34,
                              x=self.render.width // 2, y=(self.render.height // 2) + 100,
                              anchor_x='center', anchor_y='center',
                              batch=self.start_batch),
            pyglet.text.Label('Press 2 for Medium',
                              font_name='Pixeltype',
                              font_size=34,
                              x=self.render.width // 2, y=self.render.height // 2,
                              anchor_x='center', anchor_y='center',
                              batch=self.start_batch),
            pyglet.text.Label('Press 3 for Hard',
                              font_name='Pixeltype',
                              font_size=34,
                              x=self.render.width // 2, y=(self.render.height // 2) - 100,
                              anchor_x='center', anchor_y='center',
                              batch=self.start_batch)
        ]

        # selected button state
        self.selected_button = 'easy'
        self.cooldown_timer = 0
        self.update_selected_button()

    def batch_add_sprite(self, image, name, move_x, move_y):
        img = pyglet.resource.image(image)
        img.anchor_x = img.width // 2
        img.anchor_y = img.height // 2
        sprite = pyglet.sprite.Sprite(img, x=move_x, y=move_y, batch=self.start_batch)
        setattr(self, name, sprite)
        print(f"Sprite {name} added at ({move_x}, {move_y})")
        return sprite

    def update_selected_button(self):
        if self.selected_button == 'easy':
            self.easyup_sprite.image = self.easydown_img
            self.medup_sprite.image = self.medup_img
            self.hardup_sprite.image = self.hardup_img
        elif self.selected_button == 'medium':
            self.easyup_sprite.image = self.easyup_img
            self.medup_sprite.image = self.meddown_img
            self.hardup_sprite.image = self.hardup_img
        elif self.selected_button == 'hard':
            self.easyup_sprite.image = self.easyup_img
            self.medup_sprite.image = self.medup_img
            self.hardup_sprite.image = self.harddown_img


    def on_key_press(self, symbol, modifiers):
        if self.cooldown_timer <= 0:
            if symbol == key.ENTER:
                self.shared_state.game_state = 'game'
                self.render.window.state = 'game'
            elif symbol == key._1:
                self.shared_state.update_difficulty('easy')
                self.shared_state.game_state = 'game'
                self.render.window.state = 'game'
            elif symbol == key._2:
                self.shared_state.update_difficulty('medium')
                self.shared_state.game_state = 'game'
                self.render.window.state = 'game'
            elif symbol == key._3:
                self.shared_state.update_difficulty('hard')
                self.shared_state.game_state = 'game'
                self.render.window.state = 'game'
            elif symbol == key.RIGHT:
                if self.selected_button == 'easy':
                    self.selected_button = 'medium'
                elif self.selected_button == 'medium':
                    self.selected_button = 'hard'
                self.update_selected_button()
                self.cooldown_timer = 0.2
            elif symbol == key.LEFT:
                if self.selected_button == 'hard':
                    self.selected_button = 'medium'
                elif self.selected_button == 'medium':
                    self.selected_button = 'easy'
                self.update_selected_button()
                self.cooldown_timer = 0.2

    def update(self, dt):
        if self.cooldown_timer > 0:
            self.cooldown_timer -= dt

        # update plane position
        self.plane_sprite.x += self.plane_speed * self.plane_direction * dt

        # check if plane goes off screen
        if self.plane_sprite.x > self.game_config.width + 100 or self.plane_sprite.x < -100:
            self.plane_direction *= -1  # flip speed
            self.plane_sprite.y = random.randint(0, self.game_config.height)
            self.plane_sprite.image = self.plane_img.get_transform(
                flip_x=True) if self.plane_direction == -1 else self.plane_img

            

class GameController(Window):
    def __init__(self, game_config, width, height):
        super().__init__(game_config, width, height)
        self.start_screen = StartScreen(self, game_config)
        self.batch_add_label(f'Timer: {self.shared_state.time}', 36, 'label', self.start_batch)
        self.game = Game(self, game_config, width, height)  # Initialize the Game instance
        self.quiz = Quiz(self, game_config)  # Initialize the Quiz instance

    def on_key_press(self, symbol, modifiers):
        self.start_screen.on_key_press(symbol, modifiers)
        if self.shared_state.game_state == 'game':
            self.start_timer()
        elif self.shared_state.game_state == 'quiz':
            self.quiz.on_key_press(symbol, modifiers)

    def start_timer(self):
        self.update_batch(self.game_batch)
        self.window.push_handlers(self.game)  # Push handlers for the Game instance
        self.game.start_timer()

    def update(self, dt):
        if self.shared_state.game_state == 'start':
            self.start_screen.update(dt)
        elif self.shared_state.game_state == 'game':
            self.game.update(dt)
        elif self.shared_state.game_state == 'quiz':
            pass

    def reset_game(self):
        print("reset_game method triggered")  # Print statement to test if the method is triggered
        self.game.bolt.x = self.game_config.width // 2
        self.game.bolt.y = self.game_config.height - 200
        self.game.bolt_speed_y = 0
        self.game.x_speed = 0
        self.game.is_dropping = False
        self.game.directions = {'right': False, 'left': False}
        self.game.faults = []
        self.game.fault_timer = 0
        self.game.cooldown_timer = 0
        self.game.start_timer()
        #self.shared_state.time = 60  # Reset the timer
        self.shared_state.update_game_state('game')
         


class ScoredRectangle:
    def __init__(self, render, x, y, width, height, batch, scoring_window):
        self.render = render
        self.rect = pyglet.shapes.Rectangle(x, y, width, height, color=(255, 0, 0, 128), batch=batch)
        self.score = 0
        self.label = pyglet.text.Label(
            text=str(self.score), font_name='Pixeltype', font_size=24,
            x=x + width / 2, y=y + height / 2, anchor_x='center', anchor_y='center',
            batch=batch)

        self.dark_sprites = []

        self.bolt_dark_img = self.render.load_and_anchor_image('moveable sprites/dark_bolt_new.png')
        self.mini_bolt_img = self.render.load_and_anchor_image('moveable sprites/bolt_new.png')
        self.fault_img = self.render.load_and_anchor_image('moveable sprites/fault_new.png')

        self.colors = [(255, 0, 0, 180), (255, 85, 0, 180), (255, 170, 0, 180), (170, 255, 0, 180), (85, 255, 0, 180),
                       (0, 255, 0, 180)]
        self.create_dark_img(x, y, width, height, batch)
        self.scoring_window = scoring_window

    def create_dark_img(self, x, y, width, height, batch):
        dark_width = self.bolt_dark_img.width * 0.25
        total_dark_width = 5 * dark_width
        av_width = width - total_dark_width
        spacing = av_width / 6
        for i in range(5):
            dark_x = x + spacing + i * (dark_width + spacing)
            dark_y = y + 50
            dark_sprite = pyglet.sprite.Sprite(self.bolt_dark_img, x=dark_x, y=dark_y, batch=batch)
            dark_sprite.scale = 0.25
            self.dark_sprites.append(dark_sprite)

    def check_collision(self, bolt_bottom_center_x, bolt_bottom_center_y):
        if self.rect.x < bolt_bottom_center_x < self.rect.x + self.rect.width and self.rect.y < bolt_bottom_center_y < self.rect.y + self.rect.height:
            if self.score < 5:
                self.score += 1
                self.label.text = str(self.score)
                self.update_colour()
                self.update_sprites()

            else:
                self.score = 3

            self.scoring_window.update_total_score()

    def update_colour(self):
        self.rect.color = self.colors[self.score]

    def update_sprites(self):
        for i in range(5):
            if self.score > i:
                self.dark_sprites[i].image = self.mini_bolt_img
                self.dark_sprites[i].scale = 0.25
            else:
                self.dark_sprites[i].image = self.bolt_dark_img
                self.dark_sprites[i].scale = 0.25

    def deplete_score(self):
        if self.score > 0:
            self.score -= 1
            self.label.text = str(self.score)
            self.update_colour()
            self.update_sprites()

    def draw(self):
        self.rect.draw()
        for sprite in self.dark_sprites:
            sprite.draw()

    def draw_hitbox(self):
        lines = [
            pyglet.shapes.Line(self.rect.x, self.rect.y, self.rect.x + self.rect.width, self.rect.y, color=(0, 255, 0)),
            pyglet.shapes.Line(self.rect.x, self.rect.y, self.rect.x, self.rect.y + self.rect.height,
                               color=(0, 255, 0)),
            pyglet.shapes.Line(self.rect.x + self.rect.width, self.rect.y, self.rect.x + self.rect.width,
                               self.rect.y + self.rect.height, color=(0, 255, 0)),
            pyglet.shapes.Line(self.rect.x, self.rect.y + self.rect.height, self.rect.x + self.rect.width,
                               self.rect.y + self.rect.height, color=(0, 255, 0))
        ]
        for line in lines:
            line.opacity = 100
            line.draw()

    def get_score(self):
        return self.score


class Fault:

    move_durartion = 3
    still_duration = 10

    def __init__(self, x, y, width, height, batch, image_path):
        self.fault = pyglet.sprite.Sprite(pyglet.resource.image(image_path), x=x, y=y, batch=batch)
        self.fault.scale = 0.8
        self.speed_x = 0
        self.speed_y = 0
        self.state = 'stationary'  # Add state attribute to track 'moving' or 'stationary'
        self.cooldown_timer = Fault.still_duration  # Add cooldown_timer attribute

    def update_position(self, dt, window_width, window_height, faults):
        if self.state == 'moving':
            self.fault.x += self.speed_x * dt
            self.fault.y += self.speed_y * dt

            # Check collision with edges
            if self.fault.x < self.fault.width or self.fault.x + self.fault.width > window_width:
                self.speed_x *= -1
            if self.fault.y < 250 or self.fault.y + self.fault.height > window_height:
                self.speed_y *= -1

            # Check collision with other faults
            for other_fault in faults:
                if other_fault != self and self.check_collision(self.fault, other_fault.fault):
                    self.handle_fault_collision(other_fault)

            # Update movement duration
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.speed_x = 0
                self.speed_y = 0
                self.state = 'stationary'
                self.cooldown_timer = Fault.still_duration  # Set stationary period to 3 seconds

        elif self.state == 'stationary':
            self.cooldown_timer -= dt
            if self.cooldown_timer <= 0:
                self.start_moving()

    def start_moving(self):
        if self.state == 'stationary':
            self.speed_x = random.choice([-10, 10])
            self.speed_y = random.choice([-10, 10])
            self.state = 'moving'
            self.cooldown_timer = Fault.move_durartion  # Set moving duration to 5 seconds

    def check_collision(self, sprite1, sprite2):
        return (sprite1.x < sprite2.x + sprite2.width and
                sprite1.x + sprite1.width > sprite2.x and
                sprite1.y < sprite2.y + sprite2.height and
                sprite1.y + sprite1.height > sprite2.y)

    def handle_fault_collision(self, other_fault):
        # Calculate overlaps
        overlap_left = self.fault.x + self.fault.width - other_fault.fault.x
        overlap_right = other_fault.fault.x + other_fault.fault.width - self.fault.x
        overlap_top = other_fault.fault.y + other_fault.fault.height - self.fault.y
        overlap_bottom = self.fault.y + self.fault.height - other_fault.fault.y

        # Determine the smallest overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_top or min_overlap == overlap_bottom:
            self.speed_y *= -1
            other_fault.speed_y *= -1
        elif min_overlap == overlap_left or min_overlap == overlap_right:
            self.speed_x *= -1
            other_fault.speed_x *= -1

    def draw_hitbox(self):
        lines = [
            pyglet.shapes.Line(self.fault.x - self.fault.width // 2, self.fault.y - self.fault.height // 2, self.fault.x + self.fault.width // 2, self.fault.y - self.fault.height // 2, color=(255, 0, 0)),
            pyglet.shapes.Line(self.fault.x - self.fault.width // 2, self.fault.y - self.fault.height // 2, self.fault.x - self.fault.width // 2, self.fault.y + self.fault.height // 2, color=(255, 0, 0)),
            pyglet.shapes.Line(self.fault.x + self.fault.width // 2, self.fault.y - self.fault.height // 2, self.fault.x + self.fault.width // 2, self.fault.y + self.fault.height // 2, color=(255, 0, 0)),
            pyglet.shapes.Line(self.fault.x - self.fault.width // 2, self.fault.y + self.fault.height // 2, self.fault.x + self.fault.width // 2, self.fault.y + self.fault.height // 2, color=(255, 0, 0))
        ]
        for line in lines:
            line.opacity = 100
            line.draw()

class Game:
    def __init__(self, render, game_config, width, height):
        self.render = render
        self.game_config = game_config
        self.shared_state = game_config.shared_state
        self.render.batch_add_label(f'Timer: {self.shared_state.time}', 36, 'label', self.render.game_batch)
        self.timer_running = False
        self.rectangles = []
        self.faults = []
        self.gravity = -300
        self.bolt_speed_y = 0
        self.x_speed = 0
        self.cooldown_timer = 0  # Add cooldown_timer attribute
        self.is_dropping = False
        self.directions = {'right': False, 'left': False}
        self.create_rectangles()
        self.fault_image = self.render.load_and_anchor_image('moveable sprites/fault_new.png')
        self.bolt = self.render.batch_add_sprite('moveable sprites/bolt_new.png', 'bolt', width // 2, height - 200, self.render.game_batch)
        self.fault_timer = 0 
        self.fault_interval = 3
        self.num_faults_created = 0

        # Load and anchor background image
        self.background_img = self.render.load_and_anchor_image('backgrounds/bg new.png')
        self.background_sprite = pyglet.sprite.Sprite(self.background_img, x=width/2, y=height/2)
        self.background_sprite.scale_x = width / self.background_img.width
        self.background_sprite.scale_y = height / self.background_img.height

        # Schedule the print method to run every second
        #pyglet.clock.schedule_interval(self.print_bolt_state, 1.0)

    def create_rectangles(self):
        num_rect = 3
        rect_width = self.render.width / num_rect - 1
        rect_height = self.render.height / 5
        for i in range(num_rect):
            x = i * (rect_width + 5)
            y = 0
            scored_rect = ScoredRectangle(self.render, x, y, rect_width, rect_height, self.render.game_batch, self)
            self.rectangles.append(scored_rect)

    def create_fault(self):
        while True:
            x = random.randint(0, self.render.width - self.fault_image.width)
            y = random.randint(200, self.render.height - self.fault_image.height - 300)
            new_fault = Fault(x, y, self.fault_image.width, self.fault_image.height, self.render.game_batch, 'moveable sprites/fault_new.png')
            
            if not self.check_fault_overlap(new_fault):
                self.faults.append(new_fault)
                break

    def check_fault_overlap(self, new_fault):
        for fault in self.faults:
            if self.check_collision(new_fault.fault, fault.fault):
                return True
        return False

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            self.render.window.close()
        if self.shared_state.game_state == 'game':
            if symbol == key.SPACE and not self.is_dropping:
                self.bolt_speed_y = -10
                self.is_dropping = True
            if symbol == key.LEFT:
                self.directions['left'] = True
            elif symbol == key.RIGHT:
                self.directions['right'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.LEFT:
            self.directions['left'] = False
        elif symbol == key.RIGHT:
            self.directions['right'] = False

    def start_timer(self):
        if not self.timer_running:
            self.timer_running = True
            pyglet.clock.schedule_interval(self.update_timer, 1.0)
            print("Timer restarted!")

    def update_timer(self, dt):
        if self.shared_state.game_state == 'game':
            self.shared_state.time -= 1
            if self.shared_state.time <= 0:
                self.shared_state.time = 0
                pyglet.clock.unschedule(self.update_timer)
                self.render.update_batch(self.render.end_batch)
                self.render.batch_add_label('End of Game', 36, 'label', self.render.end_batch)
                self.shared_state.update_game_state('end')
            elif self.shared_state.time == 40:  # Transition to quiz state after 20 seconds
                self.shared_state.update_game_state('quiz')
                self.timer_running = False
                self.render.update_batch(self.render.quiz_batch)
                self.render.batch_add_label('Quiz Time! Press 1, 2, or 3', 36, 'label', self.render.quiz_batch)
                pyglet.clock.unschedule(self.update_timer)  # Pause the timer during quiz
        else:
            self.render.batch_add_label(f'Timer: {self.shared_state.time}', 36, 'label', self.render.game_batch)

    def update(self, dt):
        if self.shared_state.game_state == 'game':
            if self.cooldown_timer > 0:
                self.cooldown_timer -= dt
            else:
                if self.directions['right']:
                    self.x_speed = 500
                elif self.directions['left']:
                    self.x_speed = -500
                else:
                    self.x_speed = 0

            self.bolt.x += self.x_speed * dt

            if self.bolt.x < 0:
                self.bolt.x = self.render.width
            elif self.bolt.x > self.render.width:
                self.bolt.x = 0

            if self.is_dropping:
                self.bolt_speed_y += self.gravity * dt
                self.bolt.y += self.bolt_speed_y * dt

                bolt_bottom_center_x = self.bolt.x + self.bolt.width / 2
                bolt_bottom_center_y = self.bolt.y

                if self.bolt.y <= 0 + self.bolt.height - 50:
                    for scored_rect in self.rectangles:
                        scored_rect.check_collision(bolt_bottom_center_x, bolt_bottom_center_y)
                    self.bolt.y = self.render.height - 200
                    self.is_dropping = True
                    self.bolt_speed_y = 0
                    self.gravity = -300

                if self.bolt and self.bolt.y > 0:
                    self.bolt.y -= 10 * dt

            # Check collision with fault_sprite
            for fault in self.faults:
                if self.check_collision(self.bolt, fault.fault):
                    self.handle_bolt_fault_collision(fault)

            # generate new faults
            self.update_faults(dt)

            # Move faults
            self.moving_faults(dt)

    def moving_faults(self, dt):
        if len(self.faults) == self.shared_state.num_faults:
            for fault in self.faults:
                fault.update_position(dt, self.game_config.width, self.game_config.height, self.faults)

    def update_faults(self, dt):
        if self.shared_state.game_state == 'game':
            self.fault_timer += dt

            if self.fault_timer >= self.fault_interval:
                if len(self.faults) < self.shared_state.num_faults:
                    self.create_fault()
                self.fault_timer = 0

    def check_collision(self, sprite1, sprite2):
        return (sprite1.x < sprite2.x + sprite2.width and
                sprite1.x + sprite1.width > sprite2.x and
                sprite1.y < sprite2.y + sprite2.height and
                sprite1.y + sprite1.height > sprite2.y)

    def handle_bolt_fault_collision(self, fault):
        bolt = self.bolt
        bolt_left = bolt.x - bolt.width // 2
        bolt_right = bolt.x + bolt.width // 2
        bolt_top = bolt.y + bolt.height // 2
        bolt_bottom = bolt.y - bolt.height // 2

        fault_left = fault.fault.x - fault.fault.width // 2
        fault_right = fault.fault.x + fault.fault.width // 2
        fault_top = fault.fault.y + fault.fault.height // 2
        fault_bottom = fault.fault.y - fault.fault.height // 2

        # Calculate overlaps
        overlap_left = bolt_right - fault_left
        overlap_right = fault_right - bolt_left
        overlap_top = fault_top - bolt_bottom
        overlap_bottom = bolt_top - fault_bottom

        # Determine the smallest overlap
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)

        if min_overlap == overlap_top:
            self.bolt_speed_y = 400
            print("top collision")
        elif min_overlap == overlap_left:
            self.x_speed = -300  # bounce to the left
            print("left collision, x_speed set to -300")
            self.cooldown_timer = 0.5  # Set cooldown timer to 0.5 seconds
        elif min_overlap == overlap_right:
            self.x_speed = 300  # bounce to the right
            print("right collision, x_speed set to 300")
            self.cooldown_timer = 0.5  # Set cooldown timer to 0.5 seconds

    def draw_hitbox(self):
        lines = [
            pyglet.shapes.Line(self.bolt.x - self.bolt.width // 2, self.bolt.y - self.bolt.height // 2, self.bolt.x + self.bolt.width // 2, self.bolt.y - self.bolt.height // 2, color=(0, 255, 0)),
            pyglet.shapes.Line(self.bolt.x - self.bolt.width // 2, self.bolt.y - self.bolt.height // 2, self.bolt.x - self.bolt.width // 2, self.bolt.y + self.bolt.height // 2, color=(0, 255, 0)),
            pyglet.shapes.Line(self.bolt.x + self.bolt.width // 2, self.bolt.y - self.bolt.height // 2, self.bolt.x + self.bolt.width // 2, self.bolt.y + self.bolt.height // 2, color=(0, 255, 0)),
            pyglet.shapes.Line(self.bolt.x - self.bolt.width // 2, self.bolt.y + self.bolt.height // 2, self.bolt.x + self.bolt.width // 2, self.bolt.y + self.bolt.height // 2, color=(0, 255, 0))
        ]
        for line in lines:
            line.opacity = 100
            line.draw()

    def calculate_total_score(self):
        return sum(rect.get_score() for rect in self.rectangles)

    def update_total_score(self):
        self.shared_state.total_score += self.calculate_total_score()

    def deplete_scores(self, dt):
        valid_rectangles = [rect for rect in self.rectangles if rect.score > 1]
        if valid_rectangles:
            rect = random.choice(valid_rectangles)
            rect.deplete_score()

    def print_bolt_state(self, dt):
        print(f"Bolt Dropping: {self.is_dropping}, Gravity: {self.gravity}, Bolt Position: {self.bolt.y}, Bolt Speed Y: {self.bolt_speed_y}, X Speed: {self.x_speed}, Cooldown Timer: {self.cooldown_timer}")

class Quiz:
    def __init__(self, game_controller, game_config):
        self.game_controller = game_controller
        self.game_config = game_config
        self.shared_state = game_config.shared_state
        self.quiz_batch = pyglet.graphics.Batch()
        self.game_controller.batch_add_label('Quiz Time! Press 1, 2, or 3', 36, 'quiz_label', self.quiz_batch)

    def on_key_press(self, symbol, modifiers):
        if symbol in [key._1, key._2, key._3]:
            self.shared_state.update_game_state('game')
            self.game_controller.reset_game()
            

    def update(self, dt):
        pass

class End(Window):
    def __init__(self, game_config, width, height):
        super().__init__(game_config, width, height)
        self.batch_add_label('End of Game', 36, 'label', self.end_batch)

    def on_key_press(self, symbol, modifiers):
        if symbol == key.ESCAPE:
            print("escape key")
            self.window.close()

    def leaderboard (self):
        send_score = GetData(self.shared_state.total_score)
        send_score.output(self)




if __name__ == "__main__":
    game_config = GameConfig()
    width = 720
    height = 1080  
    game_controller = GameController(game_config, width, height)

    @game_controller.window.event
    def on_draw():
        game_controller.on_draw()

    def update(dt):
        game_controller.update(dt)
        if game_controller.shared_state.game_state == 'game':
            pass

    pyglet.clock.schedule_interval(update, 1/60.0)

    @game_controller.window.event
    def on_key_press(symbol, modifiers):
        game_controller.on_key_press(symbol, modifiers)

    pyglet.clock.schedule_interval(update, 1/60.0)
    pyglet.clock.schedule_interval(game_config.shared_state.print_game_state, 1)  # print game_state every second

    pyglet.app.run()
