from unsafe import forensic

image_path = "./images/DSCN0029.jpg"
get_exif_data = forensic.get_image_metadata(path=image_path)
print("EXIF data :", get_exif_data)


edit_image_exif_data = forensic.edit_image_metadata(path=image_path, key="image_description", value="Hello, World!")
get_exif_data = forensic.get_image_metadata(path=image_path)
print("EXIF data after update :", get_exif_data)

# this method delete all metadata
forensic.del_image_metadata(path=image_path)
