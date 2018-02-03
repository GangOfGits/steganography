import tkinter
from PIL import Image

def go():
    global readOrWrite
    if readOrWrite == 'Write':
        hide()
    elif readOrWrite == 'Read':
        seek()
    


def seek():
    imageName = fileEntry.get()
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

    #print(binStr)
    out = ''
    while len(binStr) > 0: #iterate through the collected bits
        out += chr(int(binStr[:8],2)) #add the ascii values of the integer values of the first 8 bits of binStr to the output
        binStr = binStr[8:] #remove the first eight bits of binStr

    #print(out) #print the rcovered message
    textBox.delete('0.0', 'end')
    textBox.insert('0.0', out)




def hide():
    imageName = fileEntry.get() #input('where would you like to hide your msg? >')
    msg = textBox.get('0.0', 'end') #input('what would you like to hide? >') #gets the text to hide

    ##converts the string msg into a string of binary ascii values
    asciimsg = ''
    for c in msg:
        b = bin(ord(c))[2:]
        while len(b) < 8:
            b = '0' + b
        asciimsg += b
    #at this point ascii message is a string of 1s and 0s, each byte representing the ascii value of a charecter

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

        asciimsg = asciimsg[255:] #cuts the first 255 bits from asciimsg


    ##the following code hides the message
    image = Image.open(imageName)
    imageSiz = image.size #gets size of the image
    img = image.load() #allows pixel access
        
    char = 0 #how far through asciimsg have we written
    y = 0
    while y <= imageSiz[1] and char < len(fullmsg): #nested loopd iterate through pictures, conditions ensure we dont write more than the picture can hold
        x = 0
        while x <= imageSiz[0] and char < len(fullmsg):
            if fullmsg[char] == '1': #if we a righting a 1
                if img[x,y][0] % 2 == 0: #check if the red value is even, if the value is even it will end in zero so we must ajust by 1
                    prev = img[x,y] #this and next 4 for editing red value
                    if prev[0] > 1:
                        img[x,y] = (prev[0] - 1,prev[1],prev[2]) #edits the pixel's red
                    else:
                        img[x,y] = (prev[0] + 1,prev[1],prev[2])
                #print('1 :', str(x), str(y), bin(img[x,y][0])[-1:])

            elif fullmsg[char] == '0': #same as above only for zeros
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

    image.save(outFile.get()) #save the image as done.png (poor practice to hard code i know)



##controls the GUI

wordLook = 'Lucinda 9'
readOrWrite = 'Write'

def butControl(val): #toggle what it say on goBut between read and write
    global readOrWrite
    readOrWrite = val
    goBut.config(text=val)

window = tkinter.Tk()
window.title('Steganography')
window.wm_iconbitmap('glass.ico')

##pic = tkinter.Label(window, text='place holder', borderwidth=10,)
##pic.grid(row=0, column=0, rowspan=4, columnspan=5, sticky='NW')

fileEntryPrompt = tkinter.Label(window, text='Input Image  :', font=wordLook).grid(row=0, column=5)
fileEntry = tkinter.Entry(window, width=22, font=wordLook)
fileEntry.grid(row=0, column=6, sticky='NE', columnspan=2, padx=3, pady=3)

outFilePrompt = tkinter.Label(window, text='Output Image :', font=wordLook).grid(row=1, column=5)
outFile = tkinter.Entry(window, width=22, font=wordLook)
outFile.grid(row=1, column=6, sticky='NE', columnspan=2, padx=3, pady=3)

readQuery = tkinter.Radiobutton(window, text='Read from input file', font=wordLook, value='Read', variable=readOrWrite, command=lambda: butControl('Read'))
writeQuery = tkinter.Radiobutton(window, text='Write to input file, save as output', font=wordLook, value='Write', variable=readOrWrite, command=lambda: butControl('Write'))
readQuery.grid(row=2, column=5, columnspan=3, sticky='NW', padx=3, pady=3)
writeQuery.grid(row=3, column=5, columnspan=3, sticky='NW', padx=3, pady=3)

textBox = tkinter.Text(window, state='normal', height=10, width=36, wrap='word', font=wordLook)
textBox.grid(row=4, column=5, sticky='NW', columnspan=3, ipadx=5, ipady=5, padx=3, pady=3)
textBox.insert('0.0', 'Text to be written')

goBut = tkinter.Button(window, font=wordLook, text='Write', width=5, command=go)
goBut.grid(row=5, column=7, sticky='NE', padx=3, pady=3)

window.mainloop()
