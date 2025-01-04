from pathlib import Path
import conllu, argparse, csv, logging, time, os

class disjunctionExample:
	def __init__(self, head_np, conjuncts, agreementCarrier, has_either, has_neither, sentence, mainPredicate):
		# Get number features, if they exist, for the head 
		if head_np.token['feats']:
			self.head_np_number = head_np.token['feats'].get('Number', 'UNK')
		else:
			self.head_np_number = "UNK"

				
		self.mainPredicateLemma = mainPredicate.token['lemma']

		# Get number features, if they exist, for the conjuncts
		self.conjuncts_number = [self.head_np_number]
		for child in conjuncts:
			if child.token['feats']: #handles words without feature category
				self.conjuncts_number.append(child.token['feats'].get('Number', 'UNK')) #handles words with features, but without number
			else: 
				self.conjuncts_number.append('UNK')

		# Get person features for conjuncts: 
		self.conjuncts_person = get_person_features([head_np]+ conjuncts)

		self.conjuncts_string = get_constituent_string(head_np)
		self.agreementCarrierForm = agreementCarrier.token['form']
		self.agreementCarrierLemma = agreementCarrier.token['lemma']
		self.agreementCarrierNumber = agreementCarrier.token['feats'].get('Number', '')
		self.has_either = has_either
		self.has_neither = has_neither
		self.sentence  = sentence
		self.mainPredicateArc = agreementCarrier.token['deprel']

		if self.conjuncts_number == ['Sing', 'Plur']:
			self.experimental_condition = 'SP'
		elif self.conjuncts_number == ['Sing', 'Sing']:
			self.experimental_condition = 'SS'
		elif self.conjuncts_number == ['Plur', 'Plur']:
			self.experimental_condition = 'PP'
		elif self.conjuncts_number == ['Plur', 'Sing']:
			self.experimental_condition = 'PS'
		else:
			self.experimental_condition = 'UNK'

	def __str__(self):
		return("\t".join([
			self.experimental_condition,
			str(self.has_either), 
			str(self.has_neither), 
			self.conjuncts_number[0],
			self.conjuncts_person[0],
			self.conjuncts_number[1],
			self.conjuncts_person[1],
			self.conjuncts_string,
			self.agreementCarrierForm,
			self.agreementCarrierLemma,
			self.agreementCarrierNumber,
			self.mainPredicateLemma,
			self.mainPredicateArc, 
			self.sentence]))


def get_person_features(conjuncts): 
	# Takes a list of NPS, returns list of 1st, 3rd person etc
	persons = []
	for np_token in conjuncts:
		if np_token.token['upos'] == 'PRON':
			if np_token.token['feats'].get('PronType', 'UNK') != 'Prs':
				person = "Not Personal Pronoun"
			else: 
				person = np_token.token['feats'].get('Person', 'UNK')
		else: 
			person = "Not Pronoun"
		persons.append(person)
	return(persons)

def np_includes_either(root, sentence): 
	# Returns TRUE if root has a child with form 'either'
	either_children  = [child for child in root.children if (child.token['form'] == 'Either') | (child.token['form'] == 'either')]
	return(len(either_children) >0 )

def np_includes_neither(root, sentence): 
	# Returns TRUE if root has a child with form 'either'
	neither_children  = [child for child in root.children if (child.token['form'] == 'Neither') | (child.token['form'] == 'neither')]
	return(len(neither_children) > 0 )


def get_constituent_string(root):
    '''Returns the constituent headed by ROOT as a string 
    Root should be a conllu tree obj 
	Copied from Emmy's Extract Datives.py File
    '''
    serialized = root.serialize()
    lines = serialized.split('\n')
    parsed_lines = [line.split('\t') for line in lines]
    #each sentence has an empty line after it, hence [:-2]
    output = [line[1] for line in parsed_lines[:-2]] 
    return(" ".join(output))

def disjuncted_NPs(root, sentence):
	# Assume that ROOT is a NOUN
	# Checks that ROOT dominates at least one other noun with a CONJ arc, and that the child 
	# noun dominates an OR.
	# Returns nothing if the NP is not a disjunction structure; otherwise returns the list of conjuncts 

	
	conjunct_children = [child for child in root.children if child.token['deprel'] == "conj"]

	# Check that it has children 
	if conjunct_children: 
		# Check that there is an "or" somewhere in the NP as well
		for secondconjunct in conjunct_children:
			for orchild in secondconjunct.children:
				if orchild.token['form'] == 'or':
					return(conjunct_children)
		
	return

def is_existential_construction(mainVerb): 
	for childNode in mainVerb.children: 
		if childNode.token['deprel'] == 'expl':
			return(True)
	return(False)

def get_main_aux(auxes):
	'''
	Takes a list of nodes, returns whichever appears right-most in the string. 
	For lists of auxiliaries, we expect this one to be the main aux: 
		E.g. "John may be in the room" --> (be) 
		E.g. "John may have had a pear" --> (had) 
	'''
	aux_index = 0 
	for aux in auxes: 
		if aux.token["id"] >aux_index:
			aux_index = aux.token["id"]
			verb = aux
	
	return(verb)
	

def processroot(root, sentence, extracted_examples):

    # Terminal node with no children, bottom out
	if len(root.children) == 0:
		return (extracted_examples)


	# Need to recurse for embedded clauses with disjuncted subjects (Alice knows that Bob or the students are in the room): 
	for child in root.children:
		extracted_examples = processroot(child, sentence, extracted_examples)

	
	is_predicate = True if root.token['upos'] in ('VERB', 'NOUN', 'PROPN', 'PRON') else False

	if is_predicate: 
		# The predicate of the sentence 
		# May not show agreement/be what we care about, e.g. 
		# John is in the room --> "room" is main predicate (we care about 'is')
		mainPredicate = root 

		
		for child in root.children:
			# Only extract if NSUBJ of the predicate includes disjuncted NPs
			conjuncts = disjuncted_NPs(child, sentence)
			
			if child.token['deprel'] == 'nsubj' and conjuncts: 
				
				# We are not yet interested in cases with more than 1 additional conjuncts, throw those away. 
				if len(conjuncts) >1: 
					logging.debug(f"Ignoring: sentence with 2 or more conjuncts \t {root.token['lemma']} \t {sentence}")
					return(extracted_examples)
				
				# If the predicate is a noun (like "John or the students are in the room"), find aux to get number agreement
				if root.token['upos'] in ('NOUN', 'PROPN', 'PRON'):
					auxes = list(filter(lambda x: x.token['upos'] == 'AUX' or x.token['upos'] == 'COP', root.children))
				
					## The case you expect: Single aux. That has the agreement features we care about, so make it the verb
					## E.g. John or mary are in the room 
					if len(auxes) == 1: 
						verb = auxes[0]
						
					## Sentences with more than one aux usually have a modal, so they won't show agreement 
					## E.g. John or Mary might be in the room. 
					
					elif len(auxes) > 1:
						## In such a case we expect the right-most to be the main one; extract it from the list 
						main_aux = get_main_aux(auxes)
						logging.debug(f"Ignoring: nominal predicate with too many auxiliaries (possible modal?) \t {main_aux.token['lemma']} \t {sentence}") 
						return(extracted_examples)
					## Sentences with no auxiliary but a nominal predicate have perhaps been misparsed; 
					## Log them them for future reference
					else: 
						logging.debug(f"Ignoring: nominal predicate with no auxiliary? \t predicate: {root.token['lemma']} \t {sentence}") 
						return(extracted_examples)
				
				# If the predicate is a verb, need to check for possible agreement blockers: 
				# Existential There (There are either lions or pandas at the zoo) 
				# Modals (John or Mary might go- the verb go will not agree in number to NSUBJ)
				else: 
					if is_existential_construction(root): 
						logging.debug(f"Ignoring: possible existential construction \t {root.token['lemma']} \t {sentence}")
						return(extracted_examples)

					auxes = list(filter(lambda x: x.token['upos'] == 'AUX' or x.token['upos'] == 'COP', root.children))

					## If no auxiliary, agreement features will be on the root/main verb. 
					## E.g. John or Mary go to the store  
					if len(auxes) == 0: 
						verb = root

					elif len(auxes) == 1: 
						# E.g. If there's just one aux and it's "have", "be", "do", this will have our agreement features
						## E.g. John or Mary have gone to the store / John or Mary has gone to the store. 
						## E.g. Cancellations or early departures due to weather do not warrant any refund of rent.
						if auxes[0].token['lemma'] == 'be' or auxes[0].token['lemma'] == 'have'  or auxes[0].token['lemma'] == 'do': 
							verb = auxes[0]
						# Otherwise, the aux is probably a modal and will block agreement
						# E.g John or Mary might go to the store 
						else: 
							logging.debug(f"Ignoring: main verb with possible modal auxiliary \t {root.token['lemma']} \t {sentence}") 
							return(extracted_examples)
						
					# If more than one auxiliary, probably includes at least one modal blocking agreement. 
					# E.g. John or Mary might be going to the store 
					elif len(auxes) >1: 
						logging.debug(f"Ignoring: main verb with too many auxiliaries (possible modal?) \t {root.token['lemma']} \t {sentence} ")
						return(extracted_examples)
					
				
				tense = verb.token['feats'].get('Tense', 'NO_TENSE') 
				if tense == 'Past':
					logging.debug(f"Ignoring: past-tense verb or aux \t {verb.token['lemma']} \t {sentence}")
					return(extracted_examples)


				has_either = np_includes_either(child, sentence) # True if dominating word "either"
				has_neither = np_includes_neither(child, sentence) # True if dominating word "neither"

				new_example = disjunctionExample(
					head_np = child, 
					conjuncts = conjuncts, 
					agreementCarrier = verb, 
					has_either = has_either, 
					has_neither = has_neither, 
					sentence = sentence, 
					mainPredicate = mainPredicate)
				extracted_examples.append(new_example)

	return(extracted_examples)


def process_file(file): 

	extracted_examples = []

	data_file = open(file, 'r', encoding = "utf-8")

	sentences = conllu.parse_tree_incr(data_file)
	for root in sentences:
		extracted_examples = processroot(root, root.metadata['text'], extracted_examples)
	return(extracted_examples)

def main(args): 
	for file in args.conllufiles: 
		
		filename = os.path.basename(file)

		logging.basicConfig(filename=args.outpath+'/' + Path(filename).stem + '_extraction.log', filemode = "w", level=logging.DEBUG, format='%(message)s')
		logging.basicConfig(level=logging.DEBUG, format='%(message)s')
		logger = logging.getLogger()
		
		# Open files, write headers 
		disjunction_examples_filepath = args.outpath+'/' + Path(filename).stem + "_extracted-disjunctions.tsv"
		disjunction_examples_file = open(disjunction_examples_filepath, 'w', newline ='')
		disjunction_examples_file.write("\t".join(["experiment_condition",
											"has_either",
											"has_neither",
											"conj_1_number",
											"conj_1_person",
											"conj_2_number",
											"conj_2_person",
											"nsubj",
											"verb_form",
											"verb_lemma",
											"verb_number",
											"main_predicate_lemma",
											"main_predicate_arc",
											"sentence",
											'filename',]) +"\n")
		
		total_extracted_examples = process_file(file)
		
		
		
		for example in total_extracted_examples: 
			disjunction_examples_file.write(str(example) + "\t" +filename + "\n")
			
			
		disjunction_examples_file.close()
	
		logging.info("process took %s %s", time.process_time(), 'seconds')

if __name__ == "__main__":
	# Run with e.g. "python extract_disjunctions.py disjunction_outputs/ test_short.conllu"
	# WARNING: If you pass multiple input files (conllufiles handles a list) will generate
	# one output file for each input file, and a single log file for the whole endeavour. 
	# the log file is named after the first input file in the list. 
    ARGPARSER = argparse.ArgumentParser() 
    ARGPARSER.add_argument('outpath', type = str)
    ARGPARSER.add_argument('conllufiles', nargs='+')
    args = ARGPARSER.parse_args()
    main(args)