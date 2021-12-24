import tkinter
from tkinter import*
import cv2
import numpy as np
from tkinter import ttk, StringVar, Label, DoubleVar
from tkinter import Tk,Label,Button, messagebox, filedialog
from PIL import ImageTk, Image
from skimage.feature import graycomatrix, graycoprops
from skimage import io
from skimage import exposure
import matplotlib.pyplot as plt

class My_Gui:

    def __init__(self,window):
        self.input_filename    = StringVar()
        self.path_filename     = StringVar()
        self.property_Energy   = DoubleVar()
        self.property_Contrast = DoubleVar()
        self.var_cliplimit     = DoubleVar()

        window.title("Dutta Tool for Image Processing")
        window.geometry('800x450')
        window.configure(background='pink')

        btn_openfile=Button(window, text="Open File",font =('Helvetica',12,'bold','underline'),foreground = 'orange', command=lambda:self.set_select_file()).grid(row=0,ipadx=5,ipady=15)

        scale_widget = Scale(window, fg = 'red', label='choose the Cliplimit',orient=HORIZONTAL, resolution =1, from_=0, to =20,variable = self.var_cliplimit)
        scale_widget.grid(row=0,column=2)


        btn_openfile=Button(window, text="Pre-Processing (CLAHE)",font =('Helvetica',12,'bold','underline'),foreground = 'Brown', command=lambda:self.set_apply_clahe()).grid(row=0, column=3,ipadx=5,ipady=15)

        ttk.Label(window, background='cyan',textvariable=self.input_filename, width=70).grid(row=0,column=1, ipadx=5, ipady=15)

        btn_glcm_analysis = Button(window, text="GLCM Properties",font =('Helvetica',12,'bold','underline'),foreground = 'Blue', command=lambda:self.set_glcm_analysis()).grid(row=2,ipadx=5,ipady=15)

        ttk.Label(window, text="Energy", background='green',font=('calibre',10,'bold')).grid(row=2, column=1, ipadx=5, ipady=15)
        ttk.Entry(window, textvariable=self.property_Energy, font=('calibre',10,'bold'), width=50).grid(row=3,column=1, ipadx=5, ipady=15)

        ttk.Label(window, text="Contrast", font=('calibre',10,'bold')).grid(row=2, column=2, ipadx=5, ipady=15)
        ttk.Entry(window, textvariable=self.property_Contrast, font=('calibre',10,'bold'), width=60).grid(row=3,column=2, ipadx=5, ipady=15)

        btn_quit = Button(window, text="QUIT", font=('Helvetica',12,'bold','underline'),foreground = 'Red',command=lambda:self.quit()).grid(row=4, ipadx=5, ipady=15)

    def set_select_file(self):
        self.path_filename =filedialog.askopenfilename(initialdir="/", title="Selecct A file",filetypes=(("png files","*.png"),("bmp files","*.bmp"),("all files","*.*")))
        self.input_filename.set(self.path_filename)
        self.my_image       = ImageTk.PhotoImage(Image.open(self.path_filename))
        my_image_label = Label(image=self.my_image).grid(row=1, column=1,ipadx=5, ipady=5)


    def set_glcm_analysis(self):
             self.image = io.imread(self.path_filename)
             self.GLCM  = graycomatrix(self.image,[1],[0],symmetric=True)#[0,np.pi/4,np.pi/2,3*np.pi/4])
             self.Energy = graycoprops(self.GLCM,'energy')
             self.Contrast=graycoprops(self.GLCM,'contrast')
             self.property_Energy.set(self.Energy)
             self.property_Contrast.set(self.Contrast)

    def set_apply_clahe(self):
        self.im = cv2.imread(self.path_filename) # open CV represents image in B,G,R order however, PIL represents image in RGB order
        print('BGR image shape', self.im.shape)
        #print(self.height, self.width, no_channels) # no.of.channels are 3 for the image
        self.im1 = cv2.cvtColor(self.im, cv2.COLOR_BGR2RGB)
        print('RGB image shape:', self.im1.shape)
        self.im1 = cv2.cvtColor(self.im1, cv2.COLOR_BGR2GRAY)
        print('Gray scale image shape:', self.im1.shape)

        # Decleratin of CLAHE; clipLimit -> Threshold for contrast limiting
        clahe = cv2.createCLAHE(clipLimit = self.var_cliplimit.get())
        self.im1 = clahe.apply(self.im1)


        #self.im_preprocessed= exposure.equalize_adapthist(self.im1, clip_limit=0.02)
        self.my_image_processed = ImageTk.PhotoImage(Image.fromarray(self.im1))
        my_image_processed_label = Label(image=self.my_image_processed).grid(row=1, column=3,ipadx=5, ipady=5)




    def quit(self):
        window.destroy()


if __name__ == '__main__':
    window = tkinter.Tk()
    gui = My_Gui(window)
    window.mainloop()

#just to track the changes
