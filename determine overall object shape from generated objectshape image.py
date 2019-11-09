import tkinter
from tkinter import *
from tkinter import ttk

from PIL import Image, ImageTk
import pixel_shapes_functions
from statistics import mean
import math


filename = "bird01 color group"

directory = "bird"

# directory is specified but does not contain /
if directory != "" and directory.find('/') == -1:
   directory +='/'


enlarged_image = 'shapes/objectshape/' + filename + ' shape x3 enlarged.png'
image_original = 'shapes/objectshape/' + filename + ' shape.png'


read_enlarged_image = Image.open(enlarged_image)
read_original_image = Image.open(image_original)

original_image_pixels = read_original_image.getdata()


enlarged_width, enlarged_height = read_enlarged_image.size

original_width, original_height = read_original_image.size




image_file = open('shapes/objectshape/' + filename + ' matched shape ids.txt')
image_file_contents = image_file.read()




checkbuttons = {}









def _from_rgb(rgb):
    """translates an rgb tuple of int to a tkinter friendly color code
    """
    return "#%02x%02x%02x" % rgb   


def button1_clicked():


    global checkbuttons

    checked_index_number = []
    
    
    for i in checkbuttons:


        # チェックされているか？
        if checkbuttons[i].get():
            checked_index_number.append(i)
            checked_index_number = list(dict.fromkeys(checked_index_number))


    shapeIDs_with_all_indexes = pixel_shapes_functions.get_all_pixels_of_shapes(checked_index_number, filename, directory)

    for shape_id in shapeIDs_with_all_indexes:
    

    
        for pixel_index in shapeIDs_with_all_indexes[shape_id]: 
        
        
           pixel_index = int(pixel_index)
           
           y = math.floor(pixel_index / original_width)

           x  = pixel_index % original_width




           read_original_image.putpixel( (x, y) , (255, 255, 255) )

    read_original_image.show()




def first_gui():
    def open_second_gui():

        second_gui()


    root = tkinter.Tk()



    # canvas作成
    test_canvas = tkinter.Canvas(root, width=read_enlarged_image.width, height=read_enlarged_image.height)
    test_canvas.grid(row=0, column=0)

    image_origin_posX = 10
    image_origin_posY = 10



    # canvasに画像を表示
    im = ImageTk.PhotoImage(image=read_enlarged_image)
    test_canvas.create_image(image_origin_posX, image_origin_posY, anchor='nw', image=im)


    textvar = StringVar()

    content = ttk.Frame(root)
    content['padding'] = (15,10,15,0)
    namelbl = ttk.Label(content,text='display individual shapes of this object shape')

    cancel = ttk.Button(content, text="open second window", command=open_second_gui)

    content.grid(column=1, row=0)
    namelbl.grid(column=1, row=0, columnspan=2)
    cancel.grid(column=2, row=2)

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
       

    image_original = 'images/' + directory + filename + '.png'

    read_original_image = Image.open(image_original)

    original_pixel = read_original_image.getdata()

    image_width, image_height = read_original_image.size

    new_image = Image.new('RGB', (image_width, image_height) )


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
           pixel_index_R, pixel_index_G, pixel_index_B, alpha = original_pixel[ pixel_index ]

           Red.append(pixel_index_R)
           Green.append(pixel_index_G)
           Blue.append(pixel_index_B)
        

        # dynamically create individual shapes when the second window opens

        #Frame作成
        frame_list[shape_id] = tkinter.Frame(second_window)
        

        my_text = tkinter.Label( frame_list[shape_id], text=str(shape_id) )
        my_text.grid(row= 0, column = 2)


        r = round(mean(Red))
        g = round(mean(Green))
        b = round(mean(Blue))




        background_label = tkinter.Label( frame_list[shape_id], background=_from_rgb((r, g, b)), width=5, height=2 )
        background_label.grid(row=0 ,column=1 )

        checkbuttons[shape_id] = tkinter.IntVar()

        display_individual_shape = ttk.Checkbutton( frame_list[shape_id] , variable=checkbuttons[shape_id])
        display_individual_shape.grid(row=0, column= 0)

        
        frame_list[shape_id].grid(row=frame_row_counter, column=frame_column_counter)

        frame_row_counter += 1


        # displaying frames in subseqent columns
        if frame_row_counter == 15:
           frame_row_counter = 0
           frame_column_counter += 1



    cancel = ttk.Button(second_window, text="close window", command=close_gui)
    cancel.grid()



    #Button
    button1 = ttk.Button(
        second_window, 
        text='show chosen individual shapes', 
        padding=5,
        command=button1_clicked)

    button1.grid()


    explanation_label = tkinter.Label( second_window, text=' Here, you see individual shape color along with shape id number. \
	                    Please put check in check box to choose individual shape.', 
                        font=("Helvetica", 16, "bold")	)
    explanation_label.grid( columnspan = 5)




    second_window.mainloop()









if __name__ == '__main__':
    first_gui()



