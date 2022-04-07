from PIL import Image



image_width = 80
image_height = 100

new_image = Image.new('RGB', (image_width,image_height))

start_coord = ( 20, 30 )

sqr_rgb = ( 100, 100, 100 )

sqr_len = 30


nbr_sqr_rgb = ( 150, 150, 150 )
nbr_sqr_len = 8

im2_lench = 5


for y in range(image_height):
   for x in range(image_width):
            
      if x >= start_coord[0] and x < start_coord[0] + sqr_len :
         if y >= start_coord[1] and y < start_coord[1] + sqr_len :
            new_image.putpixel( (x, y) , sqr_rgb)
      
      
      p_counter = 0
      decrease = False
      for add_py in range( start_coord[1] + sqr_len - 8, start_coord[1] + sqr_len):
         if p_counter ==4:
            decrease = True
            
         if decrease:
            p_counter -= 1
         else:
            p_counter += 1 
      

         p_last_counter = 1
         for add_px in range(start_coord[0] + sqr_len, start_coord[0] + sqr_len + p_counter):
         
            if p_counter == 4:
               p_last_counter += 1
               
            if p_last_counter > 4:
               continue
               
            new_image.putpixel( (add_px, add_py) , sqr_rgb)

         
         for nb_x in range( start_coord[0] + sqr_len + 3, start_coord[0] + sqr_len + 4 + nbr_sqr_len ):
            new_image.putpixel( (nb_x, add_py) , nbr_sqr_rgb)



new_image.save('images/nbr_shape2.png')
new_image.close()






