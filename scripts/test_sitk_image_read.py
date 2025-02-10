import SimpleITK as sitk

file = '/gpfs/projects/KimGroup/data/mic-mkfz/raw/Dataset104_CBCTRectumBowel/imagesTr/rectumbowel_000_0000.mha'

# Load the MHA image
image = sitk.ReadImage(file)

# Convert to a NumPy array (optional)
image_array = sitk.GetArrayFromImage(image)

# Print image information
print("Image Size:", image.GetSize())
print("Spacing:", image.GetSpacing())
print("Pixel Type:", image.GetPixelIDTypeAsString())