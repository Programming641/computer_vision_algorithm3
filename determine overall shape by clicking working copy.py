import tkinter
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import pixel_shapes_functions
from statistics import mean
import math
import read_files_functions


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   


def get_clicked_shape(event):
   global shapes
   global clicked_enlarged_image
   global read_clicked_enlarged_image
   global image_magnification

   print("mouse clicked on image")
   print('X=%s Y=%s' % (event.x, event.y))
      
   # converting x y coordinates on enlarged image to original image x y coordinates
   original_image_x = round(event.x / image_magnification)
   original_image_y = round(event.y / image_magnification)
    
   clicked_image_index = math.floor(original_image_y * original_image_width + original_image_x)
   
   clicked_shape = {}
   
   break_flag = False

   # now that we have clicked index, we need to match it with shape's index
   for shape_id in shapes:
   

      for pixel_id in shapes[shape_id]:
         if pixel_id == clicked_image_index:
         
            clicked_shape[shape_id] = {}
         
            # getting all pixels of the clicked shape
            for pixel_ids in shapes[shape_id]:
               clicked_shape[shape_id][pixel_ids] = {'x': shapes[shape_id][pixel_ids]['x'], 'y': shapes[shape_id][pixel_ids]['y'] }
               break_flag = True

         if break_flag == True:
            break
      if break_flag == True:
         break    



   # now we have clicked shape
   # we then need to convert original image xy coordinates to enlarged image coordinates
   
   for shape_id in clicked_shape:
      for pixel_ids in clicked_shape[shape_id]:
      
         x = clicked_shape[shape_id][pixel_ids]['x']
         y = clicked_shape[shape_id][pixel_ids]['y']
      
         # ---------------------------      converting original image to enlarged image algorithm      ------------------------------
         # every pixel in original image will increase by magnification amount
         # for example, pixel 0 will be 9 in magnifcation of 3. every pixel will increase horizontally and verically by magnifcation amount
         # In magnification of 3, 1 pixel will fill 3 pixels horizontally and vertically. so (1 pixel * 3 horizontally ) * ( 1pixel * 3 vertically ) = 9 pixels
         for vertical_increase in range(0, image_magnification):
            for horizontal_increase in range(0, image_magnification ):
               enlarged_pixel_index = ((y * image_magnification ) + vertical_increase ) * enlarged_width + (x * image_magnification) + horizontal_increase
            
               enlarged_y = math.floor(enlarged_pixel_index / (original_width * image_magnification) )
               enlarged_x = enlarged_pixel_index % (original_width * image_magnification )
               print(" clicked x on enlarged image " + str(enlarged_x))
               print(" clicked y on enlarged image " + str(enlarged_y))

               read_enlarged_image.putpixel( (enlarged_x, enlarged_y) , (255, 255, 255) )
               
   read_enlarged_image.save("temp.png")
   clicked_enlarged_image = Image.open("temp.png")
   read_clicked_enlarged_image = ImageTk.PhotoImage(image = clicked_enlarged_image)

   print("complete")


def show_clicked_image():
   global canvas
   global image_on_canvas
   global clicked_enlarged_image
   global read_clicked_enlarged_image
   

   canvas.itemconfig(image_on_canvas, image = read_clicked_enlarged_image)


image_filename = "swan color group"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'



image_original = 'images/' + directory + image_filename + '.png'
enlarged_image = 'images/' + directory + image_filename + ' x3 enlarged.png'

shapes_filename = 'shapes/' + image_filename + ' shapes.txt'

read_enlarged_image = Image.open(enlarged_image)
read_original_image = Image.open(image_original)

original_width, original_height = read_original_image.size
enlarged_width, enlarged_height = read_enlarged_image.size


original_image_pixels = read_original_image.getdata()

original_image_width, original_image_height = read_original_image.size

image_magnification = 3

# getting all shapes of the image
shapes = read_files_functions.read_shapes_file(image_filename, directory)

canvas = None
image_on_canvas = None
clicked_enlarged_image = None
read_clicked_enlarged_image = None

def first_gui():


    def open_second_gui():

        second_gui()



    global canvas
    global image_on_canvas

    root = Tk()

    # canvas for image
    canvas = tkinter.Canvas(root, width=read_enlarged_image.width + 10, height=read_enlarged_image.height + 10)
    canvas.grid(row=0, column=0)

    first_image = ImageTk.PhotoImage(image = read_enlarged_image)

    # set first image on canvas
    image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = first_image)

    button = Button(root, text="open second window", command=open_second_gui)
    button.grid()
    
    button = Button(root, text="show clicked image", command=show_clicked_image)
    button.grid()
    canvas.bind("<Button-1>", get_clicked_shape)

    root.mainloop()




def second_gui():


    def close_gui():
        second_window.destroy()




if __name__ == '__main__':
    first_gui()





