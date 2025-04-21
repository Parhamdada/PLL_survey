import csv
import ipdb

input_file = "NewPapers_forSurvey.csv"
output_file = "pll_data_new.csv"

with open(input_file, "r", newline="", encoding="utf-8") as infile, \
     open(output_file, "w", newline="", encoding="utf-8") as outfile:

    reader = csv.reader(infile)
    writer = csv.writer(outfile)

    author_column_idx = 2

    for row in reader:
        # ipdb.set_trace()
        row[author_column_idx] = row[author_column_idx].replace("\n", " & ")
        writer.writerow(row)        

print(f"Cleaned CSV saved to: {output_file}")
