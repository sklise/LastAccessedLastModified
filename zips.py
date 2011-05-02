zipcodes = dict()
zips = open('zips.txt')
for line in zips:
	line = line.strip()
	bits = line.split(",")
	# print bits[1].strip('"')
	zipcodes[int(bits[1].strip('"'))] = bits[3].strip('"')