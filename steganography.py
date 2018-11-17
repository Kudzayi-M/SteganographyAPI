############################################
# REMUS Linear Steganography module v1.0.0 #
############################################

########## Notes ###########
# - For every 2 bits in the file that is to be concealed, takes up one byte of the file it takes up
#       this means that every byte of the concealed file will take up 4 bytes of the concealer file.
# - Due to the above point, concealed files can only be very small, not realative to the size of the concelaer (I think).
#       Note that efforts will be made in the future to be able to write more inside of a concealer file
#       as I feel that this is the cause of a bug in the code rather than lack of bytes to replace

## Lisencing Notice ##
# Officially licensed to https://remusmtf.com/ of REMUS by Kudzayi Mberi
# You may use this product for comercial or non-comercial purpouses.
# If use is for comecrical purpuses, You must also include the version number.
# If it is for non-comercial use, you must include this entire header.
# Copyright © 2018 by https://remusmtf.com/

class KMsteg:

    def int2binstr(self, inputImg):
     self.tempArr = [None] * len(inputImg)
     for i in range(len(inputImg)):
         self.tempArr[i] = "{0:{fill}8b}".format(inputImg[i], fill='0')
     return self.tempArr 

    def string2bits(self, s=''):
        return [bin(ord(x))[2:].zfill(8) for x in s]

    def binstr2int(self, theBin):
       self.tempBinList = [None] * len(theBin)
       for i in range(len(theBin)):
           self.tempBinList[i] = int(theBin[i], 2)
       return self.tempBinList

    def hiding(self, inputText, inputImg):
        # 128 is arbitrarily used as I didn't fully understand how computers
        # read images and I din't want to touch any metadata, this may be changed
        self.fast_j = 127
        for j in range(128, (len(inputText)+128) ):
            self._j = j - 128
            if self.fast_j == 127:
               self.fast_j += 1
               #This range config is set up to read 2 bits a time out of 8 bits
            for z in range(0, 7, 2):
               self.tempForImg = list(inputImg[self.fast_j])
               self.tempForImg[6] = inputText[self._j][z]
               self.tempForImg[7] = inputText[self._j][z+1]
               self.tempForImg = "".join(self.tempForImg)
               inputImg[self.fast_j] = self.tempForImg
               self.fast_j += 1
        return inputImg

    def unhiding(self, byteCount, inputImg):
        self.foundText = ["00000000"] * byteCount
        self.fast_j = 127
        for j in range(128, (byteCount+128) ):
            self._j = j - 128
            self.slow_j = j - 128
            if self.fast_j == 127:
                self.fast_j += 1
            for z in range(0, 7, 2):
                self.tempForImg = list(inputImg[self.fast_j])
                self.tempfoundText = list(self.foundText[self.slow_j])
                self.tempfoundText[z] = self.tempForImg[6]
                self.tempfoundText[z+1] = self.tempForImg[7]
                self.tempfoundText = "".join(self.tempfoundText)
                self.foundText[self.slow_j] = self.tempfoundText
                self.fast_j += 1
        return self.foundText

    def bits2chr(self, theString):
        self.tempString = [None] * len(theString)
        for m in range(len(theString)):
            self.tempString[m] = chr(theString[m])
        return self.tempString

    def encode(self, outfile, hiddenfilename, newfile):
        with open(outfile, "rb") as self.imageFile:
            self.f = self.imageFile.read()
            self.b = bytearray(self.f)
        with open(hiddenfilename, "rb") as self.imageFile:
            self.f2 = self.imageFile.read()
            self.someText = bytearray(self.f2)
        self.someText = str(self.someText)[12:-2]
        self.b2 = self.int2binstr(self.b)
        self.someText2 = self.string2bits(self.someText)
        self.someNewImg = self.hiding(self.someText2, self.b2)
        self.b3 = self.binstr2int(self.someNewImg)
        self.b4 = bytes(self.b3)
        with open(newfile, "wb") as self.imageFile:
            self.imageFile.write(self.b4)

    def decode(self, infile, approxByteSize):
        with open(infile, "rb") as self.imageFile:
            self.the2ndf = self.imageFile.read()
            self.t1 = bytearray(self.the2ndf)
        self.t2 = self.int2binstr(self.t1)
        self.v1 = self.unhiding(approxByteSize, self.t2)
        self.v2 = self.binstr2int(self.v1)
        self.v3 = self.bits2chr(self.v2)
        return self.v3

