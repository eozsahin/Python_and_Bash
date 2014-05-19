__author__ = 'emreozsahin'

#!/usr/bin/env python

from ExtendedStegano import ExtendedStegano
import math
import os

img_name = "/Users/emreozsahin/Documents/yazilim/python/project/lena.tif"
embedded_image = "embedded_lena.tif"
save_path = "/Users/emreozsahin/Documents/yazilim/python/project/embedded_img.tif"
arma_image_path = "/Users/emreozsahin/Documents/yazilim/python/project/arma.tiff"
grayscale_img_image_path = "/Users/emreozsahin/Documents/yazilim/python/project/grayscale_img.tif"
arma_extract_image_path = "/Users/emreozsahin/Documents/yazilim/python/project/new_arma.tif"
g_extract_image_path = "/Users/emreozsahin/Documents/yazilim/python/project/new_grayscale.tif"
extract_message_path = "/Users/emreozsahin/Documents/yazilim/python/project/new_txt.txt"
test_str_1 = "/Users/emreozsahin/Documents/yazilim/python/project/text.txt"

style_hor = "horizontal"
style_ver = "vertical"
key = "abc"


#test case 1: embed and extract message - WORKS
s1 = ExtendedStegano(img_name,style_hor)#
res = s1.embedImage(save_path,grayscale_img_image_path)
print "res ",res

s8 = ExtendedStegano(embedded_image,style_hor)
success = s8.extractImage(g_extract_image_path)


"""
#test cas2: embed with key and extract with key - WORKS
sobj = ExtendedStegano(img_name,style_ver)
sobj.embedMessageWithKey(save_path,test_str_1,key)

sobj2 = ExtendedStegano(embedded_image,style_ver)
check = sobj2.extractMessageWithKey(extract_message_path,key)
print check
"""



"""
example from alex:

#Testing the embedding
myStenago = Steganography("lena.tif", scanningDirection="H")
targetImagePath = "embedded.tif"
isSuccessful = myStegano.embedMessage(targetPath=targetImagePath, message=messageToEmbed, encryptionKey=myKey)

# Testing the extraction
myStenago2 = Steganography(" embedded.tif ", scanningDirection="H")
extractedMessage = myStegano.extractMessage(encryptionKey=myKey)
print extractedMessage
"""