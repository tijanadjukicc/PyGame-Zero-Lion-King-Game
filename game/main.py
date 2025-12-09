import random

from actors import *

score = 0
coins = []
coins_timeout = 0

chameleons = []
chameleons_timeout = 0

# next_coin_spawn = random.randint(120, 3000)
# next_chameleon_spawn = random.randint(300, 4000)

WIDTH = 600
HEIGHT = 338

STATE_WELCOME = 0
STATE_RUNNING = 1
STATE_PAUSE = 2
STATE_MENU = 3
STATE_GAME_OVER = 4

state = STATE_WELCOME

bg = Actor('backgrounds/welcome')

logo = StaticActor('logo3', (300, 40))

simba = Simba('characters/young_simba/idle/idle1',(180, 260), [])
hyena = Hyena('characters/hyenas/snapping/1', (-1500, -1000), [])
bird = Bird('characters/eagle/flying/flying1', (800, 100), [])

home_icon = StaticActor("icons/home", (40, 40))
play_icon = StaticActor("icons/play", (40, 40))
quit_icon = StaticActor("icons/exit", (550, 40))

sound_icon = SoundIcon("icons/sound_on", (510, 40), "welcome", True)
game_over_sound_played = False

def reset_the_game():
    global score
    global state
    global bg
    global chameleons
    global coins

    bg = Actor('backgrounds/welcome')

    score = 0

    bird.move((800, 100))
    hyena.move((-1500, -1000))
    hyena.laughed = False

    chameleons = []
    coins = []

    simba.move((180, 260))
    simba.go_to_idle()

    sound_icon.change_song("welcome")

    state = STATE_WELCOME

def start_running():
    global state, coins_timeout

    screen.clear()
    bg.image = "backgrounds/running"
    bg.pos = (WIDTH // 2, HEIGHT // 2)

    sound_icon.change_song("running")

    simba.run()

    coins_timeout = 0

    state = STATE_RUNNING


def update_game_over():
    global game_over_sound_played
    global coins

    # hiding coins
    coins = []

    # game over sound effects
    if not game_over_sound_played and sound_icon.sound_on:
        sounds.simba_hit.play()
        game_over_sound_played = True

    simba.game_over()


def update_running():
    global state
    global score
    global game_over_sound_played
    global coins_timeout
    global chameleons_timeout

    coins_timeout += 1

    # generating new coins
    if coins_timeout > random.randint(120, 3000):
        coins.append(Coin('awards/coins/coin1', (random.randint(600, 1200), random.randint(50, 250))))
        coins_timeout = 0

    for coin in coins:
        # coin collection
        if coin.is_visible and simba.colliderect(coin):
            coin.hide()

            score +=1

            if sound_icon.sound_on:
                sounds.coin_collect.play()

    # remove coins that have passed
    for coin in coins:
        if coin.is_visible and coin.x < -50:
            coins.remove(coin)

    chameleons_timeout += 1

    if chameleons_timeout > random.randint(120, 3000):
        chameleons.append(
            Chameleon('characters/chameleon/walking/1',
                      (random.randint(600, 3000), 260),
                      [])
        )
        chameleons_timeout = 0

    for chameleon in chameleons:
        if chameleon.is_visible and simba.colliderect(chameleon):
            if not chameleon.played_sound and sound_icon.sound_on:
                sounds.chameleon_collision.play()
                chameleon.played_sound = True

            if not chameleon.deducted_points:
                score -= 1
                chameleon.deducted_points = True

    for chameleon in chameleons:
        if chameleon.x < -50:
            chameleons.remove(chameleon)


    # play hyenas sound when she appears
    if not hyena.laughed and hyena.x < 600 and sound_icon.sound_on:
        sounds.hyenas_laugh.set_volume(1.0)
        sounds.hyenas_laugh.play()
        hyena.laughed = True

    # finish the game if simba and hyena collided
    if hyena.colliderect(simba):
        state = STATE_GAME_OVER
        sound_icon.change_song('game_over')
        game_over_sound_played = False


def on_mouse_down(pos):
    global state

    if sound_icon.collidepoint(pos):
        sound_icon.toggle_sound()

    if quit_icon.collidepoint(pos):
        quit()

    if state == STATE_WELCOME and play_icon.collidepoint(pos):
        start_running()

    if state == STATE_GAME_OVER and home_icon.collidepoint(pos):
        reset_the_game()


def update():
    simba.update()
    # bird.update()
    # hyena.update()

    if state == STATE_RUNNING:
        bird.update()
        hyena.update()

        for coin in coins:
            coin.update()

        for chameleon in chameleons:
            chameleon.update()

    if keyboard.space and state == STATE_WELCOME:
        start_running()

    elif state == STATE_RUNNING:
        update_running()

    elif state == STATE_GAME_OVER:
        update_game_over()


def draw():
    bg.draw()

    if state == STATE_WELCOME:
        logo.draw()
        play_icon.draw()

        screen.draw.text("press space to start", (150, 150), fontname="public_pixel", fontsize=15)

    elif state == STATE_RUNNING:
        bird.draw()
        hyena.draw()

        for chameleon in chameleons:
            chameleon.draw()

        for coin in coins:
            if coin.is_visible:
                coin.draw()


        screen.draw.text(f'Score: {score}', (20, 20), fontname="lion_king", fontsize=18, color=(255, 245, 156))

    elif state == STATE_GAME_OVER:
        home_icon.draw()

        screen.draw.text("GAME OVER", (120, 120), fontname="public_pixel", fontsize=40)
        screen.draw.text(f'score: {score}', (228, 170), fontname="public_pixel", fontsize=18)

    simba.draw()

    quit_icon.draw()
    sound_icon.draw()
