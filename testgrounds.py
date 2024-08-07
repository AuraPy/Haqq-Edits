
# Import everything needed to edit video clips  
from moviepy.editor import *
    
# loading video dsa gfg intro video  
clip = VideoFileClip("/home/zayan/Documents/Python_Projects/Haqq-Edits/7128441-uhd_2160_3840_24fps.mp4")  
    
# clipping of the video   
# getting video for only starting 10 seconds  
clip = clip.subclip(0, 20)
    
# Reduce the audio volume (volume x 0.8)
clip = clip.volumex(0.0)  
    
# Generate a text clip  
txt_clip = TextClip("This is the hell\nyou were promised.\nEnter therein\nto burn today.", fontsize = 125, color = 'white')  
    
# setting position of text in the center and duration will be 10 seconds  
txt_clip = txt_clip.set_pos('center').set_duration(10)  
    
# Overlay the text clip on the first video clip  
video = CompositeVideoClip([clip, txt_clip])
video.write_videofile("/home/zayan/Documents/Python_Projects/Haqq-Edits/7128441-uhd_2160_3840_24fps.mp4")
