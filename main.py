import pygame
from pygame.locals import *
import os
import RPi.GPIO as GPIO
import time
import cursor 
from arrow import * 
from constants import *
from icm20948 import ICM20948
import math
from pygame import mixer
# from music_beats import beat_times
# from music_beats import*

os.putenv('SDL_VIDEODRIVER','fbcon')
os.putenv('SDL_FBDEV','/dev/fb1')
os.putenv('SDL_MOUSEDRV','TSLIB')
os.putenv('SDL_MOUSEDEV','/dev/input/touchscreen')

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)

cursor_dir = NONE
slash_time = time.time()

def gpio17_callback(channel):
    global running
    running = False
    for dir in dirs:
        dir.kill()
    if state == 'RUNNING' or state == 'PAUSE':
        os.system('echo "quit" > /home/pi/final_proj/video_fifo')


def gpio5_callback(channel):
    global cursor_dir
    global slash_time
    cursor_dir = DOWN
    slash_time = time.time()

def gpio6_callback(channel):
    global cursor_dir
    global slash_time
    cursor_dir = UP
    slash_time = time.time()

def gpio13_callback(channel):
    global cursor_dir
    global slash_time
    cursor_dir = RIGHT
    slash_time = time.time()

def gpio19_callback(channel):
    global cursor_dir
    global slash_time
    cursor_dir = LEFT
    slash_time = time.time()

GPIO.add_event_detect(17, GPIO.FALLING, callback=gpio17_callback, bouncetime=300)
GPIO.add_event_detect(5, GPIO.FALLING, callback=gpio5_callback, bouncetime=300)
GPIO.add_event_detect(6, GPIO.FALLING, callback=gpio6_callback, bouncetime=300)
GPIO.add_event_detect(13, GPIO.FALLING, callback=gpio13_callback, bouncetime=300)
GPIO.add_event_detect(19, GPIO.FALLING, callback=gpio19_callback, bouncetime=300)


imu = ICM20948()

# possible states: {START, RUNNING, DONE, PAUSE}
state = 'START' 

score = 0

# init PyGame and set up blank screen
pygame.init()
pygame.mouse.set_visible(False)
screen = pygame.display.set_mode(size)


# Set pygame font
large_font = pygame.font.Font('PixelPowerline-9xOK.ttf',20)
small_font = pygame.font.Font(None,20)

screen.fill(BLACK)

running = True
my_cursor = None

# Arrows structures
dirs = pygame.sprite.Group()
# dirs.add(GetDirArrow())

levels = 0  # adjust to see how frequent the blocks fall?

last_gen_time = time.time()
last_time = time.time()
start = time.time()

runtime = 0
last_runtime = time.time()

start_time = 0

pause_time = 0

move = True

ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
last_roll = 180*math.atan(ax/math.sqrt(ay*ay+az*az))/math.pi

song = 1

high_score_1 = 0
high_score_2 = 0

beat_times = beat_times_1
dur = dur_1

while running:

    if (runtime + time.time()-last_runtime >= dur and state == 'RUNNING'):
        state = 'DONE'
        for dir in dirs:
            dir.kill()
        if song == 1 and score > high_score_1:
            high_score_1 = score
        if song == 2 and score > high_score_2:
            high_score_2 = score
        if running:
            os.system('echo "quit" > /home/pi/final_proj/video_fifo')

    buttons = {}
    ax, ay, az, gx, gy, gz = imu.read_accelerometer_gyro_data()
    roll = 180*math.atan(ay/math.sqrt(ax*ax+az*az))/math.pi

    screen.fill(BLACK)
    if state == 'START':
        # start state - wait for user to press start
        large_text = large_font.render('Pi Saber', True, WHITE)
        small_text = small_font.render('start', True, WHITE)
        buttons['start'] = (160,200)
    if state == 'SELECT':
        large_text = large_font.render('Songs', True, WHITE)
        small_text = small_font.render('start', True, WHITE)
        buttons['song 1'] = (160,170)
        buttons['song 2'] = (160,200)
    if state == 'DONE':
        # win state
        large_text = large_font.render('Game Over', True, WHITE)
        score_text = small_font.render('score: ' + str(score), True, WHITE)
        rect = score_text.get_rect(center=(160,160))
        screen.blit(score_text,rect)
        if song == 1:
            high_score_text = small_font.render('song 1 high score: ' + str(high_score_1), True, WHITE)
            rect = high_score_text.get_rect(center=(160,180))
            screen.blit(high_score_text,rect)
        else: 
            high_score_text = small_font.render('song 2 high score: ' + str(high_score_2), True, WHITE)
            rect = high_score_text.get_rect(center=(160,180))
            screen.blit(high_score_text,rect)
        small_text = small_font.render('replay', True, WHITE)
        buttons['replay'] = (160,210)
    if state == 'PAUSE':
        # pause state
        large_text = large_font.render('Game Paused', True, WHITE)
        small_text = small_font.render('resume', True, WHITE)
        buttons['resume'] = (160,180)
        buttons['quit'] = (160,210)
    if state != 'RUNNING':
        rect = large_text.get_rect(center=(160,120))
        screen.blit(large_text,rect)
        

    else:
        # main game play state
        if (time.time()-start_time > 1000):
            state = 'DONE'
        score_text = small_font.render('score: ' + str(score), True, WHITE)
        rect = score_text.get_rect(center=(30,10))
        screen.blit(score_text,rect)
        buttons['pause'] = (300,10)

        # make arrows fall
        cur_time = time.time()

        time_stamp = round(time.time() - start + fall_time, 2)
        if time.time() - last_gen_time > 2:
            if time_stamp in beat_times:
                last_gen_time = time.time()
                arrow = GetDirArrow()
                dirs.add(arrow)
        
        if(roll > 20):
            if my_cursor.x < 320:
                my_cursor.x += 1 * (roll // 40 + 1) 
                cursor_dir = RIGHT 
            else:
                my_cursor.x = 320

        elif(roll < -20):
            if my_cursor.x > 0:
                my_cursor.x -= 1 * ((-1*roll) // 40 + 1)  
                cursor_dir = LEFT 
            else:
                my_cursor.x = 0
        
        elif (time.time() - slash_time) > 0.25:
            cursor_dir = NONE 
                
        if cur_time - last_time > 0.25:
            move = True
            last_time = time.time()
        else:
            move = False

        #set cursor image:
        my_cursor.set_dir(cursor_dir)

        for dir in dirs:
            if move:
                dir.arrow_move(speed)
            x_collide = abs(dir.rect.x - my_cursor.x) < RADIUS
            
            y_collide = abs(dir.rect.y - my_cursor.y) < RADIUS
                        
            if x_collide and y_collide and not dir.hit:
                if dir.key == UP:
                    if not GPIO.input(6):
                        dir.arrow_hit()
                        score += 10

                if dir.key == DOWN:
                    if not GPIO.input(5):
                        dir.arrow_hit()
                        score += 10

                if dir.key == LEFT: 
                    if not GPIO.input(19):
                        dir.arrow_hit()
                        score += 10

                if dir.key == RIGHT:
                    if not GPIO.input(13):
                        dir.arrow_hit()
                        score += 10

            screen.blit(dir.image, dir.rect)

        
        my_cursor.draw(screen)

    button_rects = {}
    for text,pos in buttons.items():
        small_text = small_font.render(text, True, WHITE)
        rect = small_text.get_rect(center=pos)
        button_rects[text] = rect
        screen.blit(small_text,rect)
    
    for event in pygame.event.get():
        if(event.type is MOUSEBUTTONDOWN):
            pos = pygame.mouse.get_pos()
        elif(event.type is MOUSEBUTTONUP):
            pos = pygame.mouse.get_pos()
            x,y = pos
            for text,rect in button_rects.items():
                if rect.collidepoint(pos):
                    if text == 'start':
                        state = 'SELECT'
                    elif text == 'replay':
                        state = 'START'
                        for dir in dirs:
                            dir.kill()
                    elif text == 'resume':
                        state = 'RUNNING'
                        last_runtime = time.time()
                        os.system('echo "pause" > /home/pi/final_proj/video_fifo')
                        start = start + time.time() - pause_time
                    elif text == 'pause':
                        pause_time = time.time()
                        state = 'PAUSE'
                        runtime = runtime + time.time()-last_runtime
                        os.system('echo "pause" > /home/pi/final_proj/video_fifo')
                    elif text == 'quit':
                        state = 'START'
                        for dir in dirs:
                            dir.kill()
                        os.system('echo "quit" > /home/pi/final_proj/video_fifo')
                    elif text == 'song 1':
                        beat_times = beat_times_1
                        dur = dur_1
                        song = 1
                        state = 'RUNNING'
                        my_cursor = cursor.Cursor(160,200)
                        start_time = time.time()
                        start = time.time()
                        last_runtime = time.time()
                        runtime = 0
                        score = 0
                        os.system('mplayer -input file=/home/pi/final_proj/video_fifo electronic-rock-king-around-here-15045.mp3 &')
                    elif text == 'song 2':
                        beat_times = beat_times_2
                        dur = dur_2
                        song = 2
                        state = 'RUNNING'
                        my_cursor = cursor.Cursor(160,200)
                        start_time = time.time()
                        start = time.time()
                        last_runtime = time.time()
                        runtime = 0
                        score = 0
                        os.system('mplayer -input file=/home/pi/final_proj/video_fifo the-future-bass-15017.mp3 &')

    pygame.display.flip()

GPIO.cleanup()
