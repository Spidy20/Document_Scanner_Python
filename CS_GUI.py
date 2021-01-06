from PIL import ImageTk
import PIL
from PIL import ImageDraw,ImageFont
import numpy as np
from PIL import Image
from tkinter import *
import tkinter as tk
import cv2
import glob,os
import time,datetime
from urllib.request import urlopen
from pathlib import Path
from skimage.filters import threshold_local

windo = Tk()
windo.configure(background='white')
windo.title("Document Scanner App")
width = windo.winfo_screenwidth()
height = windo.winfo_screenheight()
windo.geometry(f'{width}x{height}')

windo.iconbitmap('./meta/cs.ico')
windo.resizable(0, 0)
launch = False

# Size for displaying Image
w = 385;h = 535
size = (w, h)

def launch_mob_cam():
    global cp2, crop_c, crop_images, pdf_c, pdf_b, scanned_imgs
    url = txt.get()
    crop_c = 0
    pdf_c = 0
    scanned_imgs = []

    cp2 = tk.Button(windo, text='Capture Image', bg="spring green", fg="black", width=22,
                   height=1, font=('times', 22, 'italic bold '),command = crop_image, activebackground='yellow')
    cp2.place(x=27, y=620)

    pdf_img = PIL.Image.open('./meta/pdf.png')
    pdf_img = pdf_img.resize((148, 52), PIL.Image.ANTIALIAS)
    sp_img1 = ImageTk.PhotoImage(pdf_img)

    pdf_b = Button(windo, borderwidth=0, command=pdf_gen, image=sp_img1, bg='white')
    pdf_b.pack()
    pdf_b.image = sp_img1
    pdf_b.place(x=430, y=80)

    try:
        if url == '':
            noti = tk.Label(windo, text='Check the URL!!', width=20, height=1, fg="white", bg="firebrick1",
                            font=('times', 13, ' bold '))
            noti.place(x=24, y=68)
            windo.after(2000, destroy_widget, noti)
        else:
            global display, imageFrame, cp1, img
            imageFrame = tk.Frame(windo)
            imageFrame.place(x=24, y=80)

            display = tk.Label(imageFrame)
            display.grid()

            cp1 = tk.Button(windo, text='Turn off', bg="spring green", fg="black", width=12,
                           height=1, font=('times', 14, 'italic bold '), command=destroy_cam,
                           activebackground='yellow')
            cp1.place(x=430, y=33)

            def show_frame():
                global img
                img_resp = urlopen(url)
                img_arr = np.array(bytearray(img_resp.read()), dtype=np.uint8)
                frame = cv2.imdecode(img_arr, -1)
                frame = cv2.rotate(frame, cv2.cv2.ROTATE_90_CLOCKWISE)

                # frame = cv2.VideoCapture('new.mp4')
                # _,frame = frame.read()
                cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
                rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
                img = PIL.Image.fromarray(rgb)
                img1 = img.resize(size, PIL.Image.ANTIALIAS)
                imgtk = ImageTk.PhotoImage(image=img1)
                display.imgtk = imgtk
                display.configure(image=imgtk)
                display.after(10, show_frame)
            show_frame()
    except Exception as e:
        print(e)
        noti1 = tk.Label(windo, text='Connection Closed!!', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        noti1.place(x=24, y=68)
        windo.after(2000, destroy_widget, noti1)
        imageFrame.destroy()
        display.destroy()
        cp1.destroy()
        cp2.destroy()

def destroy_widget(widget):
    widget.destroy()

def destroy_cam():
    imageFrame.destroy()
    display.destroy()
    cp1.destroy()
    cp2.destroy()


def crop_image():
    global cropping, crop_c, launch, scanned_imgs
    launch = True
    repn = Path('Cropped_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Cropped_image')
    crop_c += 1

    img1 = img.copy()
    img1 = cv2.cvtColor(np.asarray(img1), cv2.COLOR_RGB2BGR)
    cn = './Cropped_image/img_' + str(crop_c) + '.jpg'
    cv2.imwrite(cn, img1)

    imlab2 = tk.Label(windo, text="Orignal: "+ cn[16:], width=22, height=1, fg="black", bg="yellow",
                     font=('times', 15, ' bold '))
    imlab2.place(x=430, y=140)

    imageFrame2 = tk.Frame(windo)
    imageFrame2.place(x=430, y=170)

    display2 = tk.Label(imageFrame2)
    display2.grid()

    cv2image = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
    rgb = cv2.cvtColor(cv2image, cv2.COLOR_RGBA2RGB)
    img2 = PIL.Image.fromarray(rgb)
    img2 = img2.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk = ImageTk.PhotoImage(image=img2)
    display2.imgtk = imgtk
    display2.configure(image=imgtk)
    windo.after(10000, destroy_widget, display2)
    windo.after(10000, destroy_widget, imageFrame2)
    windo.after(10000, destroy_widget, imlab2)

    imgr = cv2.imread(cn)
    imgr = cv2.cvtColor(imgr, cv2.COLOR_BGR2GRAY)
    t = threshold_local(imgr, 17, offset=15, method='gaussian')
    imgr = (imgr > t).astype('uint8') * 255
    repn = Path('Processed_image')
    if repn.is_dir():
        pass
    else:
        os.mkdir('Processed_image')
    cn1 = './Processed_image/img_' + str(crop_c) + '.jpg'
    cv2.imwrite(cn1,imgr)
    scanned_imgs.append(cn1)
    print(scanned_imgs)
    imlab4 = tk.Label(windo, text="Scanned: "+ cn[16:], width=22, height=1, fg="white", bg="black",
                     font=('times', 15, ' bold '))
    imlab4.place(x=730, y=140)

    imageFrame4 = tk.Frame(windo)
    imageFrame4.place(x=730, y=170)

    display4 = tk.Label(imageFrame4)
    display4.grid()

    cv2image4 = cv2.cvtColor(imgr, cv2.COLOR_GRAY2RGBA)
    rgb4 = cv2.cvtColor(cv2image4, cv2.COLOR_RGBA2RGB)
    img4 = PIL.Image.fromarray(rgb4)
    img4 = img4.resize((270, 480), PIL.Image.ANTIALIAS)
    imgtk4 = ImageTk.PhotoImage(image=img4)
    display4.imgtk = imgtk4
    display4.configure(image=imgtk4)
    windo.after(10000, destroy_widget, display4)
    windo.after(10000, destroy_widget, imageFrame4)
    windo.after(10000, destroy_widget, imlab4)

def pdf_gen():
    global pdf_c, pdf_b, launch, scanned_imgs
    print(launch)
    if launch == False:
        noti = tk.Label(windo, text='Capture the Images first!!', width=20, height=1, fg="white", bg="firebrick1",
                        font=('times', 13, ' bold '))
        noti.place(x=24, y=68)
        windo.after(2000, destroy_widget, noti)
        destroy_cam()
        pdf_b.destroy()
    else:
        pdf_b.destroy()
        pdf_c+=1

        ## Generate folder for PDF
        repn = Path('Scanned_PDF')
        if repn.is_dir():
            pass
        else:
            os.mkdir('Scanned_PDF')

        ## Create First Intro page
        img = PIL.Image.new('RGB', (100, 30), color=(255, 255, 255))
        fnt = ImageFont.truetype('./meta/arial.ttf', 13)
        d = ImageDraw.Draw(img)
        d.text((5, 10), "Scanned PDF ", font=fnt,fill=(0, 0, 0))
        img.save('./Processed_image/z.jpg')
        scanned_imgs.append('./Processed_image/z.jpg')
        ## Generate PDF-
        image_list = []
        for image in scanned_imgs:
            img = PIL.Image.open(image)
            img = img.convert('RGB')
            image_list.append(img)
        image_list.pop(-1)
        ts = time.time()
        timeStam = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStam.split(":")
        img.save('./Scanned_PDF/Scanned_'+str(pdf_c)+'_'+str(Hour)+'_'+str(Minute)+'_'+str(Second)+'.pdf',save_all=True, append_images=image_list)
        # img.save('./Scanned_PDF/Scanned_'+str(pdf_c)+'.pdf',save_all=True, append_images=image_list)
        noti = tk.Label(windo, text='PDF Generated!!', width=20, height=1, fg="black", bg="spring green",
                        font=('times', 13, ' bold '))
        noti.place(x=24, y=68)
        windo.after(2000, destroy_widget, noti)
        destroy_cam()

lab = tk.Label(windo, text="Enter your URL", width=18, height=1, fg="white", bg="blue2",
               font=('times', 16, ' bold '))
lab.place(x=24, y=5)

txt = tk.Entry(windo, borderwidth=4, width=34, bg="white", fg="black", font=('times', 16, ' bold '))
txt.place(x=24, y=35)
txt.insert(0,'http://192.168.1.102:8080/shot.jpg')

cp = tk.Button(windo, text='Turn on', bg="midnightblue", fg="white", width=12,
               height=1, font=('times', 14, 'italic bold '), command=launch_mob_cam, activebackground='yellow')
cp.place(x=430, y=33)

windo.mainloop()