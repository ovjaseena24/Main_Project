from zipfile import ZipFile
import re
import os
import shutil

file_name='resumes.zip'
with ZipFile(("media/"+file_name), 'r') as zip:
    # printing all the contents of the zip file
    #zip.printdir()

    # extracting all the files
    print('Extracting all the files now...')
    zip.extractall()
    print('Done!')

new_name= re.sub(r'.zip$',"",file_name)

directory=new_name




try:
    os.mkdir("download_folder")
except OSError:
    print("Directory creation failed")

posts=[]

for file in os.listdir(directory):
     filename = os.fsdecode(file)
     if filename.endswith(".pdf"):
         # shutil.copy2(filename,("download_folder"))
         print(filename)
         shutil.copy((new_name+'/'+filename),('download_folder'))
         print("copy successful")

     else:
         continue
print("extraction successful")








