# perception_tools
additional utils for working with Unity perception package, which generates synthetic images for AI training.

 
First up - perception to coco converter for 2D bounding boxes is now available.

Perception outputs all the data in their own format, 
but for most object detection, coco format is the default bounding box annotation format.
</b>
## Usage:
provide the path to the perception dir, and a name for the output coco file.
image size must be passed in.  Alternative is open every image and check, longer term can update perception to export this. 
![convert_script](https://user-images.githubusercontent.com/46302957/111084131-27c0ac80-84ce-11eb-9d92-5e951e4630af.JPG)

You can use either the notebook (run all cells down to the 'begin processing' first)...or import via the .py file.  (note that I have tested and use the notebook, the script might need to be tuned...thus recommend the notebook). 



A ready to use/train with coco file is created, in the dataset directory.

![convert_perception](https://user-images.githubusercontent.com/46302957/111054947-9138b080-8425-11eb-88e5-ced6d082de38.JPG)



![convert_complete](https://user-images.githubusercontent.com/46302957/111084148-34dd9b80-84ce-11eb-9f87-7fb32c43ca64.JPG)
