import piexif


exif_dict = piexif.load("Double_Cheeseburger.jpg")
for ifd in ("0th", "Exif", "GPS", "1st"):
    for tag in exif_dict[ifd]:
        print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])