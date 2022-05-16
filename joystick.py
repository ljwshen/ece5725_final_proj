import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(5, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(6, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(13, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down = GPIO.PUD_UP)


while(True):
    five = GPIO.input(5)
    six = GPIO.input(6)
    thirteen = GPIO.input(13)
    nineteen = GPIO.input(19)
    print("5: "+ str(five)+ "   6: "+ str(six) + "  13: "+ str(thirteen) + "   19: " + str(nineteen))

GPIO.cleanup()
