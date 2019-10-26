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

recreate shapes.py takes it further with the shapes file created above. It reads the shape's file created and recreates each shape. But finding shape algorithm does not work as I expect.. I am working on fixing this.

