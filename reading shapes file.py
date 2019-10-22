import re

from PIL import Image

original_image = Image.open("images\\bird01.png")

image_width, image_height = original_image.size



f = open('bird01 shapes.txt')
areas = f.read()

'''
( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes 
space then comes [ then comes [0-9]{1,len(str(image_width * image_height))} then comes ] then comes )
single_pixel_pattern = '\([0-9]{1, ' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
'''
single_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[[0-9]{1,' + \
                       str(len(str(image_width * image_height))) + '}\]\)'

print(str(len(str(image_width * image_height)))) 

'''
( then comes [0-9]{1, len(str(image_width * image_height))} then comes , then comes space then comes [ then comes 
GROUPSTART [0-9]{1,len(str(image_width * image_height))} then comes , then comes space GROUPEND then comes [0-9]{1,len(str(image_width * image_height))} 
then comes ] then comes )

GROUPSTART (      GROUPEND )
'''
multiple_pixel_pattern = '\([0-9]{1,' + str(len(str(image_width * image_height))) + '}, \[(?:[0-9]{1,' + str(len(str(image_width * image_height))) + \
                         '},\s{1})+[0-9]{1,' + str(len(str(image_width * image_height))) + '}\]\)'
match = re.findall(multiple_pixel_pattern, areas)

print(match)




f_write = open('bird01 each of the shapes.txt', 'w' )


for m in match:
  f_write.write(str(m) + '\n\n\n')
  
print(type(m))
print(type(match))




f_write.close()

f.close()
