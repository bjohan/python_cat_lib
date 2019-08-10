MAIN_VFO = 0
SAT_RX_VFO = 1
SAT_TX_VFO = 2

class Ft847:
    def __init__(self, cat):
        self.cat = cat
        self.catIf(True)
        self.modeDict = {   0x00: 'LSB', 
                            0x01: 'USB',
                            0x02: 'CW',
                            0x03: 'CW-R',
                            0x04: 'AM',
                            0x08: 'FM',
                            0x82: 'CW(N)',
                            0x83: 'CW(N)-R',
                            0x84: 'AM(N)',
                            0x88: 'FM(N)',};
        self.modeCodeDict = {v: k for k,v in self.modeDict.iteritems()}

    def disconnect(self):
        self.catIf(False)

    def catIf(self, on):
        if on:
            self.cat.transact(0x00)
        else:
            self.cat.transact(0x80)

    def ptt(self, on):
        if on:
            self.cat.transact(0x08)
        else:
            self.cat.transact(0x88)

    def satellite(self, on):
        if on:
            self.cat.transact(0x4E)
        else:
            self.cat.transact(0x8E)

    def receiverStatus(self):
        status = ord(self.cat.transact(0xe7, nresp = 1)[0])
        rd = {}
        rd['pttDisabled'] = (status >> 7) &0x01
        rd['dummy'] = (status >> 4) &0x3
        rd['po_or_alc'] = (status)&0x1F
        return rd

    def transmitStatus(self):
        status = ord(self.cat.transact(0xF7, nresp = 1)[0])
        rd = {}
        rd['squelched'] = (status >> 7) &0x01
        rd['ctcss_or_dcs_unmatched'] = (status >> 6) &0x1
        rd['discriminator_off_center'] = (status >> 5) &0x1
        rd['smeter'] = (status)&0x1F
        return rd

    def getVfoStatus(self, vfo):
        opcodes = {MAIN_VFO: 0x03, SAT_RX_VFO: 0x13, SAT_TX_VFO: 0x23}
        status = self.cat.transact(opcodes[vfo], nresp = 5);
        freq = 0
        mult = 10e6
        for s in status[0:4]:
            freq += int("%x"%(ord(s)))*mult
            mult /= 100
        return {'frequency': freq, 'mode': self.modeDict[ord(status[4])]}

    def getMainVfoStatus(self):
        return self.getVfoStatus(MAIN_VFO)

    def getSatRxVfoStatus(self):
        return self.getVfoStatus(SAT_RX_VFO)

    def getSatTxVfoStatus(self):
        return self.getVfoStatus(SAT_TX_VFO)

    def setFrequency(self, vfo, freq):
        opcodes = {MAIN_VFO: 0x01, SAT_RX_VFO: 0x11, SAT_TX_VFO: 0x21}
        freq = int(int(freq)/10)
        print freq, "dhz"
        data = "%d"%freq
        diff = 8-len(data)
        if diff < 0:
            data = data[-8:]
        else:
            data = "0"*diff+data
        print data

        params = []
        for i in range(4):
            params += [int(data[2*i:2*i+2], 16)]
        print params

        opc = opcodes[vfo]
        return self.cat.transact(opc, params)

    def setMainVfoFrequency(freq):
        return self.setFrequency(MAIN_VFO, freq)

    def setSatRxVfoFrequency(freq):
        return self.setFrequency(SAT_RX_VFO, freq)

    def setSatTxVfoFrequency(freq):
        return self.setFrequency(SAT_TX_VFO, freq)

    def setOperatingMode(self, vfo, mode):
        opcodes = {MAIN_VFO: 0x07, SAT_RX_VFO: 0x17, SAT_TX_VFO: 0x27}
        opc = opcodes[vfo]
        params = [self.modeCodeDict[mode], 0, 0, 0]
        return self.cat.transact(opc, params)

    def setMainVfoOperatingMode(self, mode):
        return self.setOperatingMode(MAIN_VFO, mode)

    def setSatRxVfoOperatingMode(self, mode):
        return self.setOperatingMode(SAT_RX_VFO, mode)

    def setSatTxVfoOperatingMode(self, mode):
        return self.setOperatingMode(SAT_TX_VFO, mode)







