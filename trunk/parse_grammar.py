import random
import cStringIO

totalOutput = None
startSym = None

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

		nt_prod_map[symbol_name] = prods
	
	return nt_prod_map

def ReadGrammarFile(filename):
	fd = open(filename, 'r')
	grammar_sections = fd.read().split("----------")
	return grammar_sections


def ChooseRandomProduction(productions):
	randomNumber = random.random()
	runningSum = 0.0

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

	elif terminal == '\\n':
		OutputCharacters('\n')

	else:
		OutputCharacters(terminal + ' ')

	return

def OutputCharacters(sym):
	global totalOutput
	totalOutput.write(str(sym))
	return
	
def getFuzzInput(spec, seed):
	global totalOutput 
	totalOutput = cStringIO.StringIO()
	grammar_sections = ReadGrammarFile("./ex_grm.dat")
	nt_prod_map = ParseNonTerminals(grammar_sections[0])
	t_prod_map = ParseTerminals(grammar_sections[1])
	Produce(startSym, nt_prod_map, t_prod_map)
	return totalOutput.getvalue()	

print "\nNow producing..."
print getFuzzInput('postscript', None)
	
	
