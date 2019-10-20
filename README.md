# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level


warning!
Make sure to use the small picture! about 100 x 100

This requres a very heavy processing. It will take about 10 minutes to complete. the search algorithm for figuring out
if current pixel is already in other pixel's shape needs work.

This program takes all pixels of the image and compare every pixel with its neighbors. If the appearance is similar, 
the pixels will be put in the same shape.

At the end of the processing, it will write all shapes with all pixel numbers into file.

