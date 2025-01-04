import stanza
sentences = [
    # "Either John or Mary goes to the store", # KEEP: lexical verb, no aux, SS Sing
    # "Either John or Mary go to the store", # KEEP: lexical verb, no aux, SS Plur
    # "Either John or Mary will go to the store", # JUNK: Lexical verb with modal
    # "Either John or Mary have gone to the store", # KEEP: lexical verb with 'have' aux,  SS Plur
    # "Either John or Mary has gone to the store",  # KEEP: lexical verb with 'have' aux,  SS Sing
    # "Either John or Mary are in the room",  # KEEP: Nominal predicate, 'be' aux SS Plur
    # "Either John or Mary is in the room.", # KEEP: Nominal predicate, 'be' aux SS Sing
    # "Either John or Mary might be in the room.", #JUNK: nominal predicate with modal 
    # "She knew that John or Mary were in the room.", #KEEP: nominal predicate, 'be' aux, SS Plur
    # "She knew that there were lions or pandas in the room", #JUNK: existential 
    # "She or the students know about this", # KEEP: lexical verb, no modal, SP Plural
    # "She or the students knows about this", # KEEP: lexical verb, no modal, SP Sing 
    # "I or the students know about this", # KEEP: lexical verb, no modal, SP Plural [1st, 3rd]person
    # "Cancellations or early departures due to inclement weather do not warrant any refund of rent.",
    "a death extract would be included in the supplemental documents as the widow or widower had to prove she or he was free to marry again.",
    "The original limestone house consisted of three rooms in an L-shape with a summer kitchen or porch filling in the square", # VerbForm=Ger 
    "Don’t wait for a random referral, review, or testimonial to come your way.",


]

nlp = stanza.Pipeline("en")

for sentence in sentences: 
    print("{:C}".format(nlp(sentence)))