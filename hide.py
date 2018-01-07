from PIL import Image

image = Image.open(input('name of PNG (.png) or bitmap (.bmp) >'))

imageMod = image.mode
imageSiz = image.size

img = image.load()

msg = input('what would you like to hide >')

asciimsg = ''
for c in msg:
    b = bin(ord(c))[2:]
    while len(b) < 8:
        b = '0' + b
    asciimsg += b
print(asciimsg)

char = 0
y = 0
while y <= imageSiz[1] and char < len(asciimsg):
    x = 0
    while x <= imageSiz[0] and char < len(asciimsg):
        if asciimsg[char] == '1':
            if img[x,y][0] % 2 == 0:
                prev = img[x,y]
                if prev[0] > 1:
                    img[x,y] = (prev[0] - 1,prev[1],prev[2])
                else:
                    img[x,y] = (prev[0] + 1,prev[1],prev[2])
            #print('1 :', str(x), str(y), bin(img[x,y][0])[-1:])

        elif asciimsg[char] == '0':
            if img[x,y][0] % 2 != 0:
                prev = img[x,y]
                if prev[0] > 1:
                    img[x,y] = (prev[0] - 1,prev[1],prev[2])
                else:
                    img[x,y] = (prev[0] + 1,prev[1],prev[2])
            #print('0 :', str(x), str(y), bin(img[x,y][0])[-1:])

        char += 1
        x += 1

    y += 1

image.save('done.png')
