from PIL import Image



def hide(data, imageName):
    ##the following code hides the message
    image = Image.open(imageName)
    imageSiz = image.size #gets size of the image
    img = image.load() #allows pixel access
        
    char = 0 #how far through asciimsg have we written
    y = 0
    while y <= imageSiz[1] and char < len(data): #nested loopd iterate through pictures, conditions ensure we dont write more than the picture can hold
        x = 0
        while x <= imageSiz[0] and char < len(data):
            if data[char] == '1': #if we a righting a 1
                if img[x,y][0] % 2 == 0: #check if the red value is even, if the value is even it will end in zero so we must ajust by 1
                    prev = img[x,y] #this and next 4 for editing red value
                    if prev[0] > 1:
                        img[x,y] = (prev[0] - 1,prev[1],prev[2]) #edits the pixel's red
                    else:
                        img[x,y] = (prev[0] + 1,prev[1],prev[2])
                #print('1 :', str(x), str(y), bin(img[x,y][0])[-1:])

            elif data[char] == '0': #same as above only for zeros
                if img[x,y][0] % 2 != 0:
                    prev = img[x,y]
                    if prev[0] > 1:
                        img[x,y] = (prev[0] - 1,prev[1],prev[2]) #edits the pixel's red
                    else:
                        img[x,y] = (prev[0] + 1,prev[1],prev[2])
                #print('0 :', str(x), str(y), bin(img[x,y][0])[-1:])

            char += 1
            x += 1

        y += 1

    image.save('done.png') #save the image as done.png (poor practice to hard code i know)





hidingPlace = input('where would you like to hide your msg? >')
msg = input('what would you like to hide? >') #gets the text to hide

##converts the string msg into a string of binary ascii values
asciimsg = ''
for c in msg:
    b = bin(ord(c))[2:]
    while len(b) < 8:
        b = '0' + b
    asciimsg += b
#at this point ascii message is a string of 1s and 0s, each byte representing the ascii value of a charecter
print(asciimsg)

##adds in the length indicators
#The format will use 1 or 9 bits every 255 to indicate the length of the message. In the following format 1,255,1,255,9,<255 
#if the first bit after 255 bits of data is a 1 it means there is another full 255 bit chunk of data directly following it 
#if it is a 0 the next 8 bits signofy how much data the las chunk contains

debugg = ''
fullmsg = ''
while len(asciimsg) > 0:
    seg = asciimsg[:255] #gets the first 255 bits or less from asciimsg
    
    preseg = bin(len(seg))[2:] #gets the binary for the len of seg
    while len(preseg) < 8: #adds padding
        preseg = '0' + preseg

    if preseg == '11111111' and len(asciimsg) - len(seg) > 0: preseg = '1'
    else: preseg = '0' + preseg

    fullmsg += preseg + seg #adds preseg and seg to fullmsg
    debugg += '-' + preseg + '-' + seg

    asciimsg = asciimsg[255:] #cuts the first 255 bits from asciimsg

print(debugg)


hide(fullmsg, hidingPlace) #calls the hiding function






