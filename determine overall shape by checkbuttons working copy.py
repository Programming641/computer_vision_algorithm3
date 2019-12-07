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



def set_individual_shapes_clicked():

    global checkbuttons
    global chosen_individual_shapes
    global filename
    global chosen_enlarged_image
    global read_chosen_enlarged_image
    global image_magnification

    temp_clicked_shapes = []  
    
    for i in checkbuttons:
       # getting checked checkbuttons
       if checkbuttons[i].get():

          if not i in chosen_individual_shapes:

             chosen_individual_shapes.append(i)
             print(" chosen_individual_shapes " + str(chosen_individual_shapes))
             temp_clicked_shapes.append(i)
             print(" temp clicked shape " , end="")
             print(temp_clicked_shapes)

    shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(temp_clicked_shapes, filename, directory)
    print(shapeIDs_with_all_indexes)

    for shape_id in shapeIDs_with_all_indexes:
    
        for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
        
        
           pixel_index = int(pixel_index)
           
           y = math.floor(pixel_index / original_width)

           x  = pixel_index % original_width

           # ---------------------------      converting original image to enlarged image algorithm      ------------------------------
           # every pixel in original image will increase by magnification amount
           # for example, pixel 0 will be 9 in magnifcation of 3. every pixel will increase horizontally and verically by magnifcation amount
           # In magnification of 3, 1 pixel will fill 3 pixels horizontally and vertically. so (1 pixel * 3 horizontally ) * ( 1pixel * 3 vertically ) = 9 pixels
           for vertical_increase in range(0, image_magnification):
              for horizontal_increase in range(0, image_magnification ):
                 enlarged_pixel_index = ((y * image_magnification ) + vertical_increase ) * enlarged_width + (x * image_magnification) + horizontal_increase
                
                 enlarged_y = math.floor(enlarged_pixel_index / (original_width * image_magnification) )
                 enlarged_x = enlarged_pixel_index % (original_width * image_magnification )


                 read_enlarged_image.putpixel( (enlarged_x, enlarged_y) , (255, 255, 255) )

    read_enlarged_image.save("temp.png")
    chosen_enlarged_image = Image.open("temp.png")
    read_chosen_enlarged_image = ImageTk.PhotoImage(image = chosen_enlarged_image)
    
           

def show_image():
   global read_chosen_enlarged_image
   global canvas
   global image_on_canvas
   global clicked_enlarged_image_flag
   global read_clicked_enlarged_image
   
   if clicked_enlarged_image_flag == True:
      canvas.itemconfig(image_on_canvas, image = read_clicked_enlarged_image)
      clicked_enlarged_image_flag = False
   else:
      canvas.itemconfig(image_on_canvas, image = read_chosen_enlarged_image)


def set_all_checkbuttons():
   global checkbuttons

   for i in checkbuttons:
      checkbuttons[i].set(1)

   set_individual_shapes_clicked()


def get_clicked_shape(event):

   global shapes
   global image_magnification
   global chosen_individual_shapes
   global checkbuttons
   global clicked_enlarged_image_flag
   global read_clicked_enlarged_image
   
   print("mouse clicked on image")
   print('X=%s Y=%s' % (event.x, event.y))

   # converting x y coordinates on enlarged image to original image x y coordinates
   original_image_x = round(event.x / image_magnification)
   original_image_y = round(event.y / image_magnification)
    
   clicked_image_index = math.floor(original_image_y * original_width + original_image_x)
   

   clicked_shape = {}
   
   break_flag = False

   # now that we have clicked index, we need to match it with shape's index
   for shape_id in shapes:
   
      for pixel_id in shapes[shape_id]:
         if pixel_id == clicked_image_index:
         
            # we found the clicked shape's index number
            
            if shape_id in chosen_individual_shapes:
               # we want to remove shape by clicking it. Adding the shape is by clicking the checkbuttons
               chosen_individual_shapes.remove(shape_id)
               checkbuttons[shape_id].set(0)
         
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
         
         original_r, original_g, original_b = original_image_pixels[pixel_ids]
      
         # ---------------------------      converting original image to enlarged image algorithm      ------------------------------
         # every pixel in original image will increase by magnification amount
         # for example, pixel 0 will be 9 in magnifcation of 3. every pixel will increase horizontally and verically by magnifcation amount
         # In magnification of 3, 1 pixel will fill 3 pixels horizontally and vertically. so (1 pixel * 3 horizontally ) * ( 1pixel * 3 vertically ) = 9 pixels
         for vertical_increase in range(0, image_magnification):
            for horizontal_increase in range(0, image_magnification ):
               enlarged_pixel_index = ((y * image_magnification ) + vertical_increase ) * enlarged_width + (x * image_magnification) + horizontal_increase
            
               enlarged_y = math.floor(enlarged_pixel_index / (original_width * image_magnification) )
               enlarged_x = enlarged_pixel_index % (original_width * image_magnification )

               read_enlarged_image.putpixel( (enlarged_x, enlarged_y) , (original_r, original_g, original_b) )
               
   read_enlarged_image.save("temp.png")
   clicked_enlarged_image = Image.open("temp.png")
   read_clicked_enlarged_image = ImageTk.PhotoImage(image = clicked_enlarged_image)

   clicked_enlarged_image_flag = True

   print("complete")






def determine_overall_shape_clicked():

    global chosen_individual_shapes


    if len(chosen_individual_shapes) != 0:

        pixels = {}

           
        pixel_counter = 1


        # here we get all chosen pixel shapes with their pixel index numbers
        shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(chosen_individual_shapes, filename, directory)


        # Now we need to get boundary pixels of chosen shapes. To do that, we want to pass chosen individual shapes to get_boundary_pixels
        # function. But this function parameter needs to be in required dictionary form. So in this for loop, we are turning individual shapes
        # dictionary to the required form.
        for shape_id in shapeIDs_with_all_indexes:
        

        
            for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
            
            
               pixel_index = int(pixel_index)
               
               y = math.floor(pixel_index / original_width)

               x  = pixel_index % original_width


               pixels[pixel_counter] = {}
               pixels[pixel_counter] ['x'] = x
               pixels[pixel_counter] ['y'] = y
    
               pixel_counter += 1


        print(" chosen individual shapes pixels")
        print(pixels)
        print("")




        # now we can get boundary pixels of chosen individual shapes.      
        boundary_pixels = pixel_shapes_functions.get_boundary_pixels(pixels)

        print("boundary pixels " )
        print(boundary_pixels)




filename = "swan color group"

directory = ""

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'



image_original = 'shapes/objectshape/' + filename + ' shape.png'
enlarged_image = 'shapes/objectshape/' + filename + ' shape x3 enlarged.png'
read_enlarged_image = Image.open(enlarged_image)

read_original_image = Image.open(image_original)

original_image_pixels = read_original_image.getdata()

original_width, original_height = read_original_image.size
enlarged_width, enlarged_height = read_enlarged_image.size

image_magnification = 3


image_file = open('shapes/objectshape/' + filename + ' matched shape ids.txt')
image_file_contents = image_file.read()


# getting all shapes of the image
shapes = read_files_functions.read_shapes_file(filename, directory)



canvas = None
image_on_canvas = None
show_image_flag = False
chosen_enlarged_image = None
read_chosen_enlarged_image = None
test_canvas = None
clicked_enlarged_image_flag = False
read_clicked_enlarged_image = None

checkbuttons = {}
chosen_individual_shapes = []


def first_gui():



    def open_second_gui():

        second_gui()




    global canvas
    global image_on_canvas

    root = Tk()

    # canvas for image
    canvas = tkinter.Canvas(root, width=read_enlarged_image.width, height=read_enlarged_image.height)
    canvas.grid(row=0, column=0)

    first_image = ImageTk.PhotoImage(image = read_enlarged_image)

    # set first image on canvas
    image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = first_image)

    button = Button(root, text="open second window", command=open_second_gui)
    button.grid()
    
    canvas.bind("<Button-1>", get_clicked_shape)

    
    root.mainloop()



def second_gui():

    global checkbuttons
    global image_file_contents
    global initial_loading



    def close_gui():
        second_window.destroy()


    second_window = tkinter.Toplevel()

    # removing single quote, brackets and space
    pixel_indexes_string = image_file_contents.replace('\'', '') 
    pixel_indexes_string = pixel_indexes_string.strip('[]')
    pixel_indexes_string = pixel_indexes_string.replace(' ', "")

    # list with all matched shape ids
    pixel_indexes = pixel_indexes_string.split(',')

    shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(pixel_indexes, filename, directory)
       

    frame_row_counter = 0
    frame_column_counter = 0

    frame_list = {}


    for shape_id in shapeIDs_with_all_indexes:
    
        # storing RGB values for each shape. Initializing for each shape
        Red = []
        Green = []
        Blue = []
        
        for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
        
           pixel_index = int(pixel_index)
           pixel_index_R, pixel_index_G, pixel_index_B = original_image_pixels[ pixel_index ]

           Red.append(pixel_index_R)
           Green.append(pixel_index_G)
           Blue.append(pixel_index_B)
        

        # dynamically create individual shapes when the second window opens

        frame_list[shape_id] = tkinter.Frame(second_window)

        my_text = {}
        my_text[shape_id] = tkinter.Label( frame_list[shape_id], text=str(shape_id) )
        my_text[shape_id].grid(row= 0, column = 2)

        r = round(mean(Red))
        g = round(mean(Green))
        b = round(mean(Blue))

        background_label = {}
        background_label[shape_id] = tkinter.Label( frame_list[shape_id], background=_from_rgb((r, g, b)), width=5, height=2 )
        background_label[shape_id].grid(row=0 ,column=1 )

        checkbuttons[shape_id] = tkinter.IntVar()

        individual_shape_check = {}
        individual_shape_check[shape_id] = ttk.Checkbutton( frame_list[shape_id] , variable=checkbuttons[shape_id], command= set_individual_shapes_clicked)
        individual_shape_check[shape_id].grid(row=0, column= 0)

        
        frame_list[shape_id].grid(row=frame_row_counter, column=frame_column_counter)

        frame_row_counter += 1


        # displaying frames in subseqent columns
        if frame_row_counter == 20:
           frame_row_counter = 0
           frame_column_counter += 1

    show_image_button = ttk.Button(second_window, text="show image", command=show_image)
    show_image_button.grid()
    

    cancel = ttk.Button(second_window, text="close window", command=close_gui)
    cancel.grid()

    show_image_button = ttk.Button(second_window, text="set all checkbuttons", command=set_all_checkbuttons)
    show_image_button.grid()

    determine_overall_shape_button = ttk.Button(
        second_window, 
        text='determine overall object shape', 
        command=determine_overall_shape_clicked)

    determine_overall_shape_button.grid()


    initial_loading = False
    print(" initial loading inside second window " + str(initial_loading))
    

    second_window.mainloop()





if __name__ == '__main__':
    first_gui()





