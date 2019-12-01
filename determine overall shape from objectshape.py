import tkinter
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import pixel_shapes_functions
from statistics import mean
import math


def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   



def set_individual_shapes_clicked(finished=False):


    global checkbuttons
    global chosen_individual_shapes
    global show_image_flag
    global filename
    global image_objects

    # this is to either show image or finished choosing individual shapes
    if show_image_flag == True or finished == True:

        enlarged_image2 = 'shapes/objectshape/' + filename + ' shape x3 enlarged.png'
        image_magnification = 3
        enlarged_width = original_width * image_magnification
    
        if not len(image_objects) == 0:
           print(" deleting image object")
           image_objects.clear()

        image_objects.append( Image.open(enlarged_image2) ) 
        
        for i in checkbuttons:


            # チェックされているか？
            if checkbuttons[i].get():
                print(i)
                print(checkbuttons[i].get())
                chosen_individual_shapes.append(i)
                chosen_individual_shapes = list(dict.fromkeys(chosen_individual_shapes))


        shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(chosen_individual_shapes, filename, directory)

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


                     image_objects[0].putpixel( (enlarged_x, enlarged_y) , (255, 255, 255) )


        print(image_objects)
        image_objects[0].show()
        show_image_flag = False
        
        if finished == False:
           # deleting all chosen shapes for the next choosing of shapes
           chosen_individual_shapes.clear()

           

def show_image():
   global show_image_flag

   show_image_flag = True
   set_individual_shapes_clicked()




def set_all_checkbuttons():
   global checkbuttons

   for i in checkbuttons:
      checkbuttons[i].set(1)


def determine_overall_shape_clicked():

    global chosen_individual_shapes
    
    print(" am I actuall executed?" )
    
    set_individual_shapes_clicked(True)


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




image_file = open('shapes/objectshape/' + filename + ' matched shape ids.txt')
image_file_contents = image_file.read()



canvas = None
image_on_canvas = None
show_image_flag = False
image_objects = []

test_canvas = None

checkbuttons = {}
chosen_individual_shapes = []




def first_gui():


    def open_second_gui():

        second_gui()




    global canvas
    global image_on_canvas

    root = Tk()

    # canvas for image
    canvas = tkinter.Canvas(root)
    canvas.grid(row=0, column=0)

    read_enlarged_image = Image.open(enlarged_image)


    first_image = ImageTk.PhotoImage(image = read_enlarged_image)

    # set first image on canvas
    image_on_canvas = canvas.create_image(0, 0, anchor = NW, image = first_image)

    button = Button(root, text="open second window", command=open_second_gui)
    button.grid()


    # button to change image
    button = Button(root, text="show image", command=show_image)
    button.grid()

    root.mainloop()




def second_gui():

    global checkbuttons
    global image_file_contents




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
        

        my_text = tkinter.Label( frame_list[shape_id], text=str(shape_id) )
        my_text.grid(row= 0, column = 2)


        r = round(mean(Red))
        g = round(mean(Green))
        b = round(mean(Blue))


        background_label = tkinter.Label( frame_list[shape_id], background=_from_rgb((r, g, b)), width=5, height=2 )
        background_label.grid(row=0 ,column=1 )

        checkbuttons[shape_id] = tkinter.IntVar()

        display_individual_shape = ttk.Checkbutton( frame_list[shape_id] , variable=checkbuttons[shape_id], command=set_individual_shapes_clicked)
        display_individual_shape.grid(row=0, column= 0)

        
        frame_list[shape_id].grid(row=frame_row_counter, column=frame_column_counter)

        frame_row_counter += 1


        # displaying frames in subseqent columns
        if frame_row_counter == 15:
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




    second_window.mainloop()





if __name__ == '__main__':
    first_gui()





