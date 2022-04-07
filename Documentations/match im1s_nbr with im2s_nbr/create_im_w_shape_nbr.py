from PIL import Image



image_width = 80
image_height = 100

new_image = Image.new('RGB', (image_width,image_height))

start_coord = ( 20, 30 )

sqr_rgb = ( 100, 100, 100 )

sqr_len = 30


nbr_sqr_rgb = ( 150, 150, 150 )
nbr_sqr_len = 8




for y in range(image_height):
   for x in range(image_width):
      
      if y >= start_coord[1] - nbr_sqr_len and y < start_coord[1]:
         # y is within the area of neighbor shape
         # see if x is also within the neighbor shape area
         
         # check if x is less than last pixel and greater than or equal to first neighbor shape pixel in x direction
         if x < start_coord[0] + sqr_len and x >= start_coord[0] + sqr_len - nbr_sqr_len:
            # xy is within neighbor shape area
            
            new_image.putpixel( (x, y) , nbr_sqr_rgb)

      if x >= start_coord[0] and x < start_coord[0] + sqr_len:
         if y >= start_coord[1] and y < start_coord[1] + sqr_len:
            new_image.putpixel( (x, y) , sqr_rgb)




new_image.save('images/nbr_shape1.png')
new_image.close()






