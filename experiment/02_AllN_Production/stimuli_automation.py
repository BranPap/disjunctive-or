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

singletons = ["alien", "dog", "gamer", "octopus", "man", "woman", "neighbor", "landlord", "actor", "congressperson", "dancer", "model", "engineer", "writer", "librarian", "bookworm", "clown", "painter", "golfer", "composer", "singer", "salesperson", "student", "teacher", "chef", "doctor", "farmer", "astronaut", "journalist", "firefighter", "police officer", "plumber", "electrician", "athlete", "musician", "photographer", "scientist", "mechanic", "gardener", "curator", "waitress", "waiter", "nurse", "artist", "politician", "banker", "carpenter", "sailor", "pilot", "soldier", "spy", "coach", "diver", "explorer", "hunter", "magician", "miner", "rancher", "secretary", "therapist", "veterinarian", "zookeeper", "fisherman", "hiker", "surfer", "cyclist", "skateboarder", "rock climber", "mountaineer", "skier", "snowboarder", "biker"]

random.shuffle(singletons)
# print(len(singletons))

plurals = ["sorcerers","actresses","fishers","programmers","ladies","attendants","dog trainers","graduates","candlemakers","shoemakers","workers","employees", "children","Martians","ghosts","mummies","lawyers", "wolves", "cooks", "performers", "acrobats", "astrologists", "bartenders", "employers", "butlers", "cashiers", "cartoonists", "clairvoyants", "diplomats", "florists", "humanitarians", "interpreters", "investors", "janitors", "jugglers", "knitters", "lifeguards", "manicurists", "millionaires", "novelists", "nutritionists", "orthodontists", "pharmacists", "pianists", "professors", "reporters", "runners", "sculptors", "screenwriters", "shoppers", "sunbathers", "tailors", "wrestlers", "zoologists", "taxidermists", "tattoo artists", "commanders", "interlopers", "zombies", "pedestrians", "palm readers", "jewelers", "informants", "hitchhikers", "gymnasts", "guards", "hairdressers", "fortune tellers", "realtors", "environmentalists", "detectives", "customers"]

random.shuffle(plurals)
# print(len(plurals))

vps = vps = ["going to the moon.", "eating the cake.", "dancing the Hula.", "calling for help.", "celebrating the team's win.", "running a marathon.", "building a house.", "playing the guitar.", "writing a novel.", "designing a website.", "baking cookies.", "traveling the world.", "painting a masterpiece.", "teaching a class.", "conducting an experiment.", "making a difference.", "helping others.", "solving a mystery.", "climbing a mountain.", "exploring the ocean depths.", "learning a new language.", "starting a business.", "saving the day.", "inspiring others.", "asking for assistance.", "running the meeting.", "winning the tournament.", "watching the movie.", "going to the beach.", "ordering more paella.", "preheating the oven.", "running for public office.", "hitting the jackpot.", "visiting the capital of Lithuania.", "fixing the car.", "helping their team win.", "attending the conference in Azerbaijan.", "giving away free donuts.", "writing a self-help book.", "investing in cryptocurrency.", "reading the latest Stephen King novel.", "writing a review of the circus performance.", "learning how to ride a bike.", "voting in favor of the proposition.", "attending a lecture on Jane Austen.", "dancing the macarena.", "moving to Nairobi.", "administering the exam.", "grading the term papers.", "laying the house's foundation.", "building the Lego set.", "dancing in Saturday's recital.", "building homes for the unhoused.", "sunbathing on the beach.", "camping in the Redwood forest.", "hiking the Pacific trail.", "drinking copious amounts of lemonade.", "debating morality with the guru.", "asking for more coffee.", "ordering for the table.", "hitchhiking to British Columbia.", "adopting a family of kittens.", "touring the San Diego Zoo.", "pleading with the Prime Minister.", "arguing with the forest nymphs.", "listening to the tale of Odysseus.", "beginning to believe in luck.", "feeling guilty for lying.", "celebrating World Rivers Day.", "signing up for karaoke.", "making a toy at Build-A-Bear.", "cleaning the inside of the oven."]

random.shuffle(vps)
print(len(vps))

class sentence: 
    def __init__(self, id, conj1, conj2, predicate, text, conj1_num, conj2_num, conj1_per, conj2_per, dataType):
        self.id = id
        self.conj1 = conj1
        self.conj2 = conj2
        self.predicate = predicate
        self.text = text
        self.conj1_num = conj1_num
        self.conj2_num = conj2_num
        self.conj1_per = conj1_per
        self.conj2_per = conj2_per
        dataType = "critical"

introText = "Either "
# det = "the "
disjunctive = " or "
entry = r" %is,are,am% "

stimList = []
stimCount = 0

for x in range(5):
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
                    dataType = "critical"
                )
                if stim.conj1 != stim.conj2:
                    stimList.append(stim)


random.shuffle(stimList)

print(stimList[0].text)
print(stimList[0].conj1_per)
print(stimList[0].conj1_num)
print(stimList[0].conj2_per)
print(stimList[0].conj2_num)

jsonList = [stim.__dict__ for stim in stimList]
json_file_path = "unique_stims.json"


with open('output.json', 'w') as file:
    json.dump(jsonList, file, indent=4)
