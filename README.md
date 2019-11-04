# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.


Instructions

image format must NOT be JPG!!! JPG does not work! Use PNG instead.

make sure to povide image at this line
original_image = Image.open("images\\birdcopy small.png")

To execute this program.
On windows.
py -3 finding_shapes.py

On linux:
python3 finding_shapes.py

This program takes all pixels of the image and compare every pixel with its neighbors. If the appearance is similar, 
the pixels will be put in the same shape.

At the end of the processing, it will write all shapes with all pixel numbers into file.

recreate shapes.py takes it further with the shapes file created above. It reads the shape's file created and recreates each shape. 


drag_on_image.py

this displays the image on window ( by using tkinter, python GUI library) and lets you mouse click the image and drag around the
area of interest. Once you let go of the mouse click, all coordinates are created for the area that you just circled around and it will create all images shapes that fall inside the mouse circled area! for details, please see presentation.


create objectshape from matched shape ids.py

this file creates whole object shape from mouse circled area. drag_on_image.py above created the individual shapes that fell inside the mouse circled area. The file is also created including all individual shapes of mouse circled area. This file reads this file (which is named "filename + matched shape ids.txt") and creates the one whole object image of the mouse circled area. For clarity and details, see presentations



NOTE:

the program is constantly updated so the presentations or explanations here may not be applicable anymore.

