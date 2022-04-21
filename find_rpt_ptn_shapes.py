from libraries import read_files_functions
from libraries import pixel_shapes_functions
from libraries import pixel_functions

from collections import OrderedDict


filename = "1clrgrp"

directory = "videos/street"

# directory is passed in parameter but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'
   
rpt_ptn_file = open("shapes/" + directory + filename + "_rpt_ptn_shapes.txt" , "w" )

nbr_filepath = "shapes/" + directory + "shape_nbrs/" + filename + "_shape_nbrs.txt"

shape_nbrs = read_files_functions.rd_ldict_k_v_l(filename, directory, nbr_filepath)

# list of dictionaries. each dictionary contains list of nbr_shapeid
# [ { src_shapeid: [ nbr_shapeid, nbr_shapeid, nbr_shapeid ] }, { src_shapeid: [ nbr_shapeid, nbr_shapeid ] }, ... ]
rpt_ptn_shapes = []

# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
shapeIDs_with_all_indexes = read_files_functions.rd_shapes_file(filename, directory)

# returned form. shape_id: { r, g, b }
# { '35719': {'r': 239, 'g': 53, 'b': 60}, '35731': {'r': 255, 'g': 255, 'b': 255},....}
shapes_colors = pixel_shapes_functions.get_all_shapes_colors( filename, directory )


# if shapes are too many, it would be efficient to have some efficient search strategy.
# reversed shapes colos. this is used if shape_id is greater than half way value of the entire shapes numbers
rvs_shapes_colors = OrderedDict(reversed(list(shapes_colors.items())))

# this is needed only to get maximum shape number
shapes_colors_int = {}   
# keys in shapes_colors are strings, so convert them to integers. Integers are needed for finding maximum shape_id number.
for key in shapes_colors.keys():
   shapes_colors_int[int(key)] = shapes_colors[key]

keys = shapes_colors_int.keys()

max_shape_id_num = max(keys)
mid_shape_id_num = round( max_shape_id_num / 2 )



# this will add all finished src_shapeid
already_processed = []

# needed to be accessed by process_neighbor function too. so it needs to be global variable
cur_rpt_ptn_counter = 0


def process_neighbor ( cur_already_processed, shape_id,  nbr_shapeid , called_from_src , cur_rpt_ptn ):

   global cur_rpt_ptn_counter

   if ( nbr_shapeid in cur_already_processed and not called_from_src ) or ( nbr_shapeid in already_processed ):
      return

   # check if nbr_shapeid is already in the rpt_ptn_shapes
   if rpt_ptn_shapes:
      for rpt_ptn_shape in rpt_ptn_shapes:
         for src_id , rpt_ptn_neighbors in rpt_ptn_shape.items():
            if nbr_shapeid == src_id or nbr_shapeid in rpt_ptn_neighbors:
               return    

      
   if called_from_src:
      if cur_rpt_ptn_counter > 1:
         # another src_neighbor called it. check if there was repeating pattern shape. then start over.
            
         # cur_rpt_ptn_counter is added one for src_shapeid and src_neighbors. but not added when any nested neighbor is added. so if nested neighbor is added then
         # len(cur_rpt_ptn) will be greater than cur_rpt_ptn_counter.
         #
         # adding cur_rpt_ptn to rpt_ptn_shapes
         #
         # rpt_ptn_shapes will be like below
         # [ { src_shapeid: [ nbr_shapeid, nbr_shapeid, nbr_shapeid ] }, { src_shapeid: [ nbr_shapeid, nbr_shapeid ] }, ... ]
         if len(cur_rpt_ptn) > cur_rpt_ptn_counter:
            print(" adding " + str(cur_rpt_ptn) + " to rpt_ptn_shapes" )
            added_neighbors = []
            temp = {}

            for cur_added_shape in cur_rpt_ptn:
         
               if type(cur_added_shape) == dict:
                  cur_shape_id = cur_added_shape['src']
                  temp[ cur_shape_id ] = []
               else:
                  added_neighbors.append(cur_added_shape)
            
            temp[ cur_shape_id ] = added_neighbors
     
            rpt_ptn_shapes.append( temp )            

         cur_rpt_ptn_counter = 0
            
         cur_rpt_ptn.clear()
         # initializing cur_rpt_ptn with src_shapeid
         cur_rpt_ptn.append( { 'src': shape_id } )
         cur_rpt_ptn_counter += 1
            
         # adding src_neighbor
         cur_rpt_ptn.append(nbr_shapeid)
         cur_rpt_ptn_counter += 1    
         
      else:
         # first src_neighbor with current src_shapeid
         # adding src_neighbor to cur_rpt_ptn
         cur_rpt_ptn.append(nbr_shapeid)
         # src_neighbor added
         cur_rpt_ptn_counter += 1
      

      
   if not called_from_src:
      # called with nested neighbor. Either called by src_neighbor with nested neighbor or called by nested neighbor with deeply nested neighbor

      # looking for nested neighbor's color
      
      if int(nbr_shapeid ) <= mid_shape_id_num:
         for color_shape_id in shapes_colors:
            # finding nbr_shapeid color. every  nbr_shapeid has to find its color. so it's always true
            if nbr_shapeid == color_shape_id:
               cur_neighbor_rgb = ( shapes_colors[nbr_shapeid]['r'] , shapes_colors[nbr_shapeid]['g'] , shapes_colors[nbr_shapeid]['b'] )
      
      else:
         # nbr_shapeid is greater than middle shape id number. search with reverse ordered shapes_colors
         for color_shape_id in rvs_shapes_colors:
            # finding nbr_shapeid color. every  nbr_shapeid has to find its color. so it's always true
            if nbr_shapeid == color_shape_id:
               cur_neighbor_rgb = ( shapes_colors[nbr_shapeid]['r'] , shapes_colors[nbr_shapeid]['g'] , shapes_colors[nbr_shapeid]['b'] )         
         

         
      neighbor_same_color = False

      # neighbor's neighbor or deeply nested neighbor. check if neighbor's neighbor has color same as any of the cur_rpt_ptn color
      for cur_rpt_ptn_shape_id in cur_rpt_ptn:
         cur_rpt_ptn_shape_rgb = None
         if type(cur_rpt_ptn_shape_id) == dict:
            # src_shapeid
               
            if int( cur_rpt_ptn_shape_id['src'] ) <= mid_shape_id_num:
               # looking for cur_rpt_ptn's color
               for color_shape_id in shapes_colors:   

                  if cur_rpt_ptn_shape_id['src'] == color_shape_id:
                     cur_rpt_ptn_shape_rgb = ( shapes_colors[cur_rpt_ptn_shape_id['src']]['r'], shapes_colors[cur_rpt_ptn_shape_id['src']]['g'], \
                                              shapes_colors[cur_rpt_ptn_shape_id['src']]['b'] )
                                              
            else:
               # cur_rpt_ptn_shape_id['src'] is greater than mid_shape_id_num. use reversed ordered shapes_colors
               for color_shape_id in rvs_shapes_colors:   

                  if cur_rpt_ptn_shape_id['src'] == color_shape_id:
                     cur_rpt_ptn_shape_rgb = ( shapes_colors[cur_rpt_ptn_shape_id['src']]['r'], shapes_colors[cur_rpt_ptn_shape_id['src']]['g'], \
                                              shapes_colors[cur_rpt_ptn_shape_id['src']]['b'] )               
               
         else:
            if int( cur_rpt_ptn_shape_id ) <= mid_shape_id_num:
               for color_shape_id in shapes_colors:   
         
                  if cur_rpt_ptn_shape_id == color_shape_id:
                  
                     cur_rpt_ptn_shape_rgb = ( shapes_colors[cur_rpt_ptn_shape_id]['r'], shapes_colors[cur_rpt_ptn_shape_id]['g'], shapes_colors[cur_rpt_ptn_shape_id]['b'] )
                     
            else:
               for color_shape_id in rvs_shapes_colors:   
         
                  if cur_rpt_ptn_shape_id == color_shape_id:
                  
                     cur_rpt_ptn_shape_rgb = ( shapes_colors[cur_rpt_ptn_shape_id]['r'], shapes_colors[cur_rpt_ptn_shape_id]['g'], shapes_colors[cur_rpt_ptn_shape_id]['b'] )               
               
         if cur_rpt_ptn_shape_rgb:
            total_appearance_difference_threshold = 0
            changed, ch_v = pixel_functions.compute_appearance_difference(cur_rpt_ptn_shape_rgb, cur_neighbor_rgb)

  
            if not changed:
               # appearance did not change more than threshold value
               print("nested neighbor " + str(nbr_shapeid) + " has same color as any of the cur_rpt_ptn" )
                     
               cur_rpt_ptn.append(nbr_shapeid)
                     
               print("cur_rpt_ptn " + str(cur_rpt_ptn) )
                     
               neighbor_same_color = True
               break
                     


   cur_already_processed.append(nbr_shapeid)

   # find nested neighbors only if its from src_neighbor or same color was found
   if called_from_src or neighbor_same_color:
      # find nbr_shapeid's neighbors
      
      # first, get nbr_shapeid's neighbors
      nbr_shapeid_nbrs = []
      for shape_nbr in shape_nbrs:
         for shapeid, shapeid_nbr in shape_nbr.items():
            if shapeid == nbr_shapeid:
               nbr_shapeid_nbrs = shapeid_nbr
      
      for candidate_shapeid in shapeIDs_with_all_indexes:
         if candidate_shapeid in nbr_shapeid_nbrs:

            nested_nbr_shape_id = candidate_shapeid
                     
            process_neighbor(cur_already_processed, nbr_shapeid, nested_nbr_shape_id, False, cur_rpt_ptn )
               
       

      
   #---------------------------------------------          End of process_neighbor           --------------------------------------------------
      


for src_shapeid in shapeIDs_with_all_indexes:

   print("src_shapeid " + src_shapeid )  
   
   
   # initialization of cur_rpt_ptn_counter
   cur_rpt_ptn_counter = 0
   # current repeating pattern.
   # src_shapeid and src_nbr_shapeid will be added. this will be used when nested color has same color as any of the cur_rpt_ptn
   cur_rpt_ptn = [ { 'src': src_shapeid } ]
   # cur_rpt_ptn_counter is for counting only src_shapeid and src_neighbors. if cur_rpt_ptn_counter is more than src_shapeid + src_neighbors, then 
   # it means that nested shapes are added to cur_rpt_ptn
   cur_rpt_ptn_counter += 1
   
   
   # already processed shape for current running src_shapeid.
   # nested neibor will be added after comparing its color with any of the cur_rpt_ptn color
   cur_already_processed = []
   cur_already_processed.append(src_shapeid)

   for candidate_shapeid in shapeIDs_with_all_indexes:
      
      if src_shapeid == candidate_shapeid or candidate_shapeid in already_processed:
         # itself or already processed as src_shapeid
         continue

      # check if candidate_shapeid is already in the rpt_ptn_shapes
      skip = False
      if rpt_ptn_shapes:
         for rpt_ptn_shape in rpt_ptn_shapes:
            for src_id , rpt_ptn_neighbors in rpt_ptn_shape.items():
               if candidate_shapeid == src_id or candidate_shapeid in rpt_ptn_neighbors:
                  skip = True
                  break
            if skip:
               break
         if skip:
            continue
              
      
      src_candidate_nbr_search =  True
      for shape_nbr in shape_nbrs:
         for shapeid, shapeid_nbr in shape_nbr.items():
            if shapeid == src_shapeid:
            
               if candidate_shapeid in shapeid_nbr:
                  # candidate_shapeid now becomes src_nbr_id
                  src_nbr_id = candidate_shapeid

                  process_neighbor(cur_already_processed, src_shapeid, src_nbr_id,  True , cur_rpt_ptn )
                  
                  # src_shapeid and candidate_shapeid finished, so break out of this shape_nbrs loop
                  src_candidate_nbr_search = False
                  break
               else:
                  # src_shapeid and candidate_shapeid are not neighbor to each other
                  src_candidate_nbr_search = False
                  break
                  
         if not src_candidate_nbr_search:
            break



   # at the end of candidate_shape for src_neighbors. check if there was repeating pattern shape
   #
   # cur_rpt_ptn_counter is added one for src_shapeid and src_neighbors. but not added when any nested neighbor is added. so if nested neighbor is added then
   # len(cur_rpt_ptn) will be greater than cur_rpt_ptn_counter.
   #
   # adding cur_rpt_ptn to rpt_ptn_shapes
   #
   # rpt_ptn_shapes will be like below
   # [ { src_shapeid: [ nbr_shapeid, nbr_shapeid, nbr_shapeid ] }, { src_shapeid: [ nbr_shapeid, nbr_shapeid ] }, ... ]
   if len(cur_rpt_ptn) > cur_rpt_ptn_counter:
      print(" adding " + str(cur_rpt_ptn) + " to rpt_ptn_shapes" )
      added_neighbors = []
      temp = {}
      for cur_added_shape in cur_rpt_ptn:
         
         
         if type(cur_added_shape) == dict:
            cur_shape_id = cur_added_shape['src']
            temp[ cur_shape_id ] = []
         else:
            added_neighbors.append(cur_added_shape)
            
      temp[ cur_shape_id ] = added_neighbors
   
      rpt_ptn_shapes.append( temp )    

       

   already_processed.append(src_shapeid)
        

            
rpt_ptn_file.write(str( rpt_ptn_shapes ) )
rpt_ptn_file.close()





