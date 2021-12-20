from libraries import read_files_functions
from libraries import pixel_shapes_functions

filename = "rpt_ptn_test_clr_grp"

directory = ""

rpt_ptn_file = open("shapes/" + filename + "_rpt_ptn_shapes2.txt" , "w" )

nbr_filepath = "shapes/shape_nbrs/" + filename + "_shape_nbrs.txt"

all_neighbors = read_files_functions.rd_dict_k_v_list2(filename, directory, nbr_filepath)

rpt_ptn_filepath = "shapes/" + filename + "_rpt_ptn_shapes.txt"


prev_rpt_ptn_shapes = read_files_functions.rd_dict_k_v_list2(filename, directory, rpt_ptn_filepath)
# some repeating pattern shapes have same src_shape_ids. this is because they have different src_neighbors. Because they are both
# same src_shape_ids, they should be put together for this repeating pattern algorithm


prev_rpt_ptn_shapes_len = len( prev_rpt_ptn_shapes )

for o_counter in range ( 0, prev_rpt_ptn_shapes_len ):
   if o_counter >= len( prev_rpt_ptn_shapes ):
      break   
      
   deleted = 0

   for k, v in prev_rpt_ptn_shapes[o_counter].items():

      
      for i_counter in range ( 0, prev_rpt_ptn_shapes_len ):
         
         if i_counter - deleted >= len( prev_rpt_ptn_shapes ):
            break
            
         if prev_rpt_ptn_shapes[i_counter - deleted] == prev_rpt_ptn_shapes[o_counter]:
            # itself
            continue

         if k in prev_rpt_ptn_shapes[i_counter - deleted]:

            prev_rpt_ptn_shapes[i_counter - deleted][k] += prev_rpt_ptn_shapes[o_counter][k]

            prev_rpt_ptn_shapes.pop(o_counter)

            deleted += 1


print(prev_rpt_ptn_shapes)



# list of dictionaries. each dictionary contains list of neighbor_shape_id
# [ { src_shape_id: [ neighbor_shape_id, neighbor_shape_id, neighbor_shape_id ] }, { src_shape_id: [ neighbor_shape_id, neighbor_shape_id ] }, ... ]
rpt_ptn_shapes = []


# returned form. shape_id: { r, g, b }
# { '35719': {'r': 239, 'g': 53, 'b': 60}, '35731': {'r': 255, 'g': 255, 'b': 255},....}
shapes_colors = pixel_shapes_functions.get_all_shapes_colors( filename, directory )


for prev_rpt_ptn_shape in prev_rpt_ptn_shapes:
   
   print(prev_rpt_ptn_shape)
   
   prev_rpt_ptn_shape_cp = prev_rpt_ptn_shape.copy()

   for shape_id, rpt_ptn_nbr_shape_ids in prev_rpt_ptn_shape.items():
      # getting all neighbors for the current running repeating pattern
      cur_neighbors = []

      cur_rpt_ptn_colors = []
      rpt_ptn_nbr_num = len(rpt_ptn_nbr_shape_ids)
      rpt_ptn_nbr_counter = 0
      cur_nbr_found = False
      
      for neighbor in all_neighbors:
         for neighbor_key, neigbors in neighbor.items():
            if neighbor_key == shape_id:
               cur_neighbors += neigbors
               
               rpt_ptn_nbr_counter += 1
   
            else:
               for rpt_ptn_nbr in rpt_ptn_nbr_shape_ids:
                  if rpt_ptn_nbr == neighbor_key:
                     cur_neighbors += neigbors
                     rpt_ptn_nbr_counter += 1
                     
            if rpt_ptn_nbr_counter == rpt_ptn_nbr_num + 1:
               cur_nbr_found = True
               
               # now we found all neighbors for the current repeating pattern. Next is to get all colors for the current 
               # repeating pattern
               for color_shape_id in shapes_colors:
                  if color_shape_id == shape_id:
                     cur_rpt_ptn_colors.append( shapes_colors[shape_id] )
               
                  for rpt_ptn_nbr in rpt_ptn_nbr_shape_ids:
                     if rpt_ptn_nbr == color_shape_id:
                        cur_rpt_ptn_colors.append( shapes_colors[rpt_ptn_nbr] )
               

         if cur_nbr_found:
            break

      
      # now we have all neighbors for current repeating pattern shape. Next, we need to get all repeating pattern shapes
      # which are neighbors of current repeating pattern shape.
      added = False
      cur_rpt_ptn_matches = []
      for another_prev_rpt_ptn_shapes in prev_rpt_ptn_shapes:
      
         if another_prev_rpt_ptn_shapes == prev_rpt_ptn_shape:
            # itself
            continue
      
         cur_rpt_ptn_nbr = False
         cur_rpt_ptn_nbr_shape_ids = []
         skip = False
         for another_shape_id, another_rpt_ptn_nbr_shape_ids in another_prev_rpt_ptn_shapes.items():
            if another_shape_id in cur_neighbors:
               cur_rpt_ptn_nbr = True
            
            for another_rpt_ptn_nbr in another_rpt_ptn_nbr_shape_ids:
            
               # check if another_shape_id is already in the rpt_ptn_shapes
               if rpt_ptn_shapes:
                  for rpt_ptn_shape in rpt_ptn_shapes:
                     for src_id , rpt_ptn_neighbors in rpt_ptn_shape.items():
                        if another_shape_id == src_id or another_rpt_ptn_nbr in rpt_ptn_neighbors:
                           skip = True
                                                   
            
            
               if another_rpt_ptn_nbr in cur_neighbors and not skip:
                  cur_rpt_ptn_nbr = True
            
            if skip:
               continue
            
            if cur_rpt_ptn_nbr:
               cur_rpt_ptn_nbr_shape_ids.append( another_shape_id )
               cur_rpt_ptn_nbr_shape_ids += another_rpt_ptn_nbr_shape_ids
               
            # now we found current repeating pattern shape's neighbor repeatin pattern shape. Next is to check if this neighbor
            # repeating pattern shape has same color as any of the shapes in current repeating pattern shape.
            cur_rpt_ptn_nbr_colors = []
            for color_shape_id in shapes_colors:
               for cur_rpt_ptn_nbr_shape_id in cur_rpt_ptn_nbr_shape_ids:
                  if color_shape_id == cur_rpt_ptn_nbr_shape_id:
                     cur_rpt_ptn_nbr_colors.append( shapes_colors[cur_rpt_ptn_nbr_shape_id] )


            # now we have colors for current repeating pattern and another repeating pattern shape. check if another repeating pattern 
            # has same color as any of the current repeating pattern
            
            
            for cur_rpt_ptn_color in cur_rpt_ptn_colors:
               for cur_rpt_ptn_nbr_color in cur_rpt_ptn_nbr_colors:
                  if cur_rpt_ptn_color == cur_rpt_ptn_nbr_color:
                     for prev_cp_shape_id, prev_cp_nbrs in prev_rpt_ptn_shape_cp.items():
                     
                        if added:
                           # this is second time adding
                           cur_rpt_ptn_matches += cur_rpt_ptn_nbr_shape_ids
                        else:
                           for prev_cp_shape_id, prev_cp_nbrs in prev_rpt_ptn_shape_cp.items():
                       
                              cur_rpt_ptn_matches += cur_rpt_ptn_nbr_shape_ids + prev_cp_nbrs
                              
                           added = True
                        
                        break
                        
                  if added:
                     break
                     
               if added:
                  break

      if added:
         temp = {}
         
         temp[prev_cp_shape_id] = cur_rpt_ptn_matches
                     
         rpt_ptn_shapes.append(temp)      
            
rpt_ptn_file.write(str( rpt_ptn_shapes ) )
rpt_ptn_file.close()














