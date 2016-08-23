import gopigo as gpg
from time import sleep
from gpg import set_left_speed, set_right_speed, set_speed

def waitForTarget():
    while (gpg.read_enc_status() != 0):
        sleep(0.1)

def fwd(aTicks):
    gpg.enc_tgt(1, 1, aTicks)
    gpg.fwd()
    waitForTarget()

def back(aTicks):
    gpg.enc_tgt(1, 1, aTicks)
    gpg.bwd()
    waitForTarget()

def leftRot(aTicks):
    gpg.enc_tgt(1, 1, aTicks)
    gpg.left_rot()
    waitForTarget()

def left(aTicks):
    gpg.enc_tgt(0, 1, aTicks)
    gpg.left()
    waitForTarget()

def rightRot(aTicks):
    gpg.enc_tgt(1, 1, aTicks)
    gpg.right_rot()
    waitForTarget()

def right(aTicks):
    gpg.enc_tgt(1, 0, aTicks)
    gpg.right()
    waitForTarget()