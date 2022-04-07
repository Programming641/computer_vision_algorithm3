import tkinter
from PIL import ImageTk, Image
from libraries import read_files_functions, pixel_shapes_functions, same_shapes_btwn_frames
import sys


# method: get relative positions of contact areas
# input parameter
# contact areas and shape_boundary_p have the form below
# { counter number: { "x": x, "y", y }, counter number: { "x": x, "y", y } ....  }
# returns
# [ { pixel index : [  { "x": x, "y", y } ] } ]
def get_rel_pos_contact_areas( contact_areas, shape_boundary_p, imfile, directory ):
   
   non_contact_areas = []
   
   # removing contact area pixels from shape_boundary_p
   for shape_p in shape_boundary_p.values():
      if not shape_p in contact_areas.values():
         non_contact_areas.append( shape_p )
      


   # directory is specified but does not contain /
   if directory != "" and directory[-1] != ('/'):
      directory +='/'

   img = Image.open("images/" + str(directory) + imfile + ".png")

   imwidth = img.size[0]

   rel_pos = []
   already_added_pindex = []

   for cnta_pix in contact_areas.values():
      if cnta_pix in already_added_pindex:
         continue
      
      # count how many current pixel is in contact_areas
      pindex_count = list( contact_areas.values() ).count( cnta_pix )

      pindex = cnta_pix["y"] * imwidth + cnta_pix["x"] 

      rel_pos.append( { pindex: [ ], "count": str(pindex_count) } )
      
      
   
      pix_index = rel_pos.index( { pindex: [ ], "count": str(pindex_count) } )
   
   
      for non_ca_p in non_contact_areas:
      
         relative_pos = { "x": non_ca_p["x"] - cnta_pix["x"] , "y": non_ca_p["y"] - cnta_pix["y"] }
      
         rel_pos[pix_index][pindex].append( relative_pos )
      
      
      already_added_pindex.append( cnta_pix )


   return rel_pos






im1file = "2clrgrp"
im2file = "3clrgrp"

filenames = [ im1file, im2file ]

directory = "videos/hanger"

# directory is specified but does not contain /
if directory != "" and directory[-1] != ('/'):
   directory +='/'

img1 = Image.open("images/" + str(directory) + im1file + ".png")

im1width, im1height = img1.size



t_shape = "38759"


im1s_nbrs = read_files_functions.rd_ldict_k_v_l( im1file, directory )
im2s_nbrs = read_files_functions.rd_ldict_k_v_l( im2file, directory )

im1s_clrs = pixel_shapes_functions.get_all_shapes_colors( im1file, directory )
im2s_clrs = pixel_shapes_functions.get_all_shapes_colors( im2file, directory )


# image1 shape neighbors list
im1s_nbrs_l = []

im1s_nbrs_l.append(t_shape)

# getting neighbor shapes for the target shape "t_shape"
for im1s_nbr in im1s_nbrs:
   if t_shape in im1s_nbr:
      for im1nbr in im1s_nbr[t_shape]:
         im1s_nbrs_l.append(im1nbr)


# pixel index number for the above image1 shape neighbors list
im1nbr_pix = pixel_shapes_functions.get_all_pixels_of_shapes( im1s_nbrs_l, im1file, directory )

im1nbr_shapeids = []



# this is for getting all pixel index numbers without shapeids. this is for passing pixel index numbers to "get_shapeids_frompixels" so to get shapeids
# from image2
temp_pixels = []
for congl_shapeid, congl_pixel in im1nbr_pix.items():
   temp_pixels += congl_pixel
   im1nbr_shapeids.append( congl_shapeid )

# getting all shapes from image2 that are located in the same position as the above conglomerated neighbors shape
im2shapes = pixel_shapes_functions.get_shapeids_frompixels( temp_pixels, im2file, directory)


im2shapeids = []


for im2shape in im2shapes.keys():
   im2shapeids.append( im2shape )


# checking if im1 shape color is found in im2 shapes

same_clr_shapes = []


for im1shapeid, im1s_clr in im1s_clrs.items():
   if im1shapeid in im1nbr_shapeids:
      
      for im2shapeid, im2s_clr in im2s_clrs.items():
         if im2shapeid in im2shapeids:
            # im1 and im2 shape are found. now compare their colors
            if im1s_clr == im2s_clr:
               same_clr_shapes.append( [ im1shapeid, im2shapeid ] )



print(same_clr_shapes)


# returned value has below form
# shapes[shapes_id][pixel_index] = {}
# shapes[shapes_id][pixel_index]['x'] = x
# shapes[shapes_id][pixel_index]['y'] = y
im1s_pixels = read_files_functions.rd_shapes_file(im1file, directory)
im2s_pixels = read_files_functions.rd_shapes_file(im2file, directory)


'''
all_shape_match_results = []

# this is used for displaying closest matched images
root = tkinter.Tk()


for im1shapeid in im1s_pixels:

   match_results = {}
   match_results[ im1shapeid ] = []

   cur_im1shapeid = False

   # boundary_pixels has the following form
   # {1: {'x': 0, 'y': 234}, 2: {'x': 61, 'y': 221}, {'x': 177, 'y': 319}, 16679: {'x': 178, 'y': 229}}
   # containing coordinates of boundary pixels
   im1bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im1s_pixels[im1shapeid] )

   

   for im2shapeid in im2s_pixels:
   
      shape_ids = [ int(im1shapeid ), int (im2shapeid ) ]
      
      proceed = False
      for same_clr_shape in same_clr_shapes:
         if same_clr_shape[0] == im1shapeid and same_clr_shape[1] == im2shapeid :
            proceed = True
            
      if not proceed:
         continue


      im2bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im2s_pixels[im2shapeid] )
   
      # match shapes based on relative positions of boundary pixels
      bnd_rel_result = same_shapes_btwn_frames.boundary_rel_pos(im1bnd_pixels, im2bnd_pixels, shape_ids)
      
      bnd_result = 0
      bnd_result = same_shapes_btwn_frames.process_boundaries(im1bnd_pixels, im2bnd_pixels, shape_ids, filenames)
      result = 0
      result = same_shapes_btwn_frames.find_shapes_in_diff_frames(im1s_pixels[im1shapeid], im2s_pixels[im2shapeid],  "consecutive_count", shape_ids)
      print("real pixels result " + str(result) )
      print("bnd_result " + str(bnd_result) )

      if result or bnd_result:
               
         temp = {}
         match_result = 0
         if bnd_result:
            match_result += round( bnd_result )
         if result:
            match_result += round( result )
         if bnd_rel_result:
            match_result += round( bnd_rel_result * 1.6 )


         temp['im2shapeid'] = im2shapeid
         temp['value'] = match_result
         match_results[im1shapeid ].append(temp)
            
         if not cur_im1shapeid:
            # match_results will be added to the all_shape_match_results. match_results added here is a reference and not a value. so if you update match_results, the changes will be 
            # reflected in match_results inside all_shape_match_results as well. What this means is that you only need to add match_results once. Not each time temp is added to the match_results
            all_shape_match_results.append(match_results)
            cur_im1shapeid = True
    
   match_results[im1shapeid ] = sorted(match_results[ im1shapeid ], key=lambda k: k['value'])

   if not match_results[ im1shapeid ]:
      continue
      
   closest_match = {}
   prev_im2shapeid = None
   for matches in match_results[str( shape_ids[0] )]:
         
      # closest_match initialization
      if not closest_match:
         closest_match[matches['im2shapeid']] = matches['value']
         prev_im2shapeid = matches['im2shapeid']

      elif closest_match[prev_im2shapeid] < matches['value']:
         closest_match.pop(prev_im2shapeid)
         prev_im2shapeid = matches['im2shapeid']
         closest_match[prev_im2shapeid] = matches['value']
               
   print(" im1 shape " + str(shape_ids[0]) + " closest match shape is " + str( prev_im2shapeid ) )
 
   # displaying closest match images/
   
   window = tkinter.Toplevel(root)
   window.title( str(shape_ids[0]) + " " + str( prev_im2shapeid ) )
    
   if prev_im2shapeid != None:
      if len(im1s_pixels[im1shapeid]) > 1 and len(im2s_pixels[prev_im2shapeid]) > 1:
         

         im1shape_file = "shapes/" + directory + str(im1file) + "_shapes/" + str(im1shapeid) + ".png"
         im2shape_file = "shapes/" + directory + str(im2file) + "_shapes/" + str(prev_im2shapeid) + ".png"
   
         img = ImageTk.PhotoImage(Image.open(im1shape_file))
         img2 = ImageTk.PhotoImage(Image.open(im2shape_file))
  
         label1 = tkinter.Label(window, image = img, bg="white")
         label1.image = img
         label1.pack()
   
         label2 = tkinter.Label(window, image = img2, bg="white" )
         label2.image = img2
         label2.pack()
      
      

root.mainloop()



# closest match im1shapeid and im2shapeid
# [ im1shapeid, im2shapeid, value of how much difference is there between largest and second largest ]
closest_match_shapes = []

# get closest match shape
for all_shape_match_result in all_shape_match_results:
   total = 0
   # largest value
   largest_v = None
   closest_im2shapeid = None
   for im1shapeid, im2shapes_l in all_shape_match_result.items():
      
      im2shapes_l = sorted(im2shapes_l, key=lambda d: d['value']) 
      if len(im2shapes_l) == 1:
         closest_match_shapes.append( [ im1shapeid, im2shapes_l[-1]["im2shapeid"], im2shapes_l[-1]["value"] ] )
         continue
      
      # check if largest value is 2 times more than the second largest value
      if im2shapes_l[-1]["value"] > im2shapes_l[-2]["value"] * 2:
         closest_match_shapes.append( [ im1shapeid, im2shapes_l[-1]["im2shapeid"], im2shapes_l[-1]["value"] / ( im2shapes_l[-1]["value"] + im2shapes_l[-2]["value"] ) ] )


print(closest_match_shapes)
'''

closest_match_shapes = [['34440', '34443', 0.8128571428571428], ['35573', '35574', 0.6770255271920089], ['36068', '34622', 0.8484848484848485], ['36116', '36119', 0.7171717171717171], ['36595', '33385', 0.6842105263157895], ['36901', '37260', 0.7458410351201479], ['37463', '33385', 0.7058823529411765], ['37864', '38212', 0.6684491978609626], ['38342', '37260', 0.7471264367816092], ['38759', '38761', 0.6791840519239685], ['38964', '33385', 0.7058823529411765], ['38971', '33385', 0.6842105263157895], ['39119', '39488', 0.6804123711340206], ['39683', '39488', 0.7120075046904315]]

# get match that has the largest match value
best_match = max(closest_match_shapes, key=lambda x: x[2])



im1im2rel_p_matches = []



for closest_match_shape in closest_match_shapes:
  
   
   
   if best_match == closest_match_shape:
      continue
   
   print("im1shapeid " + best_match[0] + " im1nbr_shapeid " + closest_match_shape[0]  + " im2shapeid " + best_match[1] + " im2nbr_shapeid " + closest_match_shape[1] )
   
   
   
   im1bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im1s_pixels[ best_match[0] ] )
   im1nbr_pixels = pixel_shapes_functions.get_boundary_pixels(im1s_pixels[ closest_match_shape[0] ] )
   
   
   im2bnd_pixels = pixel_shapes_functions.get_boundary_pixels(im2s_pixels[ best_match[1] ] )
   im2nbr_pixels = pixel_shapes_functions.get_boundary_pixels(im2s_pixels[ closest_match_shape[1] ] )

   # neighbor contact pixels. pixels that two shapes boundary pixels are neighbor to each other
   im1nbr_contact_p = pixel_shapes_functions.find_direct_neighbors( im1bnd_pixels, im1nbr_pixels )
   im2nbr_contact_p = pixel_shapes_functions.find_direct_neighbors( im2bnd_pixels, im2nbr_pixels )
   

   im1rel_pos = im2rel_pos = None
   if im1nbr_contact_p:
      # include pixels for the im1bnd_pixels only
      im1nbr_contact_p = {k: v for (k,v) in im1nbr_contact_p.items() if "orig" in k }

      
      # returned form
      # [ { pixel index : [  { "x": x, "y", y } ], "count": how many of this pixel index there are  } ]
      im1rel_pos = get_rel_pos_contact_areas( im1nbr_contact_p, im1bnd_pixels, im1file, directory )
      
   else:
      print("im1shapeid " + best_match[0] + " im1nbr_shapeid " + closest_match_shape[0] + " are not neighbors" )
   
   if im2nbr_contact_p:
      im2nbr_contact_p = {k: v for (k,v) in im1nbr_contact_p.items() if "orig" in k }
      im2rel_pos = get_rel_pos_contact_areas( im2nbr_contact_p, im2bnd_pixels, im2file, directory )

   else:
      print("im2shapeid " + best_match[1] + " im2nbr_shapeid " + closest_match_shape[1] + " are not neighbors")



   
   
   if im1rel_pos and im2rel_pos:
      for im1rep in im1rel_pos:
         
         for im1pixel, im1pindexes in im1rep.items():
            
            if im1pixel == "count" and type( im1pindexes ) != list :
               im1im2rel_p_matches[impindex_l]["im1pixel_count"] = im1pindexes
               
               continue
               
            print("im1pixel " + str(im1pixel) )

            for im2rep in im2rel_pos:
               for im2pixel, im2pindexes in im2rep.items():
                  if im2pixel == "count" and type( im2pindexes ) != list :
                     im1im2rel_p_matches[impindex_l]["im2pixel_count"] = im2pindexes
                     continue

                  im1im2rel_p_matches.append( { "im1shapeid": best_match[0],  "im1nbr_sid": closest_match_shape[0], "im1pixel": im1pixel, "im1rel_pix_c": str( len(im1pindexes) ) } )
                  impindex_l = im1im2rel_p_matches.index( { "im1shapeid": best_match[0],  "im1nbr_sid": closest_match_shape[0], "im1pixel": im1pixel, "im1rel_pix_c": str( len(im1pindexes) ) }  )

                  
                  cur_match_counter = 0
                  im1im2rel_p_matches[impindex_l]["im2shapeid"] = best_match[1]
                  im1im2rel_p_matches[impindex_l]["im2nbr_sid"] = closest_match_shape[1]
                  im1im2rel_p_matches[impindex_l]["im2pixel"] = im2pixel
                  im1im2rel_p_matches[impindex_l]["im2rel_pix_c"] = str( len(im2pindexes) )
                  
                  for im1pindex in im1pindexes:
                     
                     for im2pindex in im2pindexes:
                           
                        if im1pindex["x"] + 1 <= im2pindex["x"] and im1pindex["x"] - 1 <= im2pindex["x"]:
                           if im1pindex["y"] + 1 <= im2pindex["y"] and im1pindex["y"] - 1 <= im2pindex["y"]:
                              cur_match_counter += 1
                              break
      
                  im1im2rel_p_matches[impindex_l]["count"] = cur_match_counter

    
    
               
print("im1im2rel_p_matches")
print(im1im2rel_p_matches)


# im1rel_pix_c and im2rel_pix_c are counts of non-contact area pixels
# [ {'im1shapeid': '36901', 'im1nbr_sid': '36360', 'im1rel_pix_c': '35', 'im2shapeid': '37260', 'im2nbr_sid': '36540', 'im2rel_pix_c': '56', 'im1p_total': im1p_total, 'im2p_total': im2p_total,
#    'im1pixels': [ all image1 pixel indexes ], 'im2pixels': [ all image2 pixel indexes ]},
#   {'im1pixel': 35487, 'im2pixel': 36903, 'count': 0, 'im2pixel_count': '1', 'im1pixel_count': '3'}, 
#   {'im1pixel': 35488, 'im2pixel': 36903, 'count': 0, 'im2pixel_count': '1', 'im1pixel_count': '3'}, ...... ]
im1im2nbr_rslt = []
im1im2nbr_rslt.append( { "im1shapeid": im1im2rel_p_matches[0]["im1shapeid"], "im1nbr_sid": im1im2rel_p_matches[0]["im1nbr_sid"],
                         "im1rel_pix_c": im1im2rel_p_matches[0]["im1rel_pix_c"], "im2shapeid": im1im2rel_p_matches[0]["im2shapeid"],
                         "im2nbr_sid": im1im2rel_p_matches[0]["im2nbr_sid"], "im2rel_pix_c": im1im2rel_p_matches[0]["im2rel_pix_c"] } )
im1im2nbr_rslt[0]["im1pixels"] = []
im1im2nbr_rslt[0]["im2pixels"] = []



rel_pos_match_threshold = 0.7
first = True
for im1im2rel_p_match in im1im2rel_p_matches:
   
   # initialization that will be done only one time
   if first:
      im1p_total = im2p_total = im1im2match_total = 0
      im1im2match_total
      
      first = False
   
      match = False
   
   # 'im2p_total': im2p_total can be obtained from looping all im2 pixels of first im1pixel
   if im1im2rel_p_match["im1pixel"] == im1im2rel_p_matches[0]["im1pixel"]:
      im2p_total += int( im1im2rel_p_match["im2pixel_count"] )
      
      im1im2nbr_rslt[0]["im2pixels"].append( im1im2rel_p_match["im2pixel"] )

   if int(im1im2rel_p_match["count"]) / int(im1im2rel_p_match["im1rel_pix_c"]) >= rel_pos_match_threshold:
      match = True
      
      im1im2nbr_rslt.append( { "im1pixel": im1im2rel_p_match["im1pixel"], "im2pixel": im1im2rel_p_match["im2pixel"], "count": im1im2rel_p_match["count"], 
                               "im2pixel_count": im1im2rel_p_match["im2pixel_count"] } )     
      
      
      

   if im1im2rel_p_match.get("im1pixel_count"):
      # im1pixel_count is at the end of im1pixel so put into im1pixels list in im1im2nbr_rslt
      im1im2nbr_rslt[0]["im1pixels"].append( im1im2rel_p_match["im1pixel"] )
      
      im1p_total += int( im1im2rel_p_match.get("im1pixel_count") )

      im1im2nbr_rslt[0]["im2p_total"] = str( im2p_total )

      if match:
         im1im2nbr_rslt.append( { "im1pixel": im1im2rel_p_match["im1pixel"], "im2pixel": im1im2rel_p_match["im2pixel"], "count": im1im2rel_p_match["count"], 
                               "im1pixel_count": im1im2rel_p_match["im1pixel_count"] } )
      
         im1im2match_total += int( im1im2rel_p_match["im1pixel_count"] )
      
      # initialize for the next im1pixel
      match = False




   if im1im2rel_p_matches[-1] == im1im2rel_p_match:
      # last im1pixel
      im1im2nbr_rslt[0]["im1p_total"] = str( im1p_total )


      
      if im1im2match_total / im1p_total > 0.5:
         print("im1shape " + im1im2rel_p_matches[0]["im1shapeid"] + " im1 neighbor shape " + im1im2rel_p_matches[0]["im1nbr_sid"] + \
               " and im2shape " + im1im2rel_p_matches[0]["im2shapeid"] + " and im2 neighbor shape " + im1im2rel_p_matches[0]["im2nbr_sid"] + \
               " matched by " + str(im1im2match_total / im1p_total) )









































