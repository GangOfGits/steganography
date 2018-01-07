from PIL import Image

image = Image.open(input('image name/path >'))

imageMod = image.mode
imageSiz = image.size
#print(imageMod)
#print(imageSiz)

img = image.load()
#print(img[4,4])
#print(img[4,4][0])

msgLen = int(input('how many charecters are in the message >'))*8
#msgLen = 40

binStr = ''

y = 0
while y < imageSiz[1] and msgLen > 0:
    x = 0
    while x <= imageSiz[0] and msgLen > 0:
        binStr += bin(img[x,y][0])[-1:]
        #print(str(img[x,y]), bin(img[x,y][0])[-1:], str(x), str(y))

        x += 1
        msgLen -= 1

    y += 1

#print(binStr)

out = ''
while len(binStr) > 0:
    out += chr(int(binStr[:8],2))
    binStr = binStr[8:]

print(out)
input('')
