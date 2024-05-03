import random, json

class pronoun:
  def __init__(self, agr, form):
    self.agr = agr
    self.form = form

p1S = pronoun("1S", "I")
p1P = pronoun("1P", "we")
p3S = pronoun("3S", "it")
p3P = pronoun("3P", "they")

pronouns = [p1S,p1P,p3S,p3P]
# random.shuffle(pronouns)

singletons = ["alien", "dog", "gamer", "octopus", "man", "woman", "neighbor", "landlord", "actor", "congressperson", "dancer", "model", "engineer", "writer", "librarian", "bookworm", "clown", "painter", "golfer", "composer", "singer", "salesperson", "student", "teacher", "chef", "doctor", "farmer", "astronaut", "journalist", "firefighter", "police officer", "plumber", "electrician", "athlete", "musician", "photographer", "scientist", "mechanic", "gardener", "curator", "waitress", "waiter", "nurse", "artist", "politician", "banker", "carpenter", "sailor", "pilot", "soldier", "spy", "coach", "diver", "explorer", "hunter", "magician", "miner", "rancher", "secretary", "therapist", "veterinarian", "zookeeper", "fisherman", "hiker", "surfer", "cyclist", "skateboarder", "rock climber", "mountaineer", "skier", "snowboarder", "biker", "teenager", "innkeeper", "door attendant", "emperor", "meteorologist", "bard", "warrior", "author", "protestor", "visitor", "bus driver", "translator"]
random.shuffle(singletons)
print(len(singletons))

plurals = ["sorcerers","actresses","fishers","programmers","ladies","attendants","dog trainers","graduates","candlemakers","shoemakers","workers","employees", "children","Martians","ghosts","mummies","lawyers", "wolves", "cooks", "performers", "acrobats", "astrologists", "bartenders", "employers", "butlers", "cashiers", "cartoonists", "clairvoyants", "diplomats", "florists", "humanitarians", "interpreters", "investors", "janitors", "jugglers", "knitters", "lifeguards", "manicurists", "millionaires", "novelists", "nutritionists", "orthodontists", "pharmacists", "pianists", "professors", "reporters", "runners", "sculptors", "screenwriters", "shoppers", "sunbathers", "tailors", "wrestlers", "zoologists", "taxidermists", "tattoo artists", "commanders", "interlopers", "zombies", "pedestrians", "palm readers", "jewelers", "informants", "hitchhikers", "gymnasts", "guards", "hairdressers", "fortune tellers", "realtors", "environmentalists", "detectives", "customers", "archaeologists", "newsboys", "stunt doubles", "villains", "graphic designers", "gameshow hosts", "museum curators", "technical writers", "security specialists", "bodyguards", "wedding planners", "maids"]

random.shuffle(plurals)
print(len(plurals))

vps = vps = ["going to the moon.", "eating the cake.", "dancing the Hula.", "calling for help.", "celebrating the team's win.", "running a marathon.", "building a house.", "playing the guitar.", "writing a novel.", "designing a website.", "baking cookies.", "traveling the world.", "painting a masterpiece.", "teaching a class.", "conducting an experiment.", "making a difference.", "helping others.", "solving a mystery.", "climbing a mountain.", "exploring the ocean depths.", "learning a new language.", "starting a business.", "saving the day.", "inspiring others.", "asking for assistance.", "running the meeting.", "winning the tournament.", "watching the movie.", "going to the beach.", "ordering more paella.", "preheating the oven.", "running for public office.", "hitting the jackpot.", "visiting the capital of Lithuania.", "fixing the car.", "helping their team win.", "attending the conference in Azerbaijan.", "giving away free donuts.", "writing a self-help book.", "investing in cryptocurrency.", "reading the latest Stephen King novel.", "writing a review of the circus performance.", "learning how to ride a bike.", "voting in favor of the proposition.", "attending a lecture on Jane Austen.", "dancing the macarena.", "moving to Nairobi.", "administering the exam.", "grading the term papers.", "laying the house's foundation.", "building the Lego set.", "dancing in Saturday's recital.", "building homes for the unhoused.", "sunbathing on the beach.", "camping in the Redwood forest.", "hiking the Pacific trail.", "drinking copious amounts of lemonade.", "debating morality with the guru.", "asking for more coffee.", "ordering for the table.", "hitchhiking to British Columbia.", "adopting a family of kittens.", "touring the San Diego Zoo.", "pleading with the Prime Minister.", "arguing with the forest nymphs.", "listening to the tale of Odysseus.", "beginning to believe in luck.", "feeling guilty for lying.", "celebrating World Rivers Day.", "signing up for karaoke.", "making a toy at Build-A-Bear.", "cleaning the inside of the oven.", "looking for the meaning of life.", "dominating in League of Legends.", "listening to Taylor's new album.", "writing an original song about breakup.", "working on the puzzle.", "getting ready for the show.", "trying to remember the capital of Australia.", "petting the cat.", "making a hearty stew.", "objecting to the wedding.", "going grocery shopping.", "hosting the party.", "welcoming the guests.", "crying in the club."]

random.shuffle(vps)
print(len(vps))

class sentence: 
    def __init__(self, id, conj1, conj2, predicate, text, conj1_num, conj2_num, conj1_per, conj2_per, dataType, cond):
        self.id = id
        self.conj1 = conj1
        self.conj2 = conj2
        self.predicate = predicate
        self.text = text
        self.conj1_num = conj1_num
        self.conj2_num = conj2_num
        self.conj1_per = conj1_per
        self.conj2_per = conj2_per
        self.dataType = dataType
        self.cond =  cond


introText = "Either "
# det = "the "
disjunctive = " or "
entry = r" %is,are,am% "

stimList = []
stimCount = 0

for x in range(6):
    for i in pronouns:
        for i2 in pronouns:
            selection1 = i
            selection2 = i2
            if selection1.form == "it":
                conj1 = "the "+singletons.pop()
                conj1_num = "S"
                conj1_per = "3"
            elif selection1.form == "they":
                conj1 = "the "+plurals.pop()
                conj1_num = "P"
                conj1_per = "3"
            else:
                conj1 = selection1.form
                conj1_per = "1"
                if conj1 == "I":
                    conj1_num = "S"
                else: 
                    conj1_num = "P"
            if selection2.form == "it":
                conj2 = "the "+singletons.pop()
                conj2_num = "S"
                conj2_per = "3"
            elif selection2.form == "they":
                conj2 = "the "+plurals.pop()
                conj2_num = "P"
                con2_per = "3"
            else:
                conj2 = selection2.form
                conj2_per = "1"
                if conj2 == "I":
                    conj2_num = "S"
                else: 
                    conj2_num = "P"
            if conj1 != conj2:
                stimCount += 1
                predicate = vps.pop()
                stim = sentence(
                    conj1 = conj1,
                    conj2 = conj2,
                    predicate = predicate,
                    text = introText+conj1+disjunctive+conj2+entry+predicate,
                    conj1_num = conj1_num,
                    conj2_num = conj2_num,
                    conj1_per = conj1_per,
                    conj2_per = conj2_per,
                    id = stimCount,
                    dataType = "critical",
                    cond = conj1_per+conj1_num+"_or_"+conj2_per+conj2_num
                )
                if stim.conj1 != stim.conj2:
                    stimList.append(stim)


random.shuffle(stimList)

print(stimList[0].text)
print(stimList[0].conj1_per)
print(stimList[0].conj1_num)
print(stimList[0].conj2_per)
print(stimList[0].conj2_num)

# Defining Fillers

names = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", "Henry", "Ivy", "Jack", "Katherine", "Liam", "Mia", "Nora", "Oliver", "Penelope", "Quinn", "Ryan", "Sophia", "Thomas", "Uma", "Victor", "Wendy", "Xavier", "Yaryn", "Zachary", "Amelia", "Benjamin", "Chloe", "Daniel", "Ella", "Finn", "Georgia", "Hannah", "Isaac", "Jasmine", "Kevin", "Lily", "Mason", "Natalie", "Oscar", "Paige", "Quentin", "Rebekah", "Samuel", "Tiffany", "Ulysses", "Violet", "William", "Xander", "Yvonne", "Zara", "Aaron", "Bella", "Caleb", "Diana", "Ethan", "Faith", "Gabriel", "Holly", "Isabel", "Jacob", "Kylie", "Luna", "Matthew", "Naomi", "Olive", "Peter", "Quincy", "Rachel", "Samantha", "Tristan", "Ursula", "Vincent", "Willa", "Xena", "Yolanda", "Zane", "Ava", "Brian", "Cora", "Dylan", "Emily", "Gavin", "Hazel", "Isla", "James", "Kayla", "Logan", "Madison", "Noah", "Olivia", "Patrick", "Quinn", "Rose", "Simon", "Taylor", "Ursula", "Vanessa", "Wyatt", "Ximena", "Yasmine", "Zoe"]
random.shuffle(names)

activities = ["skydiving from 10,000 feet.", "sculpting a masterpiece from clay.", "trekking through the Amazon rainforest.", "designing a sustainable city.", "solving a Rubik's cube blindfolded.", "volunteering at an animal sanctuary.", "sailing across the Atlantic Ocean.", "performing stand-up comedy at an open mic.", "planting a community garden.", "mentoring underprivileged youth.", "organizing a charity fundraiser.", "restoring a vintage car.", "completing a triathlon.", "launching a podcast about astrophysics.", "building a treehouse in the backyard.", "documenting a cross-country road trip.", "training for a martial arts tournament.", "participating in a scientific expedition to Antarctica.", "creating an app for mental health awareness.", "choreographing a dance for a flash mob.", "writing a screenplay for a sci-fi movie.", "hosting a cooking class for beginners.", "starting a YouTube channel about DIY home improvement.", "volunteering at a homeless shelter.", "learning to play the violin.", "studying quantum mechanics.", "developing a permaculture farm.", "collaborating on a research paper about renewable energy.", "restoring coral reefs in the Pacific Ocean.", "joining a community theater production.", "backpacking through Europe.", "training for a marathon.", "building a tiny house on wheels.", "painting a mural in a public space.", "starting a book club for young readers.", "organizing a beach cleanup.", "training a service dog.", "creating a wildlife documentary.", "hosting a virtual reality gaming tournament.", "learning American Sign Language.","trying to get into the club.", "studying for a world history test.", "painting a mural about sustainability.", "participating in a protest.", "riding a motorcycle"]
random.shuffle(activities)

plurals2 = ["sorcerers","actresses","fishers","programmers","ladies","attendants","dog trainers","graduates","candlemakers","shoemakers","workers","employees", "children","Martians","ghosts","mummies","lawyers", "wolves", "cooks", "performers", "acrobats", "astrologists", "bartenders", "employers", "butlers", "cashiers", "cartoonists", "clairvoyants", "diplomats", "florists", "humanitarians", "interpreters", "investors", "janitors", "jugglers", "knitters", "lifeguards", "manicurists", "millionaires", "novelists", "nutritionists", "orthodontists", "pharmacists", "pianists", "professors", "reporters", "runners", "sculptors", "screenwriters", "shoppers", "sunbathers", "tailors", "wrestlers", "zoologists", "taxidermists", "tattoo artists", "commanders", "interlopers", "zombies", "pedestrians", "palm readers", "jewelers", "informants", "hitchhikers", "gymnasts", "guards", "hairdressers", "fortune tellers", "realtors", "environmentalists", "detectives", "customers", "archaeologists", "newsboys", "stunt doubles", "villains", "graphic designers", "gameshow hosts", "museum curators", "technical writers", "security specialists", "bodyguards", "wedding planners", "maids"]
random.shuffle(plurals2)


coin = ["heads", "tails", "underbelly"]

for i in range(40):
    coinflip = random.choice(coin)
    if coinflip == "heads":
        conj1 = names.pop()
        conj2 = "null"
        predicate = activities.pop()
        stim = sentence(
            conj1 = conj1,
            conj2 = "null",
            predicate = predicate,
            text = conj1+r" %is,are,am% "+predicate,
            conj1_num = "S",
            conj2_num = "null",
            conj1_per = "3",
            conj2_per = "null",
            id = stimCount,
            dataType = "filler",
            cond = "3S"
        )
    elif coinflip == "tails":
        conj1 = names.pop()
        conj2 = names.pop()
        predicate = activities.pop()
        stim = sentence(
            conj1 = conj1,
            conj2 = conj2,
            predicate = predicate,
            text = conj1+" and "+conj2+r" %is,are,am% "+predicate,
            conj1_num = "S",
            conj2_num = "S",
            conj1_per = "3",
            conj2_per = "3",
            id = stimCount,
            dataType = "filler",
            cond = "3S3S"
        )
    elif coinflip == "underbelly":
        conj1 = plurals2.pop()
        conj2 = "null"
        predicate = activities.pop()
        stim = sentence(
            conj1=conj1,
            conj2=conj2,
            predicate = predicate,
            text = "The "+conj1+r" %is,are,am% "+predicate,
            conj1_num="P",
            conj1_per="3",
            conj2_num="null",
            conj2_per="null",
            id=stimCount,
            dataType="filler",
            cond="3P"
        )
    stimCount += 1
    stimList.append(stim)


jsonList = [stim.__dict__ for stim in stimList]
print(len(jsonList))

with open('output.json', 'w') as file:
    json.dump(jsonList, file, indent=4)
