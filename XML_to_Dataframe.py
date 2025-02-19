import pandas as pd
import xml.etree.ElementTree as ET

# Path to the extracted XML file
xml_file_path = '/Users/emmet/Desktop/GeneralSceneDescription.xml'

# Parse the XML content
tree = ET.parse(xml_file_path)
root = tree.getroot()

# Initialize an empty list to hold data
data = []

# Iterate through each <Fixture> element in the XML
for fixture in root.findall(".//Fixture"):
    fixture_data = {
        "Name": fixture.get("name"),
        "UUID": fixture.get("uuid"),
        "GDTFSpec": fixture.findtext("GDTFSpec"),
        "GDTFMode": fixture.findtext("GDTFMode"),
        "FixtureID": fixture.findtext("FixtureID"),
        "UnitNumber": fixture.findtext("UnitNumber"),
        "FixtureTypeId": fixture.findtext("FixtureTypeId"),
        "CustomId": fixture.findtext("CustomId"),
        "Color": fixture.findtext("Color"),
        "CastShadow": fixture.findtext("CastShadow"),
        "Address": fixture.find(".//Address").text if fixture.find(".//Address") is not None else None
    }
    data.append(fixture_data)

# Create a Pandas DataFrame
df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
csv_file_path = '/Users/emmet/Desktop/MVR.csv'  # Specify the output CSV file path
df.to_csv(csv_file_path, index=False)  # index=False excludes the DataFrame index from the CSV file

print(f"CSV file has been saved to: {csv_file_path}")
