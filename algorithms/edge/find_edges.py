# not just take edges between pixels but keep which shape's pixel has edge.
from libraries import pixel_functions, read_files_functions

from PIL import Image
import math
import os, sys
import pickle

from libraries.cv_globals import proj_dir, top_shapes_dir, top_images_dir



image_filename = '10'
edge_directory = "videos/street3/resized"
directory = "videos/street3/resized/min"
shapes_type = "intnl_spixcShp"


if len(sys.argv) > 1:
   image_filename = sys.argv[0][0: len( sys.argv[0] ) - 4 ]
   directory = sys.argv[1]

   print("execute script find_edges.py. filename " + image_filename + " directory " + directory )

if directory != "" and directory[-1] != '/':
   directory +='/'
if edge_directory != "" and edge_directory[-1] != '/':
   edge_directory +='/'


edge_dir = top_shapes_dir + edge_directory + "edges/" + shapes_type + "/"
edge_data_dir = edge_dir + "data/"

if os.path.exists(edge_dir ) == False:
   os.makedirs(edge_dir )
if os.path.exists(edge_data_dir ) == False:
   os.makedirs(edge_data_dir )


original_image = Image.open(top_images_dir + edge_directory + image_filename + ".png")
original_pixel = original_image.getdata()
image_size = original_image.size



if shapes_type == "normal":

   # return value form is
   # shapes[shapes_id][pixel_index] = {}
   # shapes[shapes_id][pixel_index]['x'] = x
   # shapes[shapes_id][pixel_index]['y'] = y
   im_shapes = read_files_functions.rd_shapes_file(image_filename, directory)

   im_shapes_neighbors_path = top_shapes_dir + directory + "shape_nbrs/" + image_filename + "_shape_nbrs.txt"

elif shapes_type == "intnl_spixcShp":
   s_pixcShp_intnl_dir = top_shapes_dir + directory + "spixc_shapes/internal/"

   shapes_dfile = s_pixcShp_intnl_dir + "shapes/" + image_filename + "shapes.data"
   with open (shapes_dfile, 'rb') as fp:
      # { '79999': ['79999', ... ], ... }
      # { 'shapeid': [ pixel indexes ], ... }
      im_shapes = pickle.load(fp)
   fp.close()


   # converting pixel form for im_shapes
   for shapeid in im_shapes:
      cur_shape_pixels = { }
      for pindex in im_shapes[shapeid]:
         cur_shape_pixels[pindex] = {}
            
         y = math.floor( int(pindex) / image_size[0])
         x  = int(pindex) % image_size[0] 
      
         cur_shape_pixels[pindex]['x'] = x
         cur_shape_pixels[pindex]['y'] = y

      # shapes[shapes_id][pixel_index]['x'] = x
      # shapes[shapes_id][pixel_index]['y'] = y
      im_shapes[shapeid] = cur_shape_pixels

   im_shapes_neighbors_path = s_pixcShp_intnl_dir + "shape_nbrs/" + image_filename + "_shape_nbrs.txt"


# [ {"shapeid": ["nbr_shapeid", "nbr_shapeid", ...] }, ...  ]
im_shape_nbrs = read_files_functions.rd_ldict_k_v_l(image_filename, directory, im_shapes_neighbors_path)







edge_image = Image.open(top_images_dir + edge_directory + image_filename + ".png")

# [ [ shapeid1, shapeid2, shapeid1's edge pixel, shapeid2's edge pixel ], ... ]
edges = []
for im_shapeid, pixels in im_shapes.items():
   # get current shape's neighbor shapes.
   cur_shape_nbrs = [ shape_nbrs.values() for shape_nbrs in im_shape_nbrs if im_shapeid in shape_nbrs.keys() ][0]
   cur_shape_nbrs = [*cur_shape_nbrs][0]

   cur_already_processed_pix = []
   cur_already_processed_nbr_pix = []
   
   
   for pindex, xy in pixels.items():
      # returned form => [25, 26, 426, 826, 825, 824, 424, 24]
      cur_pixel_neighbors = pixel_functions.get_nbr_pixels(pindex, image_size)   
      
      for cur_pixel_neighbor in cur_pixel_neighbors:
         if cur_pixel_neighbor in cur_already_processed_pix or ( pindex in cur_already_processed_nbr_pix and cur_pixel_neighbor in cur_already_processed_pix ):
            continue
         
         neighbor_x = cur_pixel_neighbor % image_size[0]
         neighbor_y = math.floor( cur_pixel_neighbor / image_size[0])

         clrch, brit_thres, brit_ch_v = pixel_functions.compute_appearance_difference(original_pixel[int( pindex )] ,
                                                 original_pixel[cur_pixel_neighbor], 70, clr_thres=70 )
                                                   
         if clrch or ( not brit_thres ) :
            # color changed is true or brightness is over threshold
            # cur_pixel_neighbor is edge to current pixel
            cur_edge_index = len( edges )
            edges.append( [] ) 
            
            # first, add im_shapeid
            edges[cur_edge_index].insert(0, im_shapeid )

            cur_pixel_nbr_found = False
            # check which shape cur_pixel_neighbor belongs
            neighbor_shapeid = None
            for cur_shape_nbr in cur_shape_nbrs:
               if str( cur_pixel_neighbor ) in im_shapes[ im_shapeid ].keys():
                  cur_pixel_nbr_found = True
                  # current neighbor pixel belong to the im1_shapeid
                  edges[cur_edge_index].insert(1, im_shapeid )
                  edges[cur_edge_index].insert(2, pindex )
                  edges[cur_edge_index].insert(3, str( cur_pixel_neighbor ) )
                  
                  edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) )
                  break
               elif str( cur_pixel_neighbor ) in im_shapes[ cur_shape_nbr ].keys():
                  neighbor_shapeid = cur_shape_nbr
                  cur_pixel_nbr_found = True
                  edges[cur_edge_index].insert(1, cur_shape_nbr )
                  edges[cur_edge_index].insert(2, pindex )
                  edges[cur_edge_index].insert(3, str( cur_pixel_neighbor ) )
                  
                  edge_image.putpixel( ( neighbor_x, neighbor_y ) , (0, 0, 255) ) 
                  break
 
            
            if cur_pixel_nbr_found is False:
               print("ERROR. current neighbor pixel has to be found in main shape's neighbor shape's pixels")
               sys.exit()

            verified = False
            # at last, verify the current edge
            if len( edges[ cur_edge_index ] ) == 4 and ( edges[cur_edge_index][0] == im_shapeid and edges[cur_edge_index][1] == im_shapeid and
               edges[cur_edge_index][2] == pindex and edges[cur_edge_index][3] == str(cur_pixel_neighbor) ):
               # current neighbor pixel belongs to im_shapeid. verification is OK
               verified = True
            elif len( edges[ cur_edge_index ] ) == 4 and ( edges[cur_edge_index][0] == im_shapeid and edges[cur_edge_index][1] == neighbor_shapeid and
               edges[cur_edge_index][2] == pindex and edges[cur_edge_index][3] == str(cur_pixel_neighbor) ):
               verified = True
            
            if verified is False:
               print("edge verification failed")
               sys.exit()
            
            # lastly, check if current edge already exist in reverse order. order1 -> shapeid1'edge, shapeid2' edge.
            # reverse order -> shapeid2's edge, shapeid1's edge
            reverse_current_edge = [ edges[cur_edge_index][3], edges[cur_edge_index][2] ]
            
            reverse_cur_edge_exist = [ edge for edge in edges if reverse_current_edge == [ edge[2], edge[3] ] ]
            if len( reverse_cur_edge_exist ) == 1:   
               edges.pop( cur_edge_index )
            elif len( reverse_cur_edge_exist ) > 1:
               print("ERROR reverse_cur_edge_exist should not be greater than 1")
               sys.exit()
            
            
            

         cur_already_processed_nbr_pix.append( cur_pixel_neighbor )

      cur_already_processed_pix.append( pindex )

   

edge_image.save(edge_dir + image_filename + ".png" )

with open(edge_data_dir + image_filename + ".data", 'wb') as fp:
   pickle.dump(edges, fp)
fp.close()






















