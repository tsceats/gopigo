import gopigo as gpg
from time import sleep
from gopigo import set_left_speed, set_right_speed, set_speed, stop

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