#!/usr/bin/env python

import sys
import os
import math
from PIL import Image
import cypher
from Steganography import Steganography


class ExtendedStegano(Steganography):
    def __init__(self, img, dir):
        """
		Constructor for the Steganography object. It accepst image name and the embedded string
		"""
        self.img = img
        self.dir = dir

    def __isValidStr(self, message):
        """
		Validating the string that if it is possible to fit inside the image. It returns True if possible and False otherwise.
		"""
        #get the size of the image
        w, h = Image.open(str(self.img)).size
        image_size = w * h
        str_size = len(message)

        #check if the string will fit in the image
        if (8 * str_size > image_size):
            return False
        else:
            return True


    def __isValidImage(self, image_path):
        """
        Checks if stegomedium can store an image specified. Returns true if it can store.
        """

        #get both image sizes for stegomedium and the image
        try:
            w, h = Image.open(str(self.img)).size
            stego_image_size = w * h

            scriptDir = os.path.dirname(__file__)
            impath = os.path.join(scriptDir, image_path)


            width, height = Image.open(impath).size
            img_size = width * height
        except IOError as io:
            raise ValueError(str(io))

        #check if image can be embedded into stego
        if (8 * img_size > stego_image_size):
            #raise ValueError("Error: can't fit image into stego-medium")
            return False
        else:
            return True


    def __getFileNameFromPath(self, path):
        """
        Returns the filename when a path is specified
        """
        tmp = path.split('/')
        filename = tmp[len(tmp) - 1]

        return filename

    def __getFileExt(self,filename):
        """
        returns the file extension
        """
        return filename.split('.')[1]

    def __isTxt(self,path):
        """
        Checks if the path given is a text file. Returns true if it is.
        """
        filename = self.__getFileNameFromPath(path)
        ext = filename.split('.')[1]
        #print ext

        if (ext == "txt"):
            return True
        else:
            return False

    def __isImage(self,path):
        """
        Checks if the path given is an image file. Return true if it is.
        """
        image_name = self.__getFileNameFromPath(path)
        ext = image_name.split('.')[1]

        if (ext == "tif" or ext == "tiff"):
            return True
        else:
            return False


    def embedMessage(self, save_path, message_path):
        """
        Given a save path and a message path, it puts the message into the stegomedium.
        """

        byte_array = []
        mes = []
        message = ""

        if(self.__isTxt(message_path)): #check if it is a valid text file to put inside stego
            if(self.__isValidStr(message_path)): #check if the ext is txt
                scriptDir = os.path.dirname(__file__)
                mespath = os.path.join(scriptDir, message_path)
                with open(mespath,"r") as fptr: #open the file and get the message and turn into a byte array
                    lines = fptr.readlines()
                    for i in lines:
                        mes.append(i)
                    #print mes
                    #print "mes: ",mes
                    mes = [i.split('\n')[0]for i in mes]
                    message = ''.join(mes)
                    s = bytearray(message+"^")
                    #print "printing:",message
                    byte_array = [bin(i) for i in s]
                    self.__embedAny(save_path,byte_array) #gets a byte array and embeds into the given image

            else:
                print "1"
                raise ValueError("Error: Message can't fit string into stego-medium")
                return False

        else:
            print "2"
            raise ValueError("Error: Message file contains non txt file ")
            return False

        return True


    def embedImage(self, save_path, image_path):
        """
        Given the save path, puts an image inside the stegomedium.
        """
        bit_flag = 0
        byte_array = []

        if(self.__isImage(image_path)): #check if image can fit inside stego
            if(self.__isValidImage(image_path) == True):#check if the extension is ok
                scriptDir = os.path.dirname(__file__)
                impath = os.path.join(scriptDir, image_path)
                width, height = Image.open(impath).size
                #print width,height
                im = Image.open(impath)
                pix = im.load()

                if(not isinstance(pix[0,0],int)):
                    if len(pix[0,0]) > 1:
                        bit_flag = 1
                #check if it is multi colored image and creates a byte array
                for w in range(width):
                    for h in range(height):
                        if bit_flag == 1:
                            byte_array.append(bin(pix[w,h][0]))
                        else:
                            byte_array.append(bin(pix[w,h]))

                byte_array.append(bin(width))
                byte_array.append(bin(height))
                #create catching sequence in extraction. Also put the weights of the image.
                byte_array.append(bin(55))
                byte_array.append(bin(255))
                #print "byte_array: ",byte_array
                self.__embedAny(save_path,byte_array) #gives the bytearray and it embeds.
            else:
                raise ValueError("Error: can't fit image into stego-medium")
                return False
        else:
            raise ValueError("Error: Image file is not inform tif or tiff")
            return False
        return True


    def __embedAny(self,save_path,byte_array):
        pix_list = []

        #check if string is valid to embed

        #open the image and get the pixel values as well as height and width of it
        width, height = Image.open(self.img).size
        im = Image.open(self.img)
        pix = im.load()

        #if the specified direction is vertical
        if (self.dir == "vertical" or self.dir == 'v' or self.dir == 'V'):

            #get the pixel values and store them in a list with specified direction
            for w in range(width):
                for h in range(height):
                    pix_list.append(bin(pix[w, h]))

            #zero pad the byte_array and the list of pixel values
            tmp_list = [list(i.split('b')[1].rjust(8, '0')) for i in pix_list]
            byte_array = [list(x.split('b')[1].rjust(8, '0')) for x in byte_array]

            #embedd the bits of the message into the LSB of the byte in the image
            z = 0
            for bit in byte_array:
                for i in range(8):
                    tmp_list[z][7] = bit[i]
                    z = int(z) + 1
            #change format
            tmp_list = [int("".join(i), 2) for i in tmp_list]

            #with the new image bytes form a new image
            im2 = Image.new(im.mode, im.size)
            pix2 = im2.load()
            cnt = 0
            #place the bytes in the picture
            for w in range(width):
                for h in range(height):
                    pix2[w, h] = tmp_list[cnt]
                    cnt = int(cnt) + 1

        else:
            #embed the string in the horizontal direction
            #get the pixel values of the image with horizontal direction
            for h in range(height):
                for w in range(width):
                    pix_list.append(bin(pix[w, h]))
                    #store them in the tmp_list and adjust data
            tmp_list = [list(i.split('b')[1].rjust(8, '0')) for i in pix_list]
            byte_array = [list(x.split('b')[1].rjust(8, '0')) for x in byte_array]

            #embed the bits in the pixels LSB value
            z = 0
            for bit in byte_array:
                for i in range(8):
                    tmp_list[z][7] = bit[i]
                    z = int(z) + 1
            #these are the new list that contain the new pixel values including the message inside
            tmp_list = [int("".join(i), 2) for i in tmp_list]

            #open a new image and place the pixels
            im2 = Image.new(im.mode, im.size)
            pix2 = im2.load()
            cnt = 0
            for h in range(height):
                for w in range(width):
                    pix2[w, h] = tmp_list[cnt]
                    cnt = int(cnt) + 1

        #save the image new image
        im2.save(save_path)

    def embedMessageWithKey(self, save_path, message_path, key):
        """
        Embeds the given text file content into stegomedium with vigenere cyhper.
        """

        byte_array = []
        mes = []
        message = ""

        if(self.__isTxt(message_path)): #check if the file extension is txt
            if(self.__isValidStr(message_path)): #check if it can be embedded
                scriptDir = os.path.dirname(__file__)
                mespath = os.path.join(scriptDir, message_path)
                with open(mespath,"r") as fptr: #gets the message and turns into a byte_array
                    lines = fptr.readlines()
                    for i in lines:
                        mes.append(i)
                    #print mes
                    #print "mes: ",mes
                    mes = [i.split('\n')[0]for i in mes]
                    message = ''.join(mes)
                    #encrypt the message
                    message = cypher.vign_encrypt(message,key)
                    s = bytearray(message+"^")
                    #print "printing:",message

                byte_array = [bin(i) for i in s]
                #byte_array is embedded into stegomedium
                self.__embedAny(save_path,byte_array)


            else:
                raise ValueError("Error: Couldn't embed message into stego-medium")
                return False
        else:
            raise ValueError("Error: Message file contains non txt file ")
            return False
        return True


    def __extractAny(self):
        """
        Method used for any type of extraction. It returns a byte array that holds the embedded image or message.
        """

        pix_list = []
        tmp_list = []
        #open image and get width and height, pixels
        im = Image.open(self.img)
        pix = im.load()
        width,height = Image.open(self.img).size

        #with the specified direction get the current pixel values
        if(self.dir == "vertical" or self.dir == 'v' or self.dir == 'V'):
            #print "decoding in vertical fashion"
            for w in range(width):
                for h in range(height):
                    pix_list.append(bin(pix[w,h]))
        else:
            #print "deconding in horizontal fashion"
            for h in range(height):
                for w in range(width):
                    pix_list.append(bin(pix[w,h]))
        #store the pixels with adjusted values
        tmp_list = [list(i.split('b')[1].rjust(8,'0')) for i in pix_list]

        return tmp_list

        #variable declarations


    def extractMessage(self,extract_mess_path):
        """
        This method extracts message from a stegomedium. Creates the a file with given mess_path.
        """


        try:
            tmp_list = []
            tot_str = ""
            byte = ""
            cnt = 0
            flag = 1

            tmp_list = self.__extractAny()

            #obtain the image, recieve byte and check if it is valid and not the end char which is '^'
            while (flag == 1):
                for i in range(8):
                    bit = tmp_list[cnt][7]
                    cnt = int(cnt) + 1
                    byte =  byte + str(bit) #form bytes
                if(int(byte,2) == 94):
                    flag = 0
                if(int(byte,2) < 32 or int(byte,2) > 122): #check if it is valid
                    raise ValueError("Input string contains random symbols!")
                tot_str = tot_str + chr(int(byte,2))
                byte = ""

                scriptDir = os.path.dirname(__file__)
                mespath = os.path.join(scriptDir, extract_mess_path)
                with open(mespath,"w+") as fptr: #create the file and write the message into the file
                    for i in tot_str[:-1]:
                        fptr.write(i)
        except:
                raise ValueError("Error: Can not extract message from stego-medium")
                return False
        return True

    def extractMessageWithKey(self,extract_mess_path, key):
        """
        Extracts the message form stegomedium and decrypts the message given by a key.
        """


        try:
            tmp_list = []
            tot_str = ""
            byte = ""
            cnt = 0
            flag = 1

            tmp_list = self.__extractAny()

            #obtain the image, recieve byte and check if it is valid and not the end char which is '^'
            while (flag == 1):
                for i in range(8):
                    bit = tmp_list[cnt][7]
                    cnt = int(cnt) + 1
                    byte =  byte + str(bit) #form bytes
                if(int(byte,2) == 94):
                    flag = 0
                if(int(byte,2) < 32 or int(byte,2) > 122): #check if valid
                    raise ValueError("Input string contains random symbols!")
                tot_str = tot_str + chr(int(byte,2))
                #print tot_str

                message = cypher.vign_decrypt(tot_str[:-1],key) #decrypt message
                byte = ""

                scriptDir = os.path.dirname(__file__)
                mespath = os.path.join(scriptDir, extract_mess_path)
                with open(mespath,"w+") as fptr: #open the file and write the message into the file
                    for i in message:
                        fptr.write(i)
        except:
                raise ValueError("Error: Can not extract message from stego-medium")
                return False
        return True

    def extractImage(self,extract_image_path):
        """
        Extract the image from stegomedium and creates a new image.
        """

        #variable declarations
        new_byte=""
        byte = "00000000"
        cnt = 0
        flag = 1
        pixels = []

        tmp_list = self.__extractAny()

        while (flag == 1):
            for i in range(8):
                bit = tmp_list[cnt][7]
                cnt = int(cnt) + 1
                new_byte =  new_byte + str(bit) #form the bytes

            if(int(byte,2) == 55 and int(new_byte,2) == 255):
                flag = 0
            byte = new_byte
            pixels.append(int(byte,2))

            new_byte = ""

        width = pixels[len(pixels)-4] #extract the width from data
        height = pixels[len(pixels)-3] #extract the height from data

        if(width * height < len(pixels)): #check if the image really exists

            #print "height:",height
            #print "width",width

            im2 = Image.new('L', (width,height))
            pix2 = im2.load()

            cnt = 0

            #form the image
            for w in range(width):
                for h in range(height):
                    pix2[w, h] = pixels[cnt]
                    cnt = int(cnt) + 1

            im2.save(extract_image_path)
        else:
            raise ValueError("Error: Can't extract the image")








        