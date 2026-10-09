from PIL import Image

im = Image.open("Liturgical Monuments/Monument 6 - 1910 Skaballanovich Typikon/Source Text/images/p751.png")
crop_box = (150, 150, 1550, 450)
im_crop = im.crop(crop_box)
im_crop.save("scratch/p751_crop.png")
print("Saved p751_crop.png")
