import cStringIO
import string
import random

totalOutput = None
startSym = None
totalSumDict = {}
nt_prod_map = None
t_prod_map = None

def ParseTerminals(grammar_section):
	unstripped_t_prods = grammar_section.split(";")
	t_prods = []
	t_prod_map = {}

	for elem in unstripped_t_prods:
		t_prods.append(elem.strip())

	for elem in t_prods:
		prod_tuple = elem.split("->")

		if len(prod_tuple) == 1:
			break

		symbol_name = prod_tuple[0].strip()
		t_prod_map[symbol_name] = prod_tuple[1].strip()

	return t_prod_map
	
def ParseNonTerminals(grammar_section):
	global startSym
	unstripped_nt_prods = grammar_section.split(";")
	nt_prods = []
	nt_prod_map = {}

	for elem in unstripped_nt_prods:
		nt_prods.append(elem.strip())

	for elem in nt_prods:
		prod_tuple = elem.split("->")
		
		if len(prod_tuple) == 1:
			break

		symbol_name = prod_tuple[0].strip()

		if not startSym:
			startSym = symbol_name
		
		prods = []
		
		for possible_prod in prod_tuple[1].split("|"):
			prod_info, probability = possible_prod.split("~")
			prods.append((prod_info.strip(), float(probability.strip())))

		nt_prod_map[symbol_name] = tuple(prods)
	
	return nt_prod_map

def ReadGrammarFile(filename):
	fd = open(filename, 'r')
	grammar_sections = fd.read().split("----------")
	return grammar_sections


def ChooseRandomProduction(productions):
	global totalSumDict
	totalSum = 0
	runningSum = 0

	if not totalSumDict.has_key(productions):
		for elem in productions:
			totalSum = totalSum + elem[1]
		totalSumDict[productions] = totalSum
	randomNumber = random.random() * totalSumDict[productions]

	for elem in productions:
		runningSum = runningSum + elem[1]

		if runningSum > randomNumber:
			return elem	

	return productions[len(productions) - 1]


def Produce(sym, nt_prod_map, t_prod_map):
	terminal = t_prod_map.get(sym)

	if not terminal:
		productions = nt_prod_map[sym]
		production = ChooseRandomProduction(productions)
		for symbol in production[0].split():
			Produce(symbol, nt_prod_map, t_prod_map)

	elif terminal == '~newline~':
		OutputCharacters('\n')

	elif terminal == '~nat~':
		randNat = int(random.random() * 1024 * 1024)
		OutputCharacters(str(randNat) + ' ')

	elif terminal == '~int~':
		randInt = int(random.random() * 1024 * 1024)
		
		if (random.random() > 0.5):
			randInt = randInt * -1 

		OutputCharacters(str(randInt) + ' ')

	elif terminal == '~real~':
		randFloat = random.random() * 1024.0 * 1024.0

		if (random.random() > 0.5):
			randFloat = randFloat * -1.0

		OutputCharacters(str(randFloat) + ' ')

	elif terminal == '~posreal~':
		randFloat = random.random() * 1024 * 1024

		OutputCharacters(str(randFloat) + ' ')

	elif terminal == '~string~':
		randStr = ""
		chars = string.letters + string.digits
		numChars = int(random.random() * 16)

		for i in range(numChars):
			randStr = randStr + random.choice(chars)

		OutputCharacters('(' + randStr + ') ')

	elif terminal == '~intstring~':
		randStr = ""
		chars = string.digits
		numChars = int(random.random() * 16)
	
		for i in range(numChars):
			randStr = randStr + random.choice(chars)

		OutputCharacters('(' + randStr + ') ')

	elif terminal == '~realstring~':
		randStr = ""
		chars = string.digits
		numChars = int(random.random() * 16)
	
		for i in range(numChars):
			randStr = randStr + random.choice(chars)
		
		randStr = randStr + "."

		for i in range(randInt + 1, numChars):
			randStr = randStr + random.choice(chars)

		OutputCharacters('(' + randStr + ') ')
			
	else:
		OutputCharacters(terminal + ' ')


	return

def OutputCharacters(sym):
	global totalOutput
	totalOutput.write(str(sym))
	return
	
def getFuzzInput(spec, seed):
	global totalOutput 
	global totalSumDict
	global nt_prod_map
	global t_prod_map
	totalOutput = cStringIO.StringIO()
	
	if not startSym:
		grammar_sections = ReadGrammarFile("./" + spec +  ".grm")
		nt_prod_map = ParseNonTerminals(grammar_sections[0])
		t_prod_map = ParseTerminals(grammar_sections[1])

	random.seed(seed)
	Produce(startSym, nt_prod_map, t_prod_map)
	return totalOutput.getvalue()	

