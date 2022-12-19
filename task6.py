import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
import cv2


class Camera():

    rectangles = np.array([[-50, -50]], int)

    def __init__(self):
        self.win = tk.Tk()
        self.label = tk.Label(self.win)
        self.label.grid(row=0, column=0, rowspan=1)
        self.cap = cv2.VideoCapture(0)
        self.show_frames()
        self.win.mainloop()
        self.cap.release()

    def mouseButtonClick(self, event):
        self.rectangles = np.append(self.rectangles, [[event.x, event.y]], axis=0)
        print([event.x, event.y])

    def quit(self):
        self.win.destroy()
        self.cap.release()

    def clear(self):
        print("Button c pressed")
        self.rectangles = np.array([[-50, -50]], int)

    def keyPressed(self, event):
        if event.char == 'q':
            self.quit()
        if event.char == 'c':
            self.clear()

    def show_frames(self):
        delta = 10
        cv2image = cv2.cvtColor(self.cap.read()[1], cv2.COLOR_BGR2RGB)
        for coords in self.rectangles:
            cv2.rectangle(cv2image, (coords[0] - delta, coords[1] - delta), (coords[0] + delta, coords[1] + delta), (0, 255, 0))
        img = Image.fromarray(cv2image)
        imgtk = ImageTk.PhotoImage(image=img)
        self.label.imgtk = imgtk
        self.label.configure(image=imgtk)
        self.label.bind("<Button-1>", self.mouseButtonClick)
        self.win.bind("<KeyPress>", self.keyPressed)
        self.label.after(1, self.show_frames)

Camera()
