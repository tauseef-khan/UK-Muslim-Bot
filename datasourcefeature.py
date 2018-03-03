def readSourceInformation():

	filename = "datasources.txt"
	sourcesText = open(filename, "r")

	lines = sourcesText.readlines()

	message = ""
	for line in lines:
		message += line

	return message