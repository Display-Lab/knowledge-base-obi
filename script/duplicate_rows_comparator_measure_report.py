import csv
import uuid

# Measures to duplicate with new row
measures_to_duplicate = {
    'active_arrest_comp',
    'arrest_descent_comp',
    'failed_induction_comp',
    'ytd_active_arrest_comp',
    'ytd_arrest_descent_comp',
    'ytd_failed_induction_comp',
}

input_file = 'obi/ComparatorMeasureReportNew.csv'
output_file = 'obi/ComparatorMeasureReportNew1.csv'

rows = []
with open(input_file, newline='') as csvfile_in:
    reader = csv.DictReader(csvfile_in)
    fieldnames = reader.fieldnames
    for row in reader:
        rows.append(row)
        if row['measure'] in measures_to_duplicate:
            new_row = row.copy()
            new_row['identifier'] = str(uuid.uuid4())
            new_row['measureScore.rate'] = '0.8'
            new_row['measureScore.denominator'] = ''
            new_row['group.code'] = 'http://purl.obolibrary.org/obo/PSDO_0000094'
            rows.append(new_row)

with open(output_file, 'w', newline='') as csvfile_out:
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
