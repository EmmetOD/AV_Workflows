import zipfile
import pandas as pd
import xml.etree.ElementTree as ET
import os

# File paths
mvr_file_path = '/Users/emmet/Desktop/MVRS/AuraTest.mvr'  # Input MVR file
xml_output_dir = '/Users/emmet/Desktop/'  # Directory for extracted XML
csv_output_path = '/Users/emmet/Desktop/fixtures_data.csv'  # Output CSV file
xml_file_name = 'GeneralSceneDescription.xml'

def extract_xml_from_mvr(mvr_path, output_dir, xml_file):
    """
    Extracts the XML file from the given MVR file.
    """
    with zipfile.ZipFile(mvr_path, 'r') as zip_ref:
        zip_ref.extract(xml_file, output_dir)
    return os.path.join(output_dir, xml_file)

def convert_xml_to_csv(xml_path, csv_path):
    """
    Converts the extracted XML file to a CSV file using Pandas.
    """
    # Parse the XML content
    tree = ET.parse(xml_path)
    root = tree.getroot()

    # Initialize a list to store data
    fixtures_with_layers = []

    # Process fixtures within layers
    for layer in root.findall(".//Layer"):
        layer_name = layer.get("name")  # Get layer name
        for fixture in layer.findall(".//Fixture"):
            fixture_data = {
                "Layer": layer_name,  # Layer exists
                "FixtureName": fixture.get("name"),
                "GDTFSpec": fixture.findtext("GDTFSpec"),
                "GDTFMode": fixture.findtext("GDTFMode"),
                "FixtureID": fixture.findtext("FixtureID"),
                "Address": fixture.find(".//Address").text if fixture.find(".//Address") is not None else None
            }
            fixtures_with_layers.append(fixture_data)

    # Process fixtures outside of layers
    for fixture in root.findall(".//Fixture"):
        # Check if the fixture is already processed (inside a layer)
        is_processed = any(f["FixtureName"] == fixture.get("name") for f in fixtures_with_layers)
        if not is_processed:
            fixture_data = {
                "Layer": None,  # No layer
                "FixtureName": fixture.get("name"),
                "GDTFSpec": fixture.findtext("GDTFSpec"),
                "GDTFMode": fixture.findtext("GDTFMode"),
                "FixtureID": fixture.findtext("FixtureID"),
                "Address": fixture.find(".//Address").text if fixture.find(".//Address") is not None else None
            }
            fixtures_with_layers.append(fixture_data)

    # Create a Pandas DataFrame
    df = pd.DataFrame(fixtures_with_layers)
    
    # Styling of CSV File
    # 1. Order rows by FixtureID
    df["FixtureID"] = pd.to_numeric(df["FixtureID"], errors="coerce")  # Convert FixtureID to numeric
    df.sort_values(by="FixtureID", inplace=True)

    # 2. Reorder columns
    df = df[["Layer", "FixtureName", "FixtureID", "GDTFSpec", "GDTFMode", "Address"]]

    # 3. Rename column headers (e.g., "FixtureID" becomes "Patch")
    df.rename(columns={
        "Layer": "Layer",
        "FixtureName": "Name",
        "FixtureID": "Hd. Number",
        "GDTFSpec": "Specification",
        "GDTFMode": "Mode",
    }, inplace=True)

    # 4. Calculate Address column using DMX universes
    def calculate_dmx_address(address):
        if pd.notnull(address):
            try:
                address = int(address)  # Ensure address is an integer
                universe = (address - 1) // 512 + 1
                channel = (address - 1) % 512 + 1
                return f"{universe}.{channel:03}"
            except ValueError:
                return None
        return None

    df["Address"] = df["Address"].apply(calculate_dmx_address)

    # Export the DataFrame to a CSV file
    df.to_csv(csv_path, index=False)  # index=False excludes the DataFrame index from the CSV file
    print(f"CSV file has been saved to: {csv_path}")

# Main Execution
print("Extracting XML from MVR...")
extracted_xml_path = extract_xml_from_mvr(mvr_file_path, xml_output_dir, xml_file_name)
print(f"XML file extracted to: {extracted_xml_path}")

print("Converting XML to CSV...")
convert_xml_to_csv(extracted_xml_path, csv_output_path)
