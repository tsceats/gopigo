import gopigo as gpg
from time import sleep
from gopigo import set_left_speed, set_right_speed, set_speed, stop
from math import *

def oneRun():
    leftStart = gpg.enc_read(0)
    rightStart = gpg.enc_read(1)
    gpg.motor_fwd()
    sleep(2)
    stop()
    sleep(0.5)
    leftEnd = gpg.enc_read(0)
    rightEnd = gpg.enc_read(1)
    return (leftEnd - leftStart, rightEnd - rightStart)

def calibrate(speed):
    gpg.trim_write(0)
    sleep(2)
    set_left_speed(speed)
    set_right_speed(speed)
    left = -1
    right = 1
    sp = 0
    while left != right:
        both = oneRun()
        both2 = oneRun()
        left = both[0] + both2[0]
        right = both[1] + both2[1]
        if left > right + 1:
            sp -= 1
        elif (left + 1 < right):
            sp += 1
        print left, right, sp
        gpg.trim_write(sp)
        sleep(2)

def forwardTicks(distance, speed):
    distance = max(1, min(distance, 500))
    speed = max(50, min(speed, 200))
    
    leftTicks = distance
    rightTicks = distance
    right_speed = speed
    left_speed = speed
    set_left_speed(left_speed)
    set_right_speed(right_speed)
    leftStart = gpg.enc_read(0)
    rightStart = gpg.enc_read(1)
    leftTarget = leftStart + leftTicks
    rightTarget = rightStart + rightTicks
    isLeftMoving = False
    isRightMoving = False
    adjustment_interval = 1
    last_left_check = leftStart
    last_right_check = rightStart
    
    while(True):
        leftReading = gpg.enc_read(0)
        rightReading = gpg.enc_read(1)
        leftToEnd = leftTarget - leftReading
        rightToEnd = rightTarget - rightReading
        
        if leftReading >= leftTarget and rightReading >= rightTarget:
            gpg.stop()
            break
        elif leftReading < leftTarget and rightReading < rightTarget:
            new_left_speed = speed
            new_right_speed = speed
            
            if (leftToEnd > rightToEnd + 1):
                extraFactor = float(leftToEnd - rightToEnd) / leftToEnd
                extraFactor = max(0.02, min(0.15, extraFactor))
                new_left_speed = int(speed * (1.0 + extraFactor))
            elif (rightToEnd > leftToEnd + 1):
                extraFactor = float(rightToEnd - leftToEnd) / rightToEnd
                extraFactor = max(0.02, min(0.15, extraFactor))
                new_right_speed = int(speed * (1.0 + extraFactor))
            
            if (left_speed != new_left_speed):
                set_left_speed(new_left_speed)
                left_speed = new_left_speed
            if (right_speed != new_right_speed):
                set_right_speed(new_right_speed)
                right_speed = new_right_speed
            
            if (not isLeftMoving) or (not isRightMoving):
                print "Forward!"
                gpg.motor_fwd()
                isLeftMoving = True
                isRightMoving = True

def waitForTarget():
    while (gpg.read_enc_status() != 0):
        sleep(0.1)
        
def checkTicks(aTicks):
    if aTicks < 1 or aTicks > 500:
        print("Please set ticks to more than one, or less than 500")
        return False
    return True

def fwd(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(1, 1, aTicks)
        gpg.fwd()
        waitForTarget()

def back(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(1, 1, aTicks)
        gpg.bwd()
        waitForTarget()

def leftRot(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(1, 1, aTicks)
        gpg.left_rot()
        waitForTarget()

def left(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(0, 1, aTicks)
        gpg.left()
        waitForTarget()

def rightRot(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(1, 1, aTicks)
        gpg.right_rot()
        waitForTarget()

def right(aTicks):
    if checkTicks(aTicks):
        gpg.enc_tgt(1, 0, aTicks)
        gpg.right()
        waitForTarget()
