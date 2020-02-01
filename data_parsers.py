import csv

ID_TO_FIELD_NAME = {
	0: "id",
	1: "name",
	2: "developer",
	4: "product-type",
	5: "good-type",
	6: "length",
	7: "width",
	8: "height",
	10: "diameter",
	11: "warranty",
	12: "weight",
	13: "volume"
}

def parse_data(input_file_name):
	header = True
	data_chunks = []
	with open(input_file_name, newline='') as csvfile:
		reader = csv.reader(csvfile, delimiter='\t')
		for row in reader:
			if header:
				header = False
				continue
			data_chunks.append({ID_TO_FIELD_NAME[i]: row[i] for i in range(len(row)) if i in ID_TO_FIELD_NAME})
	return data_chunks
