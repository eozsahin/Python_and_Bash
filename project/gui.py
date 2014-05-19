#!/usr/bin/python

# gui.py

import wx
import math
from ExtendedStegano import ExtendedStegano

class dataTransfer():
    """
    Used by two different classes to maintain a data transfer that consists of the addr of stegomedium
    """
    def __init__(self):
        self.addr = ""

    #get and set methods
    def setAddr(self,new_addr):
        self.addr = new_addr
    def getAddr(self):
        return self.addr
class PageOne(wx.Panel):
    """
    Embed tab in the gui
    """
    def __init__(self, parent,data):

        direction = ['vertical','horizontal']
        #set font values for the gui
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        font.SetWeight(wx.FONTWEIGHT_BOLD)

        font2 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font2.SetPointSize(11)

        wx.Panel.__init__(self, parent)

        #a timer that check if the stegomedium is changed every second
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, lambda event:self.checkImageLoaded(event,data,st6,self), self.timer)

        #medium path label
        st5 = wx.StaticText(self, -1,"Medium Path: ",(50,300))
        st5.SetFont(font)

        st6 = wx.StaticText(self,-1,"",(190,300))
        st6.SetSize((250,25))
        st6.SetFont(font2)

        #source path label
        st4 = wx.StaticText(self, -1,"Source Path: ",(50,350))
        st4.SetFont(font)

        #source path input
        tc3 = wx.TextCtrl(self,-1,"",(190,350))
        tc3.SetSize((340,25))
        tc3.SetFont(font2)

        #target path label
        st1 = wx.StaticText(self, -1,"Target File Path: ",(50,400))
        st1.SetFont(font)

        #target path input
        tc = wx.TextCtrl(self,-1,"",(190,400))
        tc.SetSize((340,25))
        tc.SetFont(font2)

        #scannign direction label
        st2 = wx.StaticText(self, -1,"Scanning Direction: ",(50,450))
        st2.SetFont(font)

        #scanning direction combobox
        combobox = wx.ComboBox(self, pos=(190,450), size=(150, 25), choices=direction)

        #encryption checkbox
        checkbox = wx.CheckBox(self, -1, 'Apply Encryption', (50, 500))
        checkbox.SetFont(font)

        #key label and input
        st3 = wx.StaticText(self, -1,"Key",(50,550))
        st3.SetFont(font)
        tc2 = wx.TextCtrl(self,-1,"",(190,550))
        tc2.SetSize((340,25))
        tc2.SetFont(font2)

        #button for embedding
        button = wx.Button(self, -1, 'Embed Image', pos = (190, 570))
        button.SetSize((200,100))



        self.Bind(wx.EVT_BUTTON, lambda event: self.buttonEmbedClick(event, combobox,tc,tc3,checkbox,data,tc2),button)

    def buttonEmbedClick(self,event,combobox,target_path,src_p,checkbox,data,tc2):
        """
        Method that is fired when the embed button is clicked. Takes all info inside the embed tab and calls the ExtendedStegano.py class to embed
        """

        #check if stegomedium is selected properly
        if(data.addr != ""):

            #get the values from the embed tab
            key = tc2.GetValue()
            dir =  combobox.GetValue()
            encryption = checkbox.GetValue()
            file_path = target_path.GetValue()
            source_path = src_p.GetValue()

            #check if the source path is specified
            if(source_path == ""):
                wx.MessageBox('Error: Source path not specified', 'Error!', wx.OK | wx.ICON_ERROR)
            #check if the file path is specified
            elif(file_path == ""):
                wx.MessageBox('Error: Target path not specified', 'Error!', wx.OK | wx.ICON_ERROR)
            else:
                #get the extension
                s = source_path.split('/')

                s_size = len(s)
                s = s[s_size-1]
                #print "file:",s
                ext = s.split('.')[1]

                try:
                    #create stegano object with stegomedium and the direction of given
                    steganoObj = ExtendedStegano(data.addr,dir)

                    #process for different embeds
                    if(ext == "txt"):
                        if(encryption == True):
                            steganoObj.embedMessageWithKey(file_path,source_path,key)
                        else:
                            steganoObj.embedMessage(file_path,source_path)

                        #wx.MessageBox("Your message is embedded successfully!", 'Success!', wx.OK | wx.ICON_INFORMATION)
                    elif(ext == "tif" or ext =="tiff"):
                        #if(encryption == True):
                        #    steganoObj.embedImageWithKey(file_path,source_path,key)
                        #else:
                        steganoObj.embedImage(file_path,source_path)
                        #wx.MessageBox("Your image is embedded successfully!", 'Success!', wx.OK | wx.ICON_INFORMATION)

                except IOError as e:
                    wx.MessageBox(str(e), 'Error!', wx.OK | wx.ICON_ERROR)
                except ValueError as e:
                    wx.MessageBox(str(e), 'Error!', wx.OK | wx.ICON_ERROR)
        else:
             wx.MessageBox('Please load an image from the menu as stego-medium first!', 'Error!', wx.OK | wx.ICON_ERROR)


    def checkImageLoaded(self,e,data,st6,panel):
        """
        This method is responsible of checking if the stegomedium is selected. If it is selected it displays the image.
        """
        if(data.addr != ""):
            imageFile = data.addr
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)

            w = jpg1.GetWidth()
            h = jpg1.GetHeight()
            #image scaling to fit in the gui
            while( w > 300 and h > 300):
                w = w/2
                h = h/2
            jpg1 = jpg1.Rescale(h,w)
            jpg1 = jpg1.ConvertToBitmap()

            #display the image in the gui
            wx.StaticBitmap(panel, -1, jpg1,pos=(300-(w/2),5), size=(w, h))
            st6.SetLabel(data.addr)

class PageTwo(wx.Panel):
    """
    This tab is for extraction in gui
    """
    def __init__(self, parent,data):

        direction = ['vertical','horizontal']
        type = ['Message','Image']
        #set the fonts in gui elements
        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)
        font.SetWeight(wx.FONTWEIGHT_BOLD)
        font2 = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font2.SetPointSize(11)

        wx.Panel.__init__(self, parent)

        #create a timer that keeps track of stegomedium being loaded
        self.timer = wx.Timer(self)
        self.timer.Start(1000)
        self.Bind(wx.EVT_TIMER, lambda event:self.extrImageLoaded(event,data,st6,self), self.timer)

        #medium path label
        st5 = wx.StaticText(self, -1,"Medium Path: ",(50,300))
        st5.SetFont(font)

        st6 = wx.StaticText(self,-1,"",(190,300))
        st6.SetSize((250,25))
        st6.SetFont(font2)

        #target file path label
        st1 = wx.StaticText(self, -1,"Target File Path: ",(50,350))
        st1.SetFont(font)

        #target file path input
        tc = wx.TextCtrl(self,-1,"",(190,350))
        tc.SetSize((340,25))
        tc.SetFont(font2)

        #scanning direciton label
        st2 = wx.StaticText(self, -1,"Scanning Direction: ",(50,400))
        st2.SetFont(font)

        #scanning direction combobox
        combobox = wx.ComboBox(self, pos=(190,400), size=(150, 25), choices=direction)

        #message type label
        st4 = wx.StaticText(self, -1,"Message Type: ",(50,450))
        st4.SetFont(font)

        #message type combobox
        combobox2 = wx.ComboBox(self, pos=(190,450), size=(150, 25), choices=type)

        #apply decryption checkbox
        checkbox = wx.CheckBox(self, -1, 'Apply Decryption', (50, 500))
        checkbox.SetFont(font)

        st3 = wx.StaticText(self, -1,"Key",(50,550))
        st3.SetFont(font)
        tc2 = wx.TextCtrl(self,-1,"",(190,550))
        tc2.SetSize((340,25))
        tc2.SetFont(font2)

        #extract message button
        button = wx.Button(self, -1, 'Extract Message', pos = (190, 570))
        button.SetSize((200,100))

        #extract message button event
        self.Bind(wx.EVT_BUTTON, lambda event: self.buttonExtractClick(event, combobox,tc,combobox2,checkbox,data,tc2),button)

    def extrImageLoaded(self,e,data,st6,panel):
        """
        keeps track of the stegomedium file. If it is loaded than it will show the image in gui
        """
        if(data.addr != ""):
            imageFile = data.addr
            jpg1 = wx.Image(imageFile, wx.BITMAP_TYPE_ANY)
            # bitmap upper left corner is in the position tuple (x, y) = (5, 5)

            w = jpg1.GetWidth()
            h = jpg1.GetHeight()
            #scale image
            while( w > 300 and h > 300):
                w = w/2
                h = h/2
            jpg1 = jpg1.Rescale(h,w)
            jpg1 = jpg1.ConvertToBitmap()

            #display image in the gui
            wx.StaticBitmap(panel, -1, jpg1,pos=(300-(w/2),5), size=(w, h))
            st6.SetLabel(data.addr)

    def buttonExtractClick(self,e,combobox,tc,combobox2,checkbox,data,tc2):
        """
        Method that is responsible for extracting.
        """

        #check if the stegomedium is specified
        if(data.addr != ""):
            #get all the data from the gui
            dir = combobox.GetValue()
            message_type = combobox2.GetValue()
            decryption = checkbox.GetValue()
            key = tc2.GetValue()
            target_path = tc.GetValue()

            #check if the target path is specified
            if(target_path == ""):
                wx.MessageBox('Error: Target path not specified', 'Error!', wx.OK | wx.ICON_ERROR)
            else:

                fname = target_path.split('/')
                ext = fname[len(fname)-1].split('.')[1]


                try:
                    #create stegano obj
                    SteganoObj = ExtendedStegano(data.addr,dir)

                    #given the type extract it from stegomedium and store it in the path
                    if(message_type == "Image"):
                        if(ext == "tif"):
                            SteganoObj.extractImage(target_path)
                            #wx.MessageBox("Your image is extracted successfully!", 'Success!', wx.OK | wx.ICON_INFORMATION)
                        else:
                            wx.MessageBox("Error: Choose correct message type for given target file path", 'Error!', wx.OK | wx.ICON_ERROR)
                    else:
                        if(ext == "txt"):
                            if(decryption):
                                SteganoObj.extractMessageWithKey(target_path,key)
                            else:
                                SteganoObj.extractMessage(target_path)
                           # wx.MessageBox("Your message is extracted successfully!", 'Success!', wx.OK | wx.ICON_INFORMATION)
                        else:
                            wx.MessageBox("Error: Choose correct message type for given target file path", 'Error!', wx.OK | wx.ICON_ERROR)
                except ValueError as e:
                    wx.MessageBox(str(e),'Error!', wx.OK | wx.ICON_ERROR)
                except IOError as e:
                    wx.MessageBox(str(e),'Error!', wx.OK | wx.ICON_ERROR)

        else:
             wx.MessageBox('Please load an image from the menu as stego-medium first!', 'Error!', wx.OK | wx.ICON_ERROR)






class Gui(wx.Frame):

    def __init__(self, *args, **kwargs):
        super(Gui, self).__init__(*args, **kwargs)

        #create the gui with size and title
        self.InitUI()
        self.SetSize((600,750))
        self.SetMaxSize((600, 750))
        self.SetMinSize((600, 750))
        self.SetTitle('Steganography')
        self.Centre()
        self.Show(True)

    def InitUI(self):

        data = dataTransfer()

        #create the menubar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        help_menu = wx.Menu()
        about = wx.Menu()

        #create the file menu
        fitem1 = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
        fitem2 = fileMenu.Append(wx.ID_OPEN, '&Load', 'Open Image')
        menuAbout= fileMenu.Append(wx.ID_ABOUT, "About"," Information about this program")
        menubar.Append(fileMenu, '&File')
        menubar.Append(help_menu, '&Help')

        #event handling for menu
        self.SetMenuBar(menubar)
        self.Bind(wx.EVT_MENU, self.OnQuit, fitem1)
        self.Bind(wx.EVT_MENU,lambda event: self.OnFileOpen(event,data), fitem2)
        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)

        panel = wx.Panel(self)

        font = wx.SystemSettings_GetFont(wx.SYS_SYSTEM_FONT)
        font.SetPointSize(12)

        vbox_main = wx.BoxSizer()
        #create notebook
        nb = wx.Notebook(panel)

        #notebook tabs
        Page1 = PageOne(nb,data)
        Page2 = PageTwo(nb,data)

        nb.AddPage(Page1,"Embed")
        nb.AddPage(Page2,"Extract")

        vbox_main.Add(nb,1,wx.EXPAND)
        panel.SetSizer(vbox_main)


    def OnQuit(self, e):
        """
        Menu Quit function
        """
        self.Close()

    def OnFileOpen(self, event,data):
        """
        File load data
        """
        dlg = wx.FileDialog(self, "Open","(*.tiff) | (*.tif)",style = wx.FD_OPEN)

        if (dlg.ShowModal() == wx.ID_OK):
            self.fileName = dlg.GetFilename()
            self.dirName = dlg.GetDirectory()
            self.path = dlg.GetPath()
            data.setAddr(self.path)

        dlg.Destroy()
    def OnAbout(self,e):
        """
        Menu about info
        """
        wx.MessageBox('By Emre Ozsahin', 'Steganography', wx.OK | wx.ICON_INFORMATION)

if __name__ == '__main__':

    app = wx.App()
    Gui(None, title='Stegonagrapy')
    app.MainLoop()
