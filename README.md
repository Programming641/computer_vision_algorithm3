# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level

Instructions

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
area of interest. Once you let go of the mouse click, all coordinates are created for the area that you just circled around.

Upcomping next, which is what I am working on now.


Later, this will be matched with the recreate shapes.py. recreate shapes.py created all shapes of the image. By combining drag_on_image.py with the recreate shapes.py, you will have all shapes of the interested area!






