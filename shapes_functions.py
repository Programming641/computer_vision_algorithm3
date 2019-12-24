
from PIL import Image
import os
import recreate_shapes
from statistics import mean
import pixel_functions
import read_files_functions



def find_direct_shape_neighbors(image_filename, directory_under_images):

    # directory is passed in parameter but does not contain /
    if directory_under_images != "" and directory_under_images.find('/') == -1:
       directory_under_images +='/'

    if os.path.exists("shapes") == False:
       os.mkdir("shapes")


    shapes_neighbors_filename = "shapes/" + image_filename + " shapes_neighbors.txt"

    if os.path.exists(shapes_neighbors_filename):
       neighbor_shapes = read_files_functions.read_dict_key_value_list(image_filename, directory_under_images, shapes_neighbors_filename)
       return neighbor_shapes

    image_original = 'images/' + directory_under_images + image_filename + '.png'

    read_original_image = Image.open(image_original)

    original_width, original_height = read_original_image.size

    # for storing shape's neighbor shapes
    # { shape id: [ neighboor shape id1 , neighbor shape id2, ..... ] }
    shape_neighbors = {}

    whole_image_shapes = recreate_shapes.get_whole_image_shape(True, image_filename, directory_under_images)  

    for pixel_shape_id , pixel_xy_values in whole_image_shapes.items():  
       # outer loop is for current running shape which looks for direct shape neighbors
       
       print(pixel_shape_id)
       # every shape has its neighbors
       shape_neighbors[pixel_shape_id] = []
       
       boundary_pixels = pixel_functions.get_boundary_pixels(pixel_xy_values)
       
       boundary_direct_neigbors = pixel_functions.get_direct_neighbors(boundary_pixels)
       
       # for storing boundary pixels' neighbor pixel indexes. if candidate neighbor shape contains any of the 
       # index numbers in it, then this candidate is neighbor shape
       pixel_indexes = []
       
       for shape_id, xy_values in boundary_direct_neigbors.items():
       
          pixel_index = xy_values['y'] * original_width + xy_values['x']
          pixel_indexes.append(pixel_index)
          
       for neighbor_shape_id , neighbor_pixel_xy_values in whole_image_shapes.items():         
          # inner loop is for finding neighbors for current running shape
          
          neighbor_pixel_indexes = []
          
          for key in neighbor_pixel_xy_values:
       
             neighbor_pixel_index = neighbor_pixel_xy_values[key]['y'] * original_width + neighbor_pixel_xy_values[key]['x']
             neighbor_pixel_indexes.append(neighbor_pixel_index)
          
             
          if not pixel_shape_id == neighbor_shape_id:  
             for pixel_index in pixel_indexes:
                if pixel_index in neighbor_pixel_indexes:

                   shape_neighbors[pixel_shape_id].append(neighbor_shape_id)
                   break    
             
        
       if len(shape_neighbors[pixel_shape_id]) == 0:
          shape_neighbors.pop(pixel_shape_id)


    f = open(shapes_neighbors_filename, 'w')
    f.write(str(shape_neighbors))
    f.close()





    return shape_neighbors




def get_shapes_colors(filename, directory):

    # directory is specified but does not contain /
    if directory != "" and directory.find('/') == -1:
       directory +='/'

    shapes_color_filename = "shapes/" + filename + " shapes_colors.txt"

    image_original = 'images/' + directory + filename + '.png'

    read_original_image = Image.open(image_original)

    image_width, image_height = read_original_image.size

    image_pixels = read_original_image.getdata()

    shapes_colors = {}

    whole_image_shapes = recreate_shapes.get_whole_image_shape(True, filename, directory)

    for shape_id , pixel_xy_values in whole_image_shapes.items():
    
       shapes_colors[shape_id] = {}
    
       # for storing RGB values for each shape. Initializing for each shape
       Red = []
       Green = []
       Blue = []
    
       for pixel_id in pixel_xy_values:

          image_index = pixel_xy_values[pixel_id]['y'] * image_width + pixel_xy_values[pixel_id]['x']

          r, g, b, a = image_pixels[ image_index ]
          Red.append(r)
          Green.append(g)
          Blue.append(b)


       r = round(mean(Red))
       g = round(mean(Green))
       b = round(mean(Blue))
       
       shapes_colors[shape_id] = { 'r': r, 'g': g, 'b': b }


    f = open(shapes_color_filename, 'w')
    f.write(str(shapes_colors))
    f.close()

    return shapes_colors











































































































