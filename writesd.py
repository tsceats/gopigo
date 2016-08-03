#!/Users/bvance/anaconda/bin/python
import argparse
import subprocess
from re import sub
from time import sleep

def shell(aShellCmd):
    return subprocess.check_output(aShellCmd, shell=True).decode('ascii')

def getArgs():
    myParser = argparse.ArgumentParser(description='Write custom rpi hostname and WPA settings')
    myParser.add_argument('-n', dest = 'netname', help = 'Wifi network name prefix', required = True)
    myParser.add_argument('-f', dest = 'countFrom', help = 'Host suffix start (inclusive)', required = True)
    myParser.add_argument('-t', dest = 'countTo', help = 'Host suffix end (inclusive)', required = True)
    myParser.add_argument('-p', dest = 'passwd', help = 'Wifi password', required = True)
    myParser.add_argument('-H', dest = 'hostname_prefix', help = 'hostname', required = True)
    myParser.add_argument('-I', dest = 'ip_prefix', help = 'IP prefix', required = True)

    return myParser.parse_args()

def repStrInFile(aFileName, aOldString, aNewString):
    myReadHandle = open(aFileName, 'r')
    myContent = myReadHandle.read()
    myReadHandle.close()

    print("O|||", myContent)
    myNewContent = sub(aOldString, aNewString, myContent)
    print("N|||", myNewContent)
    myWriteHandle = open(aFileName, 'w')
    myWriteHandle.write(myNewContent)
    myWriteHandle.close()

def setHostname(aRootDir, aHostname):
    repStrInFile(aRootDir + "/etc/hostname", "imcrobot[0-9]{2,4}", aHostname)
    repStrInFile(aRootDir + "/etc/hosts", "imcrobot[0-9]{2,4}", aHostname)

def setNetwork(aRootDir, aName, aPasswd):
    repStrInFile(aRootDir + "/etc/wpa_supplicant/wpa_supplicant.conf", 'ssid=\\".*\\"','ssid="' + aName + '"')
    repStrInFile(aRootDir + "/etc/wpa_supplicant/wpa_supplicant.conf", 'psk=\\".*\\"','psk="' + aPasswd + '"')

def setStaticIP(aRootDir, aStaticIP):
    myGateway = aStaticIP[:-3]+"1"
    repStrInFile(aRootDir + "/etc/network/interfaces", 'address [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}', 'address ' + aStaticIP)
    repStrInFile(aRootDir + "/etc/network/interfaces", 'gateway [0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}[.][0-9]{1,3}', 'gateway ' + myGateway)

def checkNetwork(aRootDir, aName, aPasswd):
    myReadHandle = open(aRootDir + "/etc/wpa_supplicant/wpa_supplicant.conf", 'r')
    myContent = myReadHandle.read()
    myReadHandle.close()

    if not (aName in myContent and aPasswd in myContent):
        print("Check failed, will write network settings...")
        setNetwork(aRootDir, aName, aPasswd)
        checkNetwork(aRootDir, aName, aPasswd)
    else:
        print("Check passed...")

def findSDCard():
    myResults = shell("diskutil list")
    mySplitResults = myResults.split("/dev/")
    myFoundDisk = None
    for myDisk in mySplitResults:
        if "FDisk_partition_scheme" in myDisk and "internal, physical" in myDisk:
            if "*31.1 GB" in myDisk or "*16.1 GB" in myDisk or "*15.9 GB" in myDisk:
                myFoundDisk = myDisk.strip().split()[0].strip()
                print("Found SD %s from %s" % (myFoundDisk, myDisk))
                break
    return myFoundDisk

def unmountDisk(aDrive):
    print(shell("diskutil unmountDisk /dev/" + aDrive))

def writeImage(anImage, aDrive):
    try:
        print(shell("dd bs=1m if=" + anImage + " of=/dev/r" + aDrive))
    except:
        print("Write failed, will try to unmount...")
        sleep(5)
        unmountDisk(aDrive)
        writeImage(anImage, aDrive)

def ejectDisk(aDrive):
    print(shell("diskutil eject /dev/r" + aDrive))

def mountImage(aName):
    myMountResult = shell("hdiutil attach " + aName)
    myMountResultSplit = [i.strip() for i in myMountResult.split('\t') if i.strip() != '']
    myMountedDisk = myMountResultSplit[0]
    myMountedPartition = myMountResultSplit[-1]
    return (myMountedDisk, myMountedPartition)

def detach(aDrive):
    print(shell("hdiutil detach " + aDrive))

def setInImage(aHostname, aStaticIP, aNetname, aPasswd):
    print("Host=%s\nWifi network=%s\nWifi password=%s\n" % (aHostname, aNetname, aPasswd))

    print("Mounting image...")
    myMountedDisk, myMountedPartition = mountImage("imcrpi.img")
    print("Mounted %s from %s" % (myMountedPartition, myMountedDisk))

    setHostname(myMountedPartition, aHostname)
    setNetwork(myMountedPartition, aNetname, aPasswd)
    setStaticIP(myMountedPartition, aStaticIP)

    print("Unmounting image...")
    detach(myMountedDisk)
    print("Done.")

def findSDCardComplete():
    print("Finding SD card...")

    myCard = findSDCard()
    if (myCard == None):
        print("SD card not found, please insert!")
    while myCard == None:
        sleep(1)
        myCard = findSDCard()
    print("SD card found on " + myCard)
    return myCard

def writeImageToCard(aCard):
    try:
        unmountDisk(aCard)
    except:
        print("Unmount failed, retrying...")
        sleep(5)
        unmountDisk(aCard)
    print("Unmounted, waiting...")
    sleep(5)
    print("Writing image...")
    writeImage("imcrpi.img", aCard)
    print("Done")

def ejectCard(aCard):
    sleep(5)
    print("Ejecting disk...")
    try:
        ejectDisk(aCard)
    except subprocess.CalledProcessError:
        print("Failed to eject, will try again in 10 seconds!")
        sleep(10)
        ejectDisk(aCard)

def setImageAndWriteToCard(aHostname, aStaticIP, aNetname, aPasswd):
    setInImage(aHostname, aStaticIP, aNetname, aPasswd)
    myCard = findSDCardComplete()
    writeImageToCard(myCard)
    ejectCard(myCard)

if __name__ == '__main__':
    myArgs = getArgs()

    for i in range(int(myArgs.countFrom),int(myArgs.countTo)+1):
        myHostnamePostfix = str(i).zfill(2)
        print("Begin", myHostnamePostfix)
        myCompleteHostname = myArgs.hostname_prefix + myHostnamePostfix
        myCompleteStaticIP = myArgs.ip_prefix + myHostnamePostfix
        setImageAndWriteToCard(myCompleteHostname, myCompleteStaticIP, myArgs.netname, myArgs.passwd)
        print("Done", myHostnamePostfix)

    print("All done!")

"""if __name__ == '__main__':
    myArgs = getArgs()

    myCounter = 12
    while True:
        mySdCard = findSDCardComplete()
        print("Waiting...")
        sleep(10)
        #setNetwork("/Volumes/Untitled", myArgs.netname, myArgs.passwd)
        checkNetwork("/Volumes/Untitled", myArgs.netname, myArgs.passwd)
        ejectCard(mySdCard)

        myCounter += 1
        print("Checked card", myCounter)"""
