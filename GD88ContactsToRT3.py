import csv

# Input and output file paths
input_file = r'C:\Users\grant\Downloads\88contacts.csv'
output_file = r'C:\Users\grant\Downloads\rt3contacts_converted.csv'

# Mapping for Call Type
call_type_map = {
    'Group': '1',
    'Private': '2'
}

# Read from 88contacts.csv and write to RT3 format
with open(input_file, mode='r', newline='', encoding='utf-8') as infile, \
     open(output_file, mode='w', newline='', encoding='utf-8') as outfile:

    reader = csv.DictReader(infile)
    fieldnames = ['Contact Name', 'Call Type', 'Call ID', 'Call Receive Tone']
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        contact_name = row['Name'].strip()
        call_id = row['DMR ID'].strip()
        call_type = call_type_map.get(row['Type'].strip(), '1')  # Default to Group if unknown

        writer.writerow({
            'Contact Name': contact_name,
            'Call Type': call_type,
            'Call ID': call_id,
            'Call Receive Tone': '0'
        })

print(f"✅ Conversion complete. Output saved to {output_file}")
