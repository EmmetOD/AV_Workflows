import zipfile

# Specify the path to the MVR file (ZIP archive)
mvr_file_path = '/Users/emmet/Desktop/MVRS/1ForAllMartin.mvr'
extracted_xml_path = '/Users/emmet/Desktop/GeneralSceneDescription.xml'  # Path to save extracted XML

# Open the .mvr file as a ZIP archive
with zipfile.ZipFile(mvr_file_path, 'r') as zip_ref:
    # List all files in the ZIP archive
    zip_ref.printdir()

    # Extract the specific XML file
    zip_ref.extract('GeneralSceneDescription.xml', '/Users/emmet/Desktop')

print(f"XML file extracted to: {extracted_xml_path}")
