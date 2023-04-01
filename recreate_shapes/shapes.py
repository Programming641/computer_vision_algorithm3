import re
import math
import os, sys
import shutil
import pickle

from PIL import Image

from libraries.cv_globals import proj_dir, top_shapes_dir
from libraries import image_functions

shapes_dir = proj_dir + "/shapes/"
images_dir = proj_dir + "/images/"


filename = "13"
directory = "videos/street3/resized/min"

# choices are "shapes", "brightness", 
recreate_what = "shapes"

# choices are
# normal, intnl_spixcShp
shapes_type = "intnl_spixcShp"

backgnd_color = ( 0, 0, 255 )


'''
this module serves 2 purposes. One is to recreate the each shape of the image. Another purpose is to return xy coordinate values of the each 
shape to the caller. If parameter is true then, it is a request to return xy coordinates of all image shapes

2nd parameter, shapeids_in_need is a list that contains all shape id numbers
'''
def get_whole_image_shape(parameter, recreate_what, filename,  directory="", shapeids_in_need=None):
    # directory is specified but does not contain /
    if directory != "" and directory[-1] != '/':
       directory +='/'
    
    shapes_fdir = directory + "shapes/"
    
    # by default shapes_filename is "_shapes.txt"
    shapes_filename = filename + "_shapes.txt"
    
    foldername = ""
    if recreate_what == "shapes":
       foldername =  shapes_dir + shapes_fdir + shapes_filename[:-4] 
          
    elif shapeids_in_need:
       foldername = shapes_dir + directory + "circleda/" + filename
   
    elif recreate_what == "brightness":
       shapes_filename = filename + "_britshapes.txt"
       foldername = shapes_dir + directory + "brit/" + filename

    # delete and create folder
    if foldername and os.path.exists(foldername) == True:
       shutil.rmtree(foldername)
   
    if foldername and os.path.exists(foldername) == False:
       os.makedirs(foldername)     

    if foldername != "" and foldername[-1] != '/':
       foldername +='/'

    original_image = Image.open(images_dir + directory + filename + ".png")

    image_width, image_height = original_image.size

    original_image_data = original_image.getdata()



    shapes_file = open(shapes_dir + shapes_fdir + shapes_filename)
    shapes_file_contents = shapes_file.read()


    # not taking single pixel shapes
    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
    space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
    single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'

    single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                           str(len(str(image_width * image_height))) + '}\]\)'
                           
    match = re.findall(single_pixel_pattern, shapes_file_contents)

    '''


    '''
    ( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
    GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
    then comes ] then comes )

    GROUPSTART (      GROUPEND )
    '''
    multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                             '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
    match = re.findall(multiple_pixel_pattern, shapes_file_contents)

    shapes = {}

    shape_progress_counter = 0
    # match contains all shapes
    for shape in match:

       if parameter == False:
          new_image = Image.new('RGB', (image_width, image_height), ( backgnd_color ) )

       shapes_id_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '},'
       match_temp = re.search(shapes_id_pattern, shape)
       shapes_id = match_temp.group().strip('(,')
 
       # it is a request to create shapes that fell inside the mouse circled area but the current running shape is not 
       # inside the mouse circled area
       if shapeids_in_need != None and not str(shapes_id) in shapeids_in_need:
          continue
          


 
       pixels_list_pattern = '\[.*\]'
       pixels_index_string = re.findall(pixels_list_pattern, shape)




       shape_pixel_counter = 0 
       shapes[shapes_id] = {}



       #pixels_index_string contains one shape
       # pixels_index_string is a list but contains only one string
       for one_string in pixels_index_string:
      
          # one_string is a one string. removing unnecessary characters leaving only the numbers
          one_string_stripped = one_string.strip('[, ]')
          # split each number by ,
          one_string_list = one_string_stripped.split(',')

          # now iterate over all pixel index numbers
          for pixel_index in one_string_list:
             shape_pixel_counter += 1
             pixel_index = int(pixel_index)
         
             if len(original_image_data[pixel_index ]) == 3:
                original_image_red, original_image_green, original_image_blue = original_image_data[pixel_index ]
             else:
                original_image_red, original_image_green, original_image_blue, alpha = original_image_data[pixel_index ]
             y = math.floor(pixel_index / image_width)
             x  = pixel_index % image_width          
             
             if parameter == True:

                shapes[shapes_id][shape_pixel_counter] = {}
                shapes[shapes_id][shape_pixel_counter]['x'] = x
                shapes[shapes_id][shape_pixel_counter]['y'] = y

             if parameter == False:
                new_image.putpixel( (x, y) , (original_image_red, original_image_green, original_image_blue) )


          if parameter == False:
             shape_progress_counter += 1          
             print("shape " + str(shape_progress_counter))  
             
             # saving one shape
             new_image.save(foldername + shapes_id + '.png')
      
    shapes_file.close() 
    
    if parameter == True:
       return shapes 




if __name__ == '__main__':

   
   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   if shapes_type == "normal":
      get_whole_image_shape(False, recreate_what, filename, directory )
      
   elif shapes_type == "intnl_spixcShp":
      # read shapes file
      shapes_dir = top_shapes_dir + directory + "shapes/intnl_spixcShp/"
      shapes_intnl_s_pixcShp_dfile = shapes_dir + "data/" + filename + "shapes.data"
      
      shapes_imdir = shapes_dir + filename + "/"
      Lshapes_imdir = shapes_dir + "/Lshapes/" + filename + "/"
      
      # delete and create folder
      if shapes_imdir and os.path.exists(shapes_imdir) == True:
          shutil.rmtree(shapes_imdir)
      os.makedirs(shapes_imdir )
      
      if Lshapes_imdir and os.path.exists(Lshapes_imdir) == True:
         shutil.rmtree(Lshapes_imdir)
      os.makedirs(Lshapes_imdir )         

      with open (shapes_intnl_s_pixcShp_dfile, 'rb') as fp:
         # { 'shapeid': [ pixel indexes ], ... }
         im_shapes_w_intl_spixcShp = pickle.load(fp)
      fp.close()      
      
   
      for shapeid in im_shapes_w_intl_spixcShp:
         shapes = [ shapeid ]
         save_filepath = shapes_imdir + shapeid + ".png"
         image_functions.cr_im_from_shapeslist2( filename, directory, shapes, save_filepath=save_filepath , shapes_rgb=( 0, 0, 255 ) )

         if len( im_shapes_w_intl_spixcShp[shapeid] ) >= 50:
            save_filepath = Lshapes_imdir + shapeid + ".png"
            image_functions.cr_im_from_shapeslist2( filename, directory, shapes, save_filepath=save_filepath , shapes_rgb=( 0, 0, 255 ) )         

   else:
      print("ERROR at recreate_shapes.py shapes_type " + shapes_type + " is not supported")
      sys.exit()











