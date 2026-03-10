import csv

# List of measure values to remove
measures_to_remove = {
    'cat2',
    'elective_induction',
    'latent_phase_arrest_comp',
    'medical_induction',
    'spontaneous_labor',
    'ytd_cat2',
    'ytd_elective_induction',
    'ytd_latent_phase_arrest_comp',
    'ytd_medical_induction',
    'ytd_spontaneous_labor',
}

input_file = 'obi/ComparatorMeasureReport.csv'
output_file = 'obi/ComparatorMeasureReportNew.csv'

with open(input_file, newline='') as csvfile_in:
    reader = csv.DictReader(csvfile_in)
    rows = [row for row in reader if row['measure'] not in measures_to_remove]
    fieldnames = reader.fieldnames

with open(output_file, 'w', newline='') as csvfile_out:
    writer = csv.DictWriter(csvfile_out, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(rows)
