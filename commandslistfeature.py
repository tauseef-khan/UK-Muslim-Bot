def readCommands():

	filename = "commandslist.txt"
	commandsText = open(filename, "r")

	lines = commandsText.readlines()

	message = ""
	for line in lines:
		message += line

	return message