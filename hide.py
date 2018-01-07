from PIL import Image

image = Image.open(input('name of PNG (.png) or bitmap (.bmp) >')) #akss for an image name and opens it 

imageMod = image.mode #useless
imageSiz = image.size #gets size of the image

img = image.load() #img allows pixel editing

msg = input('what would you like to hide >') #gets the text to hide

##converts the string msg into a string of binary ascii values
asciimsg = ''
for c in msg:
    b = bin(ord(c))[2:]
    while len(b) < 8:
        b = '0' + b
    asciimsg += b
print(asciimsg)

char = 0 #how far through asciimsg have we written
y = 0
while y <= imageSiz[1] and char < len(asciimsg): #nested loopd iterate through pictures, conditions ensure we dont write more than the picture can hold
    x = 0
    while x <= imageSiz[0] and char < len(asciimsg):
        if asciimsg[char] == '1': #if we a righting a 1
            if img[x,y][0] % 2 == 0: #check if the red value is even, if the value is even it will end in zero so we must ajust by 1
                prev = img[x,y] #this and next 4 for editing red value
                if prev[0] > 1:
                    img[x,y] = (prev[0] - 1,prev[1],prev[2])
                else:
                    img[x,y] = (prev[0] + 1,prev[1],prev[2])
            #print('1 :', str(x), str(y), bin(img[x,y][0])[-1:])

        elif asciimsg[char] == '0': #same as above only for zeros
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

image.save('done.png') #save the image as done.png (poor practice to hard code i know)
