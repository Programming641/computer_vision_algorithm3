import tkinter
from PIL import Image, ImageTk

root = tkinter.Tk()


image_filename = 'images/bird01 x3 enlarged.png'

# object shape's filename exclude images folder name and replacing extension with txt
object_shape_filename = "objectshape/" + image_filename[7:-4] + ".txt"

read_image = Image.open(image_filename)

# canvas作成
test_canvas = tkinter.Canvas(root, width=read_image.width + 200, height=read_image.height +200)
test_canvas.grid(row=0, column=0)

image_origin_posX = 10
image_origin_posY = 10



# canvasに画像を表示
im = ImageTk.PhotoImage(image=read_image)
test_canvas.create_image(image_origin_posX, image_origin_posY, anchor='nw', image=im)

# for storing each object shape's x, y coordinate
object_shape = {}
object_shape_counter = 0

def onLeftDrag(event):
    print ('Got left mouse button drag:')
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
   for i in range(smallest_y + 1, largest_y - 1 ):
      # smallest_y + 1 because smallest_y is the very top boundary.  largest_y - 1 because largest_y is the very bottom boundary
       
      # current_y_keys contains all xy coordinate pairs that have the current running y value.
      current_y_keys = [k for k in object_shape  if (int(object_shape[k]['y'])) == i]
       
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
                  
         # getting all x values from smallest x to largest x that go with the current running y value
         for x in range(smallest_x_with_current_y + 1, largest_x_with_current_y - 1 ):
                       
            object_shape[object_shape_counter] = {}
            object_shape[object_shape_counter]['x'] = x
            object_shape[object_shape_counter]['y'] = i
             
            object_shape_counter += 1
              
            
          

   f = open(object_shape_filename, 'w')
   f.write(str(object_shape))
   f.close()
   
   print(" done!")


test_canvas.bind('<B1-Motion>', onLeftDrag) 
test_canvas.bind('<ButtonRelease-1>', saveObjectshape) 


root.mainloop()





