from PIL import Image

image = Image.open(input('image name/path >')) #open an image

imageMod = image.mode
imageSiz = image.size
#print(imageMod)
#print(imageSiz)

img = image.load() #allows reading of pixels
#print(img[4,4])
#print(img[4,4][0])

msgLen = int(input('how many charecters are in the message >'))*8 #the number of chaecters in the hidden message * 8 to get to the number of bits (i could encode this in the first 16 pixels of so ina later version)
#msgLen = 40

binStr = '' #an empty string to store recovered bits

y = 0 #iterate throught the images pixels 
while y < imageSiz[1] and msgLen > 0:
    x = 0
    while x <= imageSiz[0] and msgLen > 0:
        binStr += bin(img[x,y][0])[-1:] #add the last bit of the the binary value of the red channel of each pixel to binStr
        #print(str(img[x,y]), bin(img[x,y][0])[-1:], str(x), str(y))

        x += 1
        msgLen -= 1

    y += 1

#print(binStr)

out = ''
while len(binStr) > 0: #iterate through the collected bits
    out += chr(int(binStr[:8],2)) #add the ascii values of the integer values of the first 8 bits of binStr to the output
    binStr = binStr[8:] #remove the first eight bits of binStr

print(out) #print the rcovered message
input('') #holds the window open

#please forgive multifunction lines
