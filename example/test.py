import steganography as steg

myKM = steg.KMsteg()
myKM.encode("tiger2.jpg", "someText.txt", "tigerNew.jpg")
print(myKM.decode("tigerNew.jpg", 12))
