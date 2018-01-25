from PIL import Image


def seek(imageName):
    image = Image.open(imageName) #open an image
    imageSiz = image.size
    img = image.load() #allows reading of pixels

    go = True
    count = 255
    holt = -1
    readingLength = True
    lengthStr = ''
    binStr = '' #an empty string to store recovered bits
    

    y = 0 #iterate throught the images pixels 
    while y < imageSiz[1] and go == True:
        x = 0
        while x <= imageSiz[0] and go == True:
            
            bit = bin(img[x,y][0])[-1:] #add the last bit of the the binary value of the red channel of each pixel to binStr
           
            if count >= 255: #if the number of bits since the last segment of length encoding is 255
                if bit == '1' and count == 255: #if the first LE bit is a 1
                    count = -1 #reset count (so as to read till next LE segment)
                elif bit == '0' and count == 255: #if the first LE bit is a 0
                    lengthStr = '' #create a length string
            
                elif count > 255: #if we aren't on the first LE bit 
                    lengthStr += bit #add it to the length string
                if len(lengthStr) == 8: #if the length string is long enough
                    holt = int(lengthStr, 2) #set the holt so the program knows when to stop reading 
                    count = -1 #reset the count bit 
                       
            else: binStr += bit #if its a data bit add it to binStr

            count += 1

            if count == holt: #stops if all the data is read
                go = False

            x += 1
        y += 1

    print(binStr)
    return binStr




hidingPlace = input('what is the name/path of the steganographic image? >')
#msgLen = int(input('how many charecters are in the message? >'))*8

msgStr = seek(hidingPlace)

out = ''
while len(msgStr) > 0: #iterate through the collected bits
    out += chr(int(msgStr[:8],2)) #add the ascii values of the integer values of the first 8 bits of binStr to the output
    msgStr = msgStr[8:] #remove the first eight bits of binStr

print(out) #print the rcovered message
input('') #holds the window open

#please forgive multifunction lines

