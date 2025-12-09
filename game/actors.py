from pgzero.actor import Actor
from pgzero import music
from pgzero.keyboard import keyboard
import random


class AnimatedActor(Actor):
    def __init__(self, image, pos, frames, speed=9, play_once=False):
        super().__init__(image, pos)
        self.frames = frames
        self.index = 0
        self.speed = speed
        self.timer = 0
        self.play_once = play_once

    def animate(self):
        self.timer += 1
        if self.timer >= self.speed and len(self.frames) > 0:
            self.timer = 0

            if not (self.play_once and self.index + 1 >= len(self.frames)):
                self.index = (self.index + 1) % len(self.frames)
                self.image = self.frames[self.index]

    def move(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class StaticActor(Actor):
    def __init__(self, image, pos):
        super().__init__(image, pos)

    def move(self, pos):
        self.x = pos[0]
        self.y = pos[1]


class Simba(AnimatedActor):
    def __init__(self, image, pos, frames):
        super().__init__(image, pos, frames, speed=5)

        self.go_to_idle()

        self.is_jumping = False
        self.is_long_jumping = False
        self.velocity_y = 0
        self.gravity = 0.5
        self.ground_y = 260
        self.game_running = False

    def update(self):
        self.animate()

        if not self.game_running:
            return

        if not self.is_jumping:
            if keyboard.up:
                self.is_jumping = True
                self.velocity_y = -9
                self.jump()
        else:
            if not self.is_long_jumping:
                if keyboard.w:
                    self.velocity_y = -13
                    self.is_long_jumping = True

            self.y += self.velocity_y
            self.velocity_y += self.gravity

            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.is_jumping = False
                self.is_long_jumping = False
                self.run()

    def jump(self):
        self.game_running = True
        self.play_once = False

        self.frames = [
            'characters/young_simba/jumping/jumping1',
            'characters/young_simba/jumping/jumping2',
            'characters/young_simba/jumping/jumping3',
            'characters/young_simba/jumping/jumping4',
            'characters/young_simba/jumping/jumping5',
            'characters/young_simba/jumping/jumping6',
            'characters/young_simba/jumping/jumping8',
            'characters/young_simba/jumping/jumping9'
        ]

    def game_over(self):
        self.game_running = False
        self.play_once = True
        self.speed = 10
        self.y = 260

        self.frames = [
            'characters/young_simba/game_over/1',
            'characters/young_simba/game_over/2',
            'characters/young_simba/game_over/3',
            'characters/young_simba/game_over/4',
            'characters/young_simba/game_over/5',
            'characters/young_simba/game_over/6',
            'characters/young_simba/game_over/7',
            'characters/young_simba/game_over/8',
            'characters/young_simba/game_over/9',
            'characters/young_simba/game_over/10',
            'characters/young_simba/game_over/11',
            'characters/young_simba/game_over/12'
        ]

    def run(self):
        self.game_running = True
        self.play_once = False

        self.speed = 6
        self.frames = [
            'characters/young_simba/running/running1',
            'characters/young_simba/running/running2',
            'characters/young_simba/running/running3',
            'characters/young_simba/running/running4',
            'characters/young_simba/running/running5',
            'characters/young_simba/running/running6',
            'characters/young_simba/running/running7'
        ]

    def go_to_idle(self):
        self.game_running = False
        self.play_once = False
        self.speed = 5

        self.frames = [
            'characters/young_simba/idle/idle1',
            'characters/young_simba/idle/idle2',
            'characters/young_simba/idle/idle3',
            'characters/young_simba/idle/idle4',
            'characters/young_simba/idle/idle5',
            'characters/young_simba/idle/idle6',
            'characters/young_simba/idle/idle7',
            'characters/young_simba/idle/idle8',
            'characters/young_simba/idle/idle9'
        ]


class Bird(AnimatedActor):
    def __init__(self, image, pos, frames):
        super().__init__(image, pos, frames, 6)
        self.frames = frames
        self.frames = [
            'characters/eagle/flying/flying1',
            'characters/eagle/flying/flying2',
            'characters/eagle/flying/flying3',
            'characters/eagle/flying/flying4',
            'characters/eagle/flying/flying5',
            'characters/eagle/flying/flying6'
        ]

    def update(self):
        self.animate()

        if self.x > -70:
            self.x -= 2
        else:
            self.x = random.randint(1200, 3000)
            self.y = 100


class Hyena(AnimatedActor):
    def __init__(self, image, pos, frames):
        super().__init__(image, pos, frames, 3)
        self.frames = frames
        self.frames = [
            'characters/hyenas/running/1',
            'characters/hyenas/running/2',
            'characters/hyenas/running/3',
            'characters/hyenas/running/4',
            'characters/hyenas/running/5',
            'characters/hyenas/running/6',
            'characters/hyenas/running/7',
            'characters/hyenas/running/8',
            'characters/hyenas/running/9',
            'characters/hyenas/running/10',
            'characters/hyenas/running/11',
            'characters/hyenas/running/12',
            'characters/hyenas/running/13',
            'characters/hyenas/running/14'
        ]
        self.laughed = False

    def update(self):
        self.animate()

        if self.x > -70:
            self.x -= 5
        else:
            self.x = random.randint(2000, 5000)
            self.y = 230

            self.laughed = False


class Chameleon(AnimatedActor):
    def __init__(self, image, pos, frames):
        super().__init__(image, pos, frames, 7)
        self.frames = frames
        self.frames = [
            'characters/chameleon/walking/1',
            'characters/chameleon/walking/2',
            'characters/chameleon/walking/3',
            'characters/chameleon/walking/4',
            'characters/chameleon/walking/5',
            'characters/chameleon/walking/6',
            'characters/chameleon/walking/7'
        ]
        self.played_sound = False
        self.is_visible = True
        self.deducted_points = False

    def update(self):
        self.animate()

        if self.x > -70:
            self.x -= 2
        else:
            self.x = random.randint(600, 2000)
            self.y = 200

            self.played_sound = False
            self.is_visible = True
            self.deducted_points = False

    def hide(self):
        self.is_visible = False


class Coin(AnimatedActor):
    def __init__(self, image, pos):
        super().__init__(image, pos, [
            'awards/coins/coin1',
            'awards/coins/coin2',
            'awards/coins/coin3',
            'awards/coins/coin4',
            'awards/coins/coin5',
            'awards/coins/coin6',
            'awards/coins/coin7'
        ])
        self.is_visible = True

    def update(self):
        self.animate()

        if self.is_visible:
            if self.x > -50:
                self.x -= 5
            else:
                self.x = random.randint(1000, 3000)
                self.y = random.randint(50, 250)

                self.is_visible = True

    def hide(self):
        self.is_visible = False

class SoundIcon(Actor):
    def __init__(self, image, pos, song, sound_on):
        super().__init__(image, pos)
        self.song = song
        self.sound_on = sound_on

        if sound_on:
            music.play(song)

    def toggle_sound(self):
        if self.sound_on:
            music.stop()
            self.image = "icons/sound_off"
        else:
            music.play(self.song)
            self.image = "icons/sound_on"

        self.sound_on = not self.sound_on

    def change_song(self, new_song):
        self.song = new_song

        music.stop()

        if self.sound_on:
            music.play(self.song)
