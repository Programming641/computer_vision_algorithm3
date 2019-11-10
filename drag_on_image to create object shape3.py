import tkinter
from tkinter import *
from tkinter import ttk
from PIL import Image, ImageTk
import recreate_shapes

matched_shape_id_with_mouse_circled_area = []

whole_image_shapes = recreate_shapes.get_whole_image_shape(True)   



def execute_mouse_circled_shapes( mouse_circled_x, mouse_circled_y ):

   global matched_shape_id_with_mouse_circled_area
   global whole_image_shapes


   # we are getting xy coordinates of whole image shapes. We will then get all shapes that fall inside the 
   # mouse circled image area 
   

   for shape_id , pixel_xy_values in whole_image_shapes.items():

      for pixel_id in pixel_xy_values:
      
         if pixel_xy_values[pixel_id]['x'] == mouse_circled_x and pixel_xy_values[pixel_id]['y'] == mouse_circled_y:
            # pixel falls in the mouse circled area
            if not str(shape_id) in matched_shape_id_with_mouse_circled_area:
            
               print(" shape found! shape id is " + shape_id )          
               matched_shape_id_with_mouse_circled_area.append(shape_id)
            






enlarged_image = 'images/bird/bird01 color group x3 enlarged.png'
image_original = 'images/bird/bird01 color group.png'

# finding file name under the last directory
image_directory_position = enlarged_image.rfind('/')



# object shape's filename exclude images folder name and replacing extension with txt
object_shape_filename = "shapes/objectshape/" + enlarged_image[image_directory_position + 1:-4] + ".txt"

original_image_filename = "shapes/objectshape/" + image_original[image_directory_position + 1:-4] + " matched shape ids.txt"

read_enlarged_image = Image.open(enlarged_image)
read_original_image = Image.open(image_original)
enlarged_width, enlarged_height = read_enlarged_image.size

original_width, original_height = read_original_image.size









root = tkinter.Tk()



# canvas作成
test_canvas = tkinter.Canvas(root, width=read_enlarged_image.width, height=read_enlarged_image.height)
test_canvas.grid(row=0, column=0)

image_origin_posX = 10
image_origin_posY = 10



# canvasに画像を表示
im = ImageTk.PhotoImage(image=read_enlarged_image)
test_canvas.create_image(image_origin_posX, image_origin_posY, anchor='nw', image=im)



# for storing each object shape's x, y coordinate
mouse_circled_boundary = {}
mouse_circled_boundary_counter = 0

# for storing entire mouse circled area
mouse_circled_entire_area = {}


# this is executed every movement you make with mouse
def onLeftDrag(event):


    global mouse_circled_boundary_counter
    global mouse_circled_boundary
    mouse_circled_boundary_counter += 1

    image_starting_posX = event.x  - image_origin_posX
    image_starting_posY = event.y - image_origin_posY
    print ('Widget=%s X=%s Y=%s' % (event.widget, image_starting_posX, image_starting_posY))
    
    mouse_circled_boundary[mouse_circled_boundary_counter] = {}
    mouse_circled_boundary[mouse_circled_boundary_counter]['x'] = image_starting_posX
    mouse_circled_boundary[mouse_circled_boundary_counter]['y'] = image_starting_posY
    

# this is executed when you are finished circling around and let go of the mouse button press
def saveObjectshape(event):

   global matched_shape_id_with_mouse_circled_area
   global mouse_circled_boundary
   global mouse_circled_entire_area
   

   smallest_y = min(int(d['y']) for d in mouse_circled_boundary.values())
   largest_y = max(int(d['y']) for d in mouse_circled_boundary.values())

 

   
 
   first = True
   mouse_circled_counter = 1
   
   # iterating all coordinate xy value pairs from smallest_y + 1 to largest_y - 1.
   #  for y in range(start, stop) stop value is excluded
   for y in range(smallest_y + 1, largest_y ):
      # smallest_y + 1 because smallest_y is the very top boundary.  largest_y - 1 because largest_y is the very bottom boundary
       
      # pixel_ids_with_current_y_values contains all xy coordinate pairs that have the current running y value.
      pixel_ids_with_current_y_values = [k for k in mouse_circled_boundary  if (int(mouse_circled_boundary[k]['y'])) == y]
      
      counter = 0
      # key is the coordinate pair id.
      # looking for smallest and largest x values that go with the current running y value
      for key in pixel_ids_with_current_y_values:
         counter += 1

         if first != False:
            smallest_x_with_current_y = mouse_circled_boundary[key]['x']
            largest_x_with_current_y = mouse_circled_boundary[key]['x']
            first = False
           
         if mouse_circled_boundary[key]['x'] < smallest_x_with_current_y:
            smallest_x_with_current_y = mouse_circled_boundary[key]['x']
            smallest_x_key_with_current_y = key
              
         if mouse_circled_boundary[key]['x'] > largest_x_with_current_y:
            largest_x_with_current_y = mouse_circled_boundary[key]['x']
            largest_x_key_with_current_y = key
                  
         # getting all xy values from smallest x to largest x that go with the current running y value
         #  for y in range(start, stop) stop value is excluded
         # but first, make sure that smallest x and largest x value are obtained from all pixel coordinates with current running y value
         if counter == len(pixel_ids_with_current_y_values):
            for x in range(smallest_x_with_current_y + 1, largest_x_with_current_y):
                       
               mouse_circled_entire_area[mouse_circled_counter] = {}
               mouse_circled_entire_area[mouse_circled_counter]['x'] = x
               mouse_circled_entire_area[mouse_circled_counter]['y'] = y
            
               # because mouse circled area is on enlarged image, we need to convert back to the original xy coordinates
               converted_back_to_original_x =   round (x / 3)
               converted_back_to_original_y =  round (y / 3)       
             
               execute_mouse_circled_shapes(converted_back_to_original_x, converted_back_to_original_y )     
               
               mouse_circled_counter += 1
              
            
   
   recreate_shapes.get_whole_image_shape(False, matched_shape_id_with_mouse_circled_area)
   
   print(matched_shape_id_with_mouse_circled_area)
   
   # saving all coordinates for the entire mouse circled area
   f = open(object_shape_filename, 'w')
   f.write(str(mouse_circled_entire_area))
   f.close()
   
   # saving all shapes id numbers that fall inside the mouse circled area
   f = open(original_image_filename, 'w')
   f.write(str(matched_shape_id_with_mouse_circled_area))
   f.close()
   
   print(" ----------------------     done!     ------------------------")


test_canvas.bind('<B1-Motion>', onLeftDrag) 
test_canvas.bind('<ButtonRelease-1>', saveObjectshape) 

switch_window_button = ttk.Button(root, text="show all shapes in circled area", command=open_second_gui)
switch_window_button.grid()



root.mainloop()

