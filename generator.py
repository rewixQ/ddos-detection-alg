import time
import threading
import bitstring
import random
import Cryptodome.Random.random
import os


class NetflowGenerator:

    def __init__(self, numberOfDevices, filePath, network, frequency, isDos):
        self.numberOfDevices = numberOfDevices
        self.filePath = filePath
        self.done = False
        self.network = network
        self.isDos = isDos
        self.frequency = frequency
        self.run()

    def getBin(self, i, w):
        get_bin = lambda x, n: format(x, 'b').zfill(n)
        return get_bin(i, w)
    
    def getTime(self):
        lyear = str(bitstring.BitArray(int=time.localtime().tm_year, length=12))[2:]
        lmon = str(bitstring.BitArray(int=time.localtime().tm_mon, length=12))[2:]
        lday = str(bitstring.BitArray(int=time.localtime().tm_mday, length=12))[2:]
        lhour = str(bitstring.BitArray(int=time.localtime().tm_hour, length=12))[2:]
        lmin = str(bitstring.BitArray(int=time.localtime().tm_min, length=12))[2:]
        lsec = str(bitstring.BitArray(int=time.localtime().tm_sec, length=12))[2:]
        return lyear + " " + lmon + " " + lday + " " + lhour + " " + lmin + " " + lsec

    #AquaCarrier - Devices packets generating method
    def generateAquaCarrier(self, file, ipList, ownIp):
        while not self.done:
            #writing AquaCarrier packets 
            for ip in ipList:
                ltime = self.getTime()
                com = Cryptodome.Random.random.getrandbits(16)
                ipHex = hex(int(ip, 2))[2:]
                ownIpHex = hex(int(ownIp, 2))[2:]
                packet = ownIpHex + " " + ipHex + " " + ltime + " " + str(bitstring.BitArray(int=com, length=20))[2:]
                file.write(packet + "\n")
            time.sleep(random.randint(18,22))

    #Device - AquaCarrier packets generating method
    def generateDevice(self, file, ownIp, aquaIp):
        while not self.done:
            #writing devices packets
            ltime = self.getTime()
            com = Cryptodome.Random.random.getrandbits(16)
            aquaIpHex = hex(int(aquaIp, 2))[2:]
            ownIpHex = hex(int(ownIp, 2))[2:]
            packet = ownIpHex + " " + aquaIpHex +  " " + ltime + " " + str(bitstring.BitArray(int=com, length=20))[2:]
            file.write(packet + "\n")
            time.sleep(self.frequency)

    #Attack packets generating method
    def attack(self, file, attackers, recIp):
        it = 0
        end = random.randint(2500,3000)
        while not self.done:
            #Writing DoS packets
            ltime = self.getTime()
            com = Cryptodome.Random.random.getrandbits(16)
            srcIpHex = hex(int(attackers[random.randint(0,len(attackers))-1], 2))[2:]
            recIpHex = hex(int(recIp, 2))[2:]
            if recIpHex == srcIpHex:
                continue
            packet = srcIpHex + " " + recIpHex +  " " + ltime + " " + str(bitstring.BitArray(int=com, length=20))[2:]
            file.write(packet + "\n")
            it += 1
            if it == end:
                return

    def repair(self):
        fileToRep = open("temp"+self.filePath, "r")
        fileToWrite = open(self.filePath, "w")
        for line in fileToRep:
                fileToWrite.write(line[len(line)-40:])
        fileToWrite.close()

    def run(self):
        #Warning
        if os.path.exists(self.filePath):
            ans = input("\n\nFILE EXISTS!!! Type 'stop' if you dont want do overwrite this file. Otherwise press Enter.\n")
            if ans == "stop":
                return

        #Opening file
        file = open("temp"+self.filePath, "w")

        #Generating AquaCarrier
        AQUACARRIERIP = self.network + "1111" + str(self.getBin(14, 4))

        #Generating devices
        iptab = []
        trtab = []
        for i in range(self.numberOfDevices):
            ip = self.network + str(self.getBin(i+1, 16-len(self.network)))
            iptab.append(ip)
            thread = threading.Thread(target=self.generateDevice, args=[file, ip, AQUACARRIERIP])
            trtab.append(thread)

        #Netflow starting
        traq = threading.Thread(target=self.generateAquaCarrier, args=[file, iptab, AQUACARRIERIP])
        traq.start()
        for thread in trtab:
            thread.start()

        #Giving time for generating
        print("Generating\n")
        time.sleep(random.randint(120,180))

        #Attack starting
        if self.isDos:
            print("Attack\n")
            if random.randint(0,99) < 50:
                if random.randint(0,99) < 50:
                    trattack = threading.Thread(target=self.attack, args=[file, iptab, iptab[random.randint(0,len(iptab)-1)]])
                else:
                    trattack = threading.Thread(target=self.attack, args=[file, iptab, AQUACARRIERIP])
            else:
                attackersIps = []
                for i in range(int(self.numberOfDevices/2)):
                    ip = "10101010" + str(self.getBin(i+1, 8))
                    attackersIps.append(ip)
                if random.randint(0,99) < 50:
                    trattack = threading.Thread(target=self.attack, args=[file, attackersIps, iptab[random.randint(0,len(iptab)-1)]])
                else:
                    trattack = threading.Thread(target=self.attack, args=[file, attackersIps, AQUACARRIERIP])
            trattack.start()
            trattack.join()
    
        #Ending
        input("Press Enter to stop")
        self.done = True
        file.close()

        #Repairing file
        print("Repairing")
        self.repair()
        os.remove("temp"+self.filePath)




# generator = NetflowGenerator(128,                       #number of devices
#                              "test.nfp",                #output file path
#                              "11000100",                #network (bits)
#                              1,                         #frequency of the devices>AquaCarrier communication
#                              False)                     #flag indicating the occurrence of an attack 
# generator = NetflowGenerator(128, "packets128attack2.nfp", "11000100", 1,  True)
generator = NetflowGenerator(128, "packets128attack3.nfp", "11000100", 1,  True)
