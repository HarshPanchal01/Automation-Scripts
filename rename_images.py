import exifread
import os
from datetime import datetime            

def extract_metadata(file_path):
    try: # open the file and put its exif data into a dictionary then return it
        with open(file_path, 'rb') as f:
            tags = exifread.process_file(f)
            #print(tags)
            metadata = {}
            for tag in tags.keys():
                tag_name = tag.replace("EXIF ", "") # need to replace 'EXIF' because its always in the key values
                metadata[tag_name] = str(tags[tag])
            return metadata
    except Exception as e:
        print(f"Error occurred while extracting info: {e}")
        return None
    
def rename_files(folder):
    i = 1 # count for the images
    for filename in os.listdir(folder): # loop through each image file
        if filename.lower().endswith(".jpg"):
            file_path = os.path.join(folder, filename)
            # get the metadata for the image
            metadata = extract_metadata(file_path)
            if metadata:
                # get the original date of the image taken and the make of the device which took it
                datetime_original = metadata.get("DateTimeOriginal")
                device_make = metadata.get("Image Model")
                #print(device_make)
                if datetime_original:
                    # convert the time to month, day, year
                    datetime_obj = datetime.strptime(datetime_original, "%Y:%m:%d %H:%M:%S")
                    # set new filename structure 
                    new_filename = f"[{i}] {datetime_obj.strftime('%B')}-{datetime_obj.day}-{datetime_obj.year} ({device_make}).jpg"
                    # need to get the correct paths 
                    source_file = os.path.join(folder, filename)
                    destination_file = os.path.join(folder, new_filename)
                    # rename
                    os.rename(source_file, destination_file)
                    # increment counter
                    i += 1

# set this with correct directory for the script to work
folder = "directory/to/images"
rename_files(folder)
