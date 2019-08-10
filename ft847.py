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
        self.modeCodeDict = self.revDict(self.modeDict) 

        self.ctcssDcsModeDict = {   0x0A: "DCS ON",
                                    0x2A: "CTCSS ENC/DEC ON",
                                    0x4A: "CTCSS ENC ON",
                                    0x8A: "CTCSS/DCS OFF",}
        self.ctcssDcsCodeDict = self.revDict(self.ctcssDcsModeDict)

        self.ctcssToneCodeDict = {
                "67.0": 0x3F,
                "94.8": 0x1D ,
                "131.8": 0x09 ,
                "186.2": 0x04,
                "69.3": 0x39,
                "97.4": 0x3A,
                "136.5": 0x18,
                "192.8": 0x13,
                "71.9": 0x1F,
                "100.0": 0x0D,
                "141.3": 0x08,
                "203.5": 0x03,
                "74.4": 0x3E,
                "103.5": 0x1C,
                "146.2": 0x17,
                "210.7": 0x12,
                "77.0": 0x0F,
                "107.2": 0x0C,
                "151.4": 0x07,
                "218.1": 0x02,
                "79.7": 0x3D,
                "110.9": 0x1B,
                "156.7": 0x16,
                "225.7": 0x11,
                "82.5": 0x1E,
                "114.8": 0x0B,
                "162.2": 0x06,
                "233.6": 0x01,
                "85.4": 0x3C,
                "118.8": 0x1A,
                "167.9": 0x15,
                "241.8": 0x10,
                "88.5": 0x0E,
                "123.0": 0x0A,
                "173.8": 0x05,
                "250.3": 0x00,
                "91.5": 0x3B,
                "127.3": 0x19,
                "179.9": 0x14,}

    def revDict(self, d):
        return {v: k for k,v in d.iteritems()}

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


    def numToParams(self, num, length=8):
        data = "%d"%num
        diff = length-len(data)
        if diff < 0:
            data = data[-length:]
        else:
            data = "0"*diff+data

        params = []
        for i in range(int(length/2)):
            params += [int(data[2*i:2*i+2], 16)]
        return params

    def setFrequency(self, vfo, freq):
        opcodes = {MAIN_VFO: 0x01, SAT_RX_VFO: 0x11, SAT_TX_VFO: 0x21}
        freq = int(int(freq)/10)
        params = self.numToParams(freq)
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

    def setCtcssDcsMode(self, vfo, mode):
        opcodes = {MAIN_VFO: 0x0A, SAT_RX_VFO: 0x1A, SAT_TX_VFO: 0x2A}
        opc = opcodes[vfo]
        params = [self.ctcssDcsCodeDict[mode], 0,0,0]
        return self.cat.transact(opc, params)

    def setMainVfoCtcssDcsMode(self, mode):
        self.setCtcssDcsMode(MAIN_VFO, mode)

    def setSatRxVfoCtcssDcsMode(self, mode):
        self.setCtcssDcsMode(SAT_RX_VFO, mode)

    def setSatTxVfoCtcssDcsMode(self, mode):
        self.setCtcssDcsMode(SAT_TX_VFO, mode)


    def setCtcssFrequency(self, vfo, freq):
        opcodes = {MAIN_VFO: 0x0B, SAT_RX_VFO: 0x1B, SAT_TX_VFO: 0x2B}
        opc = opcodes[vfo]
        params = [self.ctcssToneCodeDict[freq], 0, 0, 0]
        return self.cat.transact(opc, params)

    def setMainVfoCtcssFrequency(self, freq):
        return self.setCtcssFrequency(MAIN_VFO, freq)

    def setSatRxVfoCtcssFrequency(self, freq):
        return self.setCtcssFrequency(SAT_RX_VFO, freq)

    def setSatTxVfoCtcssFrequency(self, freq):
        return self.setCtcssFrequency(SAT_TX_VFO, freq)

    def setDcsCode(self, vfo, dcsCode):
        opcodes = {MAIN_VFO: 0x0C, SAT_RX_VFO: 0x1C, SAT_TX_VFO: 0x2C}
        opc = opcodes[vfo]
        params = self.numToParams(int(dcsCode), 4)
        print params
        return self.cat.transact(opc, params)

    def setMainVfoDcsCode(self, code):
        return self.setDcsCode(MAIN_VFO, code)

    def setSatRxVfoDcsCode(self, code):
        return self.setDcsCode(SAT_RX_VFO, code)

    def setSatTxVfoDcsCode(self, code):
        return self.setDcsCode(SAT_TX_VFO, code)

    def setRepeaterShift(self, shift):
        shiftDict = {"-": 0x09, "+": 0x49, "0": 0x89}
        params = [shiftDict[shift], 0, 0, 0]
        return self.cat.transact(0x09, params)

    def setRepeaterOffset(self, offs):
        params = self.numToParams(int(int(offs)/10), 8)
        print params
        return self.cat.transact(0xF9, params)








