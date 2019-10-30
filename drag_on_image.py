import tkinter
from PIL import Image, ImageTk
import recreate_shapes

matched_shape_id_with_mouse_circled_area = []

def execute_mouse_circled_shapes( mouse_circled_x, mouse_circled_y ):

   



   # we are getting xy coordinates of whole image shapes. We will then get all shapes that fall inside the 
   # mouse circled image area 
   whole_image_shapes = recreate_shapes.get_whole_image_shape(True)   

   for shape_id , pixel_xy_values in whole_image_shapes.items():

      for pixel_id in pixel_xy_values:
      
         if pixel_xy_values[pixel_id]['x'] == mouse_circled_x and pixel_xy_values[pixel_id]['y'] == mouse_circled_y:
            # pixel falls in the mouse circled area
            print(" shape found!" )          
            matched_shape_id_with_mouse_circled_area.append(shape_id)
            


   








enlarged_image = 'images/easy image to analyze for practice x3 enlarged.png'
image_original = 'images/easy image to analyze for practice.png'



# object shape's filename exclude images folder name and replacing extension with txt
object_shape_filename = "shapes/objectshape/" + enlarged_image[7:-4] + ".txt"

read_enlarged_image = Image.open(enlarged_image)
read_original_image = Image.open(image_original)
enlarged_width, enlarged_height = read_enlarged_image.size

original_width, original_height = read_original_image.size









root = tkinter.Tk()



# canvas作成
test_canvas = tkinter.Canvas(root, width=read_enlarged_image.width + 200, height=read_enlarged_image.height +200)
test_canvas.grid(row=0, column=0)

image_origin_posX = 10
image_origin_posY = 10



# canvasに画像を表示
im = ImageTk.PhotoImage(image=read_enlarged_image)
test_canvas.create_image(image_origin_posX, image_origin_posY, anchor='nw', image=im)

# for storing each object shape's x, y coordinate
object_shape = {}
object_shape_counter = 0

def onLeftDrag(event):

    global object_shape_counter
    global object_shape
    object_shape_counter += 1

    image_starting_posX = event.x  - image_origin_posX
    image_starting_posY = event.y - image_origin_posY
    print ('Widget=%s X=%s Y=%s' % (event.widget, image_starting_posX, image_starting_posY))
    
    object_shape[object_shape_counter] = {}
    object_shape[object_shape_counter]['x'] = image_starting_posX
    object_shape[object_shape_counter]['y'] = image_starting_posY
    
     
def saveObjectshape(event):

   global object_shape

   smallest_y = min(int(d['y']) for d in object_shape.values())
   largest_y = max(int(d['y']) for d in object_shape.values())

   first = True
   object_shape_counter = 1
   
   # iterating all coordinate xy value pairs from smallest_y + 1 to largest_y + 1
   for y in range(smallest_y + 1, largest_y - 1 ):
      # smallest_y + 1 because smallest_y is the very top boundary.  largest_y - 1 because largest_y is the very bottom boundary
       
      # current_y_keys contains all xy coordinate pairs that have the current running y value.
      current_y_keys = [k for k in object_shape  if (int(object_shape[k]['y'])) == y]
       
      # key is the coordinate pair id.
      # looking for smallest and largest x values that go with the current running y value
      for key in current_y_keys:

         if first != False:
            smallest_x_with_current_y = object_shape[key]['x']
            largest_x_with_current_y = object_shape[key]['x']
            first = False
           
         elif object_shape[key]['x'] < smallest_x_with_current_y:
            smallest_x_with_current_y = object_shape[key]['x']
            smallest_x_key_with_current_y = key
              
         elif object_shape[key]['x'] > largest_x_with_current_y:
            largest_x_with_current_y = object_shape[key]['x']
            largest_x_key_with_current_y = key
                  
         # getting all xy values from smallest x to largest x that go with the current running y value
         for x in range(smallest_x_with_current_y + 1, largest_x_with_current_y - 1 ):
                       
            object_shape[object_shape_counter] = {}
            object_shape[object_shape_counter]['x'] = x
            object_shape[object_shape_counter]['y'] = y
            
            converted_back_to_original_x =   round (x / 3)
            converted_back_to_original_y =  round (y / 3)
            
            
            execute_mouse_circled_shapes(converted_back_to_original_x, converted_back_to_original_y )
            

             
             
            
            object_shape_counter += 1
              
            
          
   recreate_shapes.get_whole_image_shape(False, matched_shape_id_with_mouse_circled_area)
   
   print(matched_shape_id_with_mouse_circled_area)
   f = open(object_shape_filename, 'w')
   f.write(str(object_shape))
   f.close()
   
   print(" ----------------------     done!     ------------------------")


test_canvas.bind('<B1-Motion>', onLeftDrag) 
test_canvas.bind('<ButtonRelease-1>', saveObjectshape) 


root.mainloop()





