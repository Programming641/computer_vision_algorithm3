# computer_vision_algorithm3
finding shapes based on the appearance change. my first attempt to analyze pictures at low level

## Operating environment
Windows 10

Python 3

## Note

Please note that I am not using any conventional computer vision algorithm! algorithm are entirely created by me! The advantages of my algorithm are straightforward and intuitive, because for one, I am not using heavy mathmatics.

execute the following and see how it works for yourself!!!

**Caution:** image format must NOT be JPG!!! JPG does not work! Use PNG instead.

## Directory structure

![無題](https://user-images.githubusercontent.com/56218301/229271311-e689ada3-ed6c-4e5c-b516-8d734e57c071.png)


### Instructions

#### preparation before executing python scripts.

- set PYTHONPATH environment variable

this needs to be the project top directory

in windows 10

~~~
set PYTHONPATH= "this project top directory"
~~~

also set global variable of top project directory

#### libraries/cv_globals.py

![global top_directory](https://user-images.githubusercontent.com/56218301/223993262-cba3c9d3-4d73-4340-9b2e-0e87ec0ee180.png)

#### algorithms/fundamental/putpix_into_clgrp.py 

![putpix_into_clrgrp](https://user-images.githubusercontent.com/56218301/223995514-43e1f79c-5b7d-4bef-96b0-2301c54bc904.png)


~~~
py  algorithms/fundamental/putpix_into_clgrp.py 
~~~

examples of results

original

![1](https://user-images.githubusercontent.com/56218301/223995965-405a2f40-f1e0-4f1f-8bf2-e7468c6c5fbf.png)

![1](https://user-images.githubusercontent.com/56218301/223996102-4571793b-8cbd-4440-9cd2-d94277af52d4.png)


#### algorithms/fundamental/find_shapes.py

![find_shapes](https://user-images.githubusercontent.com/56218301/223996977-9bc09cd2-aabe-45cb-bd16-197db59a3717.png)

execute "find_shapes.py" without any parameters just like many of the other python scripts of this project.


![find_shapes2](https://user-images.githubusercontent.com/56218301/223997693-1ac5aa6a-cff7-4768-87d0-9c029285941e.png)


after executing it, 

"filename"_shapes.txt will be created under shapes folder

![shapes files](https://user-images.githubusercontent.com/56218301/223998871-8408ec9f-d0ee-4785-94b5-f4b1ffa48acf.png)


- Then, execute "recreate_shapes.py". This is needed by some python scripts below to show images of shapes.

![recreate_shapes](https://user-images.githubusercontent.com/56218301/223999818-49c7df2a-7611-4bd8-bf1d-f2027efae418.png)

execute it without parameters

~~~
py recreate_shapes.py
~~~

### scripts that need to be executed to run most of the scripts

- putpix_into_clrgrp.py
- find_shapes.py
- create_shape_locations.py
- create_shape_neighbors.py
- find_edges.py
- findim_pixch.py
- recreate_shapes.py

#### help_lib/create_shape_locations.py


![無題](https://user-images.githubusercontent.com/56218301/229271689-67c681ef-bc8a-4c2f-9cb1-ce16bc3d6d42.png)

#### help_lib/create_shape_neighbors.py

![無題](https://user-images.githubusercontent.com/56218301/229272104-e1d86de2-6635-40dc-90a2-f6bafa48c524.png)



## edge detection
find_edges.py

**examples**

-executing on the original produces such great results!

![1](https://user-images.githubusercontent.com/56218301/167111595-cda24611-a4f1-4a6d-8516-d675dcbabd59.png)
![leaf_mov_orig1clrgrp_70_70resized](https://user-images.githubusercontent.com/56218301/167110586-851fedc0-4b58-4865-8cb1-0af54f8a2acb.png)

![1](https://user-images.githubusercontent.com/56218301/167111645-54b68a84-1710-41e5-8dde-e5e5fb066d76.png)
![sea_ride_orig1clrgrp_70_70resized](https://user-images.githubusercontent.com/56218301/167111935-707a1dd4-dfd7-47f4-963f-e7fd865fa58a.png)

![1](https://user-images.githubusercontent.com/56218301/167112014-16aa3325-5446-4c97-84e0-ad8ad945c192.png)
![street_orig1clrgrp_70_70resized](https://user-images.githubusercontent.com/56218301/167112277-22a42350-6860-4ee0-9ee6-dd413ccd92ec.png)




## Repeating pattern shapes

### Instructions

I'll update on this later on.

### Execution Results examples

Original Image

![dog](https://user-images.githubusercontent.com/56218301/146460923-3a92db6e-a0c4-4a37-9637-6d9e8f10ce13.png)
![dog_clr_grp](https://user-images.githubusercontent.com/56218301/146460935-5a73c5dc-e4ad-4dba-8fcd-fda84206c40e.png)

![147](https://user-images.githubusercontent.com/56218301/146707275-c8e7dd24-5f59-4081-8424-8f4b3476807c.png)
![967](https://user-images.githubusercontent.com/56218301/146707279-50fb2a3f-c73a-44e9-b6c5-60731787d791.png)
![2900](https://user-images.githubusercontent.com/56218301/146707291-b9e980d7-e9dc-4fbb-88c3-0aaef42593b7.png)
![17614](https://user-images.githubusercontent.com/56218301/146707296-104b82c9-f72c-40c8-95f3-b5cfce247c16.png)
![19007](https://user-images.githubusercontent.com/56218301/146707303-292ebefe-cd36-4478-b374-b6471f04066c.png)
![22122](https://user-images.githubusercontent.com/56218301/146707308-0fcde6e1-bc9e-49c9-b5a3-21ada745159b.png)
![28743](https://user-images.githubusercontent.com/56218301/146707313-2ec1e890-bfdd-4a3d-9f03-ecfac16e61da.png)

### Combine repeating pattern shapes

combine_rpt_ptn_shapes.py

***great result but big disadvantage is very very slow!!!!***

I'll work on it to improve its speed.

![1](https://user-images.githubusercontent.com/56218301/167757599-d4fff3bc-4316-4162-bee4-89087b563550.png)

![764](https://user-images.githubusercontent.com/56218301/167757652-3a139646-fce5-40c6-9a9f-8835cbab4d42.png)
![1085](https://user-images.githubusercontent.com/56218301/167757661-bd327c6e-a5a3-4ed7-9c4e-e7718fd98e9b.png)




# Video Analysis

## the video analysis is all about finding the same shape between frames! sounds boring and tiring which is it is... but I believe computer vision for video is all about that!

## Requirement

- You need frames from video

At least two consecutive frames are needed.

you can use **ffmpeg** to get frames from the video

example video

https://user-images.githubusercontent.com/56218301/140649130-48e34f72-b9c7-4533-877d-94d96134cf73.mp4

## pixel change analysis between video frames ( usually between two consecutive frames from the same video )

### running examples

original image1 original image2

![1_clrgrp](https://user-images.githubusercontent.com/56218301/160788385-38ca6232-4da6-4390-a812-61c8dbc96f2a.png)
![2_clrgrp](https://user-images.githubusercontent.com/56218301/160788396-436991c0-1027-4b96-b5ff-8caa668d86ce.png)


taking difference between frames above

![diff12result1](https://user-images.githubusercontent.com/56218301/160788480-e0ec30f6-fac7-48cf-8ade-0b31c67d3ceb.png)
![diff12result2](https://user-images.githubusercontent.com/56218301/160788496-14a8bf87-ec82-43b5-a10a-f59624693d61.png)


**another example**

![birdflying1](https://user-images.githubusercontent.com/56218301/160788687-bc9e5be6-d146-4b41-932e-8f806ca02b21.png)
![birdflying2](https://user-images.githubusercontent.com/56218301/160788722-189dac54-6aad-4a13-b6eb-4de6e64c210c.png)


![birdflying1_clr_grp](https://user-images.githubusercontent.com/56218301/160788748-39ab3395-6e28-4699-a339-334d8a3b713e.png)
![birdflying2_clr_grp](https://user-images.githubusercontent.com/56218301/160788759-69168a2e-35c2-4f19-bf27-61efc7558879.png)

![diff12result1](https://user-images.githubusercontent.com/56218301/160788785-b54ff963-6a0c-4b57-8a36-b090b3aa3dc8.png)
![diff12result2](https://user-images.githubusercontent.com/56218301/160788795-a4598c9d-78bb-4b55-930a-01fa6345f94d.png)

original image

![1](https://user-images.githubusercontent.com/56218301/167390805-f775ed91-e365-42c8-9e80-f95527575cd1.png)
![2](https://user-images.githubusercontent.com/56218301/167390826-7fcb291c-5ee0-496c-a867-e6abf3f468c2.png)



![analyzing image difference1-1](https://user-images.githubusercontent.com/56218301/167390316-7160fc3f-403b-4fd0-9815-a9557bde4daf.png)

![analyzing image difference2-1](https://user-images.githubusercontent.com/56218301/167390372-40847e6b-9acc-4e8b-8775-48d18043d190.png)

![analyzing image difference3-1](https://user-images.githubusercontent.com/56218301/167390405-8a80cbf8-1eb4-4b0b-a540-849fac50ef5b.png)



original image

![1](https://user-images.githubusercontent.com/56218301/167391021-b5861fcb-fce7-493e-806a-8e8b0e761134.png)
![2](https://user-images.githubusercontent.com/56218301/167391040-d3633f39-287c-40aa-a5e3-3efe26623e02.png)


![analyzing image difference4-1](https://user-images.githubusercontent.com/56218301/167390444-d03f5bd5-814e-4bf7-9e25-625fc406a36d.png)



## find_staying_Lshp_btwn_frames.py

this script finds large shapes ( shapes with more than 50 pixels ) that did not move to another locations but stayed or moved a little in the next frame.


execution examples

original images

![24](https://user-images.githubusercontent.com/56218301/224001739-d137e267-b4ce-42b3-bcbf-2e54c733a9da.png)
![25](https://user-images.githubusercontent.com/56218301/224001769-58c8f5c0-bd64-4dfe-860f-7f3404a33582.png)

putpix_into_clrgrp.py --minimized colors version--

![24](https://user-images.githubusercontent.com/56218301/224001806-60ea7997-c070-4f6a-9df8-d9836e126b4a.png)
![25](https://user-images.githubusercontent.com/56218301/224001821-987b8e80-513e-422a-9388-78a867cccb20.png)


the results are perfect! works 100%!

![find_staying_Lshp_btwn_frames](https://user-images.githubusercontent.com/56218301/224004907-6459650e-bccc-4511-b0f4-b0fce91c3407.png)








## find_staying_Lshp_wo_pixch_btwn_frames.py

this is similar to find_staying_Lshp_btwn_frames.py but what is different is that this finds large shapes even if lots of pixel changes occurred.

execution examples

original images

![10](https://user-images.githubusercontent.com/56218301/224007382-cd3d944d-f9a4-4421-93f7-202b78711fa4.png)
![11](https://user-images.githubusercontent.com/56218301/224007393-f4e7ca8e-f205-4d7e-b5ad-520b9711681c.png)

![10](https://user-images.githubusercontent.com/56218301/224007410-cc393a1a-a9b2-4366-a8b4-9d68ddb221c7.png)
![11](https://user-images.githubusercontent.com/56218301/224007422-18295251-0322-42b2-bd02-f8f9a0ae0364.png)


![find_staying_Lshp_wo_pixch_btwn_frames](https://user-images.githubusercontent.com/56218301/224009151-123a108f-de8e-47b8-ad6f-665ebdcd3083.png)


## find_internal_s_pixc_shapes.py

this script finds small pixels shapes that entirely surrounded by the one large shape. entirely surronded by one large shape means that they are internal shapes within the one large shape.


![internal shapes1](https://user-images.githubusercontent.com/56218301/224010500-3c13d4e3-4e7e-47db-bf72-8f44fbbe3526.png)

![internal shapes2](https://user-images.githubusercontent.com/56218301/224010518-369e2132-3830-4aa8-a878-e2e9f63d75f4.png)

example

original

![24](https://user-images.githubusercontent.com/56218301/224011010-f37efd1c-a726-4bf7-ba22-56b89119cf89.png)
![24](https://user-images.githubusercontent.com/56218301/224011021-c4452f77-8579-42ee-b192-e85fd7f28f7b.png)


![50934](https://user-images.githubusercontent.com/56218301/224011136-fe8e535d-b462-434b-bff0-f3e360c0e3b2.png)
![73989](https://user-images.githubusercontent.com/56218301/224011150-c200e5f9-7ac6-4202-a0e6-23c8f6dba75c.png)
![101926](https://user-images.githubusercontent.com/56218301/224011195-217af7f1-1c25-4946-bc08-8552c7540600.png)
![101932](https://user-images.githubusercontent.com/56218301/224011225-1785cb73-01d0-4e8b-9bd2-c75769528065.png)
![102222](https://user-images.githubusercontent.com/56218301/224011237-8ee65fc7-c7b4-4d2d-911b-6c242c7427c4.png)




execute  recreate_internal_s_pixc_shapes.py to see the results


## algorithms/spixc/find_spixc_shapes_nbrs_among_frames.py

required scripts
find_spixc_shapes_nbrs.py
find_spixc_shapes_nbrs_btwn_frames.py
recreate_shapes/spixc_shapes_nbrs.py

![無題](https://user-images.githubusercontent.com/56218301/229273162-75bf416d-48b8-4827-ab74-e8203d386250.png)




## Note
this is not the end of the project! Now, I am getting closer to first milestone of object detection!

**if you like this project, please consider supporting me by sponsoring this project or hire me so I can work on this project for you!**
