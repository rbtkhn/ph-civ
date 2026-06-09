"""Pilot: proper-noun normalization for civ-01 through civ-12 transcripts."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

SHARED_ARCHAEOLOGY = [
    ("go tape", "Gobekli Tepe"),
    ("go goe", "Gobekli Tepe"),
    ("Kaya Hoak", "Catalhoyuk"),
    ("katah Hoak", "Catalhoyuk"),
    ("K Hoak", "Catalhoyuk"),
    ("kah Hoak", "Catalhoyuk"),
    ("kah holak", "Catalhoyuk"),
    ("kind of holak", "Catalhoyuk"),
    ("kind of Hoya", "Catalhoyuk"),
    ("kind of Hoak", "Catalhoyuk"),
    ("go bye", "Gobekli Tepe"),
    ("like goe and", "like Gobekli Tepe and"),
    ("is goe and", "is Gobekli Tepe and"),
    ("this is goe and", "this is Gobekli Tepe and"),
    ("place like goe and", "place like Gobekli Tepe and"),
]


def repair_goes_corruption(text: str) -> str:
    """Undo false positives where bare goe matched the ``goes`` substring."""
    return text.replace("Gobekli Tepes", "goes")


def apply_reps(text: str, reps: list[tuple[str, str]]) -> str:
    for old, new in reps:
        text = text.replace(old, new)
    return repair_goes_corruption(text)


def normalize_civ01(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("yuel Harari", "Yuval Harari"),
        (" sapen ", " Sapiens "),
        ("champanes", "chimpanzees"),
        ("Bol BS", "bonobos"),
        (" uh chenes ", " chimpanzees "),
        ("confusious", "Confucius"),
        ("naian culture", "Natufian culture"),
        ("the naian culture", "the Natufian culture"),
        ("tafan culture", "Natufian culture"),
        ("porion while", "for coercion, while"),
        ("cotion", "coercion"),
        ("cion and", "coercion and"),
        ("that's cion", "that's coercion"),
        ("group bual", "group burial"),
        ("Bob who", "bonobos who"),
        ("Tower of jerle", "Tower of Jericho"),
        ("Jero went", "Jericho went"),
        ("5% of tee", "5% of Gobekli Tepe"),
        ("Jericho and um kak", "Jericho and Catalhoyuk"),
        ("kolak", "Catalhoyuk"),
        ("Kaho", "Catalhoyuk"),
    ]
    return apply_reps(text, reps)


def normalize_civ02(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("alar Spain", "Altamira, Spain"),
        ("Emmanuel Kant", "Immanuel Kant"),
        ("Emanuel Khan", "Immanuel Kant"),
        ("uel Kant", "Immanuel Kant"),
        ("neither is ratal an isolated case", "neither is this an isolated case"),
        ("from the pic okay meaning Ice Age", "from the Ice Age"),
        ("balance of apprais", "broad surveys"),
    ]
    return apply_reps(text, reps)


def normalize_civ03(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("homoa sapiens", "Homo sapiens"),
        ("peaceful otan and artistic", "peaceful egalitarian and artistic"),
        ("yamaya came", "Yamnaya came"),
        ("ShaManichaeism", "shamanism"),
        ("animal BS", "animal bones"),
        ("proper trute", "proper tribute"),
        ("way Davis", "Wade Davis"),
        ("Army ANS invade", "army ants invade"),
    ]
    return apply_reps(text, reps)


def normalize_civ04(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("skeletons of the yayah", "skeletons of the Yamnaya"),
        ("the yayah people", "the Yamnaya people"),
        ("burials of the yayah people", "burials of the Yamnaya people"),
        ("yayah people", "Yamnaya people"),
        ("conquest of the yayah", "conquest of the Yamnaya"),
        ("called the yaya um", "called the Yamnaya um"),
        ("time of the yaya about", "time of the Yamnaya about"),
        ("who the yah were", "who the Yamnaya were"),
        ("Maria gambas", "Marija Gimbutas"),
        ("Maria gbas", "Marija Gimbutas"),
        ("Mar G said", "Marija Gimbutas said"),
        ("Maria gutas", "Marija Gimbutas"),
        ("until 20200 BC", "until 2200 BC"),
    ]
    return apply_reps(text, reps)


def normalize_civ05(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("he got atarian", "egalitarian"),
        ("who are the yamaya", "who are the Yamnaya"),
        ("the yanah okay", "the Yamnaya okay"),
        ("the yanah people", "the Yamnaya people"),
        ("yanah people", "Yamnaya people"),
        ("confusious", "Confucius"),
        ("came from that period laa okay", "came from that period Laozi okay"),
        ("the tun of China", "the Spring and Autumn period of China"),
        ("hedgemon", "hegemon"),
        ("aent of the great", "Alexander the Great"),
        ("before theah humans", "before the Yamnaya humans"),
        ("groups of yah okay", "groups of Yamnaya okay"),
        ("the yayah", "the Yamnaya"),
    ]
    return apply_reps(text, reps)


def normalize_civ06(text: str) -> str:
    reps = SHARED_ARCHAEOLOGY + [
        ("the bran age collapse", "the Bronze Age collapse"),
        ("bran age collapse", "Bronze Age collapse"),
        ("during the bran age there", "during the Bronze Age there"),
        ("bran H collapse", "Bronze Age collapse"),
        ("branch it collapse", "Bronze Age collapse"),
        ("branchage collapse", "Bronze Age collapse"),
        ("masan Greece", "Mycenaean Greece"),
        ("m and Greece", "Mycenaean Greece"),
        ("the M gree", "the Mycenaean"),
        ("across the agan SE", "across the Aegean Sea"),
        ("the agan SE", "the Aegean Sea"),
        ("this is the agent is what we call", "this is what we call"),
        ("hedgemon", "hegemon"),
        ("Force fire", "forest fire"),
        ("force fire", "forest fire"),
        ("highte Empire", "Hittite Empire"),
        ("hiat Empire", "Hittite Empire"),
        ("the high ties", "the Hittites"),
        ("the hitit", "the Hittite"),
        ("place called Canaan", "place called Canaan"),
        ("place called canine", "place called Canaan"),
        ("canine is important", "Canaan is important"),
        ("so canine today", "so Canaan today"),
        ("Canan is", "Canaan is"),
        ("though canine disappeared", "though Canaan disappeared"),
        ("for Mason and Greece", "for Mycenaean Greece"),
        ("Cyprus and Cit", "Cyprus and Crete"),
        ("Maia Greece", "Mycenaean Greece"),
        ("must in Greece", "Mycenaean Greece"),
        ("destroy the masan Greece", "destroy Mycenaean Greece"),
        ("theory of the per", "theory of the perfect"),
        ("Peter Turin", "Peter Turchin"),
        ("Peter turchin", "Peter Turchin"),
        ("Peter turon's", "Peter Turchin's"),
        ("KL marks", "Karl Marx"),
        ("KARK says", "Karl Marx says"),
        ("KL Marx", "Karl Marx"),
        ("we do Samaria Samaria", "we do Sumeria"),
        ("rcking behavior", "rent-seeking behavior"),
        ("reding Behavior", "rent-seeking behavior"),
        ("engage in reding", "engage in rent-seeking"),
        ("collapsed m in gree", "collapsed Mycenaean Greece"),
        ("branch age collapsed m in gree", "Bronze Age collapsed Mycenaean Greece"),
    ]
    return apply_reps(text, reps)


def normalize_civ07(text: str) -> str:
    reps = [
        ("faciiities", "Thucydides"),
        ("fiddies", "Thucydides"),
        ("reading forties will", "reading Thucydides will"),
        ("when forties when", "when Thucydides when"),
        ("mean Greece", "Mycenaean Greece"),
        ("the means controlled", "the Mycenaeans controlled"),
        ("branchage collapse", "Bronze Age collapse"),
        ("Bron AG collapse", "Bronze Age collapse"),
        ("because of R collapse", "because of Bronze Age collapse"),
        ("thousands of policies around Greece", "thousands of poleis around Greece"),
        ("the Polish any questions", "the polis, any questions"),
        ("in this polish and", "in this polis and"),
        ("these Poes were", "these poleis were"),
        ("against other polies", "against other poleis"),
        ("in Egypt and in Samaria", "in Egypt and in Sumer"),
        ("the wunning system", "the writing system"),
        ("sang okay Ro Romans are three kingdoms", "Romance of the Three Kingdoms"),
        ("the children War", "the Trojan War"),
        ("story of the children war", "story of the Trojan War"),
        ("children Army", "Trojan army"),
        ("children are slaughtered", "Trojans are slaughtered"),
        ("goddess is apod", "goddess is Aphrodite"),
        ("Hera apina or", "Hera, Athena, or"),
        ("named o disas", "named Odysseus"),
        ("when you read thead", "when you read the Iliad"),
        ("with the ilad", "with the Iliad"),
        ("unique to the ilad", "unique to the Iliad"),
        ("in the ilad", "in the Iliad"),
        ("the ilot starts", "the Iliad starts"),
        ("shocking about daad", "shocking about the Iliad"),
        ("that's the that's the ilc", "that's the Iliad"),
        ("King prome", "King Priam"),
        ("prum is", "Priam is"),
        ("egam Manon", "Agamemnon"),
        ("aanon the King", "Agamemnon the King"),
        ("you're your dog eanon", "you're your dog Agamemnon"),
        ("Egon could", "Agamemnon could"),
        ("achilles", "Achilles"),
        ("achillus", "Achilles"),
        ("ailles", "Achilles"),
        ("his friend Petrus", "his friend Patroclus"),
        ("Petrus is", "Patroclus is"),
        ("killing Petrus", "killing Patroclus"),
        ("Hector kills Petras", "Hector kills Patroclus"),
        ("kills Petras", "kills Patroclus"),
        ("death of fas", "death of Patroclus"),
        ("friend petas died", "friend Patroclus died"),
        ("Prim doesn't", "Priam doesn't"),
        ("Prime instead", "Priam instead"),
        ("admires PR's", "admires Priam's"),
        ("body to prum", "body to Priam"),
        ("King pram", "King Priam"),
        ("the phans connected", "the Phoenicians connected"),
        ("confusion Scholars", "Confucian scholars"),
        ("confusion thought", "Confucian thought"),
        ("the pipan war", "the Peloponnesian War"),
        ("guess what forties when", "guess what Thucydides when"),
        ("polus", "polis"),
        ("poll is", "polis is"),
        ("Pol is", "polis is"),
    ]
    text = apply_reps(text, reps)
    return text.replace("polisis", "polis is")


SHARED_HELLENIC = [
    ("hedgemon", "hegemon"),
    ("stAttalus quo", "status quo"),
    ("psychotic dialogue", "Socratic dialogue"),
    ("achronic dialogue", "Socratic dialogue"),
    ("hubis", "hubris"),
    ("huus", "hubris"),
    ("polus", "polis"),
    ("polist", "poleis"),
    ("polies", "poleis"),
    ("the pois okay", "the poleis okay"),
    ("focusing on the pois", "focusing on the poleis"),
    ("Greek pois", "Greek poleis"),
    ("other Greek pois", "other poleis"),
    ("banished from your polish", "banished from your polis"),
    (" PO system", " polis system"),
    ("P pelian War", "Peloponnesian War"),
    ("pelian War", "Peloponnesian War"),
    ("pelan war", "Peloponnesian War"),
    ("palpan war", "Peloponnesian War"),
    ("palan War", "Peloponnesian War"),
    ("the pan war", "the Peloponnesian War"),
    ("pelan", "Peloponnese"),
    ("peles", "Peloponnese"),
    ("bronch age", "Bronze Age"),
    ("m in gree", "Mycenaean Greece"),
    ("Myan gree", "Mycenaean Greece"),
    ("Ming and Greece", "Mycenaean Greece"),
    ("masine period", "Mycenaean period"),
    ("egam Menon", "Agamemnon"),
    ("EG Manon", "Agamemnon"),
    ("egam Manon", "Agamemnon"),
    ("eanon", "Agamemnon"),
    ("Egon", "Agamemnon"),
    ("the children War", "the Trojan War"),
    ("children war", "Trojan War"),
    ("children woman", "Trojan Women"),
    ("children Army", "Trojan army"),
    ("children are slaughtered", "Trojans are slaughtered"),
    ("children men", "Trojan men"),
    ("paricles", "Pericles"),
    ("Peres", "Pericles"),
    ("perally", "Pericles"),
    ("Perle", "Pericles"),
    ("daan League", "Delian League"),
    ("Delan league", "Delian League"),
    ("delan league", "Delian League"),
    ("dlan league", "Delian League"),
    ("parnon", "Parthenon"),
    ("paron", "Parthenon"),
    ("thermop pil", "Thermopylae"),
    ("thermop P", "Thermopylae"),
    ("HPP lights hopl lights", "hoplites"),
    ("hopl lights", "hoplites"),
    ("hoplin", "hoplon"),
    ("phing formation phic", "phalanx formation"),
    ("Macedonas", "Mardonius"),
    ("mardones", "Mardonius"),
    ("ptia", "Plataea"),
    ("greatek Navy", "Greek Navy"),
    ("Virgin Navy", "Persian Navy"),
    ("from mexic did", "Themistocles did"),
    ("set by fames", "sent by Themistocles"),
    ("his name is f f f", "his name is Themistocles"),
    ("half Nots", "have-nots"),
    ("P petite B", "petite bourgeoisie"),
    ("G as Khan", "Genghis Khan"),
    ("helenistic", "Hellenistic"),
    ("helenic world", "Hellenic world"),
    ("helenic Empire", "Hellenistic Empire"),
    ("Mason was", "Macedon was"),
    ("macona has", "Macedon has"),
    ("macona", "Macedon"),
    ("parmenion", "Parmenion"),
    ("Alexander the greate", "Alexander the Great"),
    ("EX life", "Alexander's life"),
    ("IllIllIllyria", "Illyria"),
    ("polares", "poleis"),
    ("play rights", "playwrights"),
]


def normalize_hellenic(text: str, extra: list[tuple[str, str]] | None = None) -> str:
    text = apply_reps(text, SHARED_HELLENIC + (extra or []))
    return text.replace("polisis", "polis is")


def normalize_civ08(text: str) -> str:
    reps = [
        ("so many Hots okay", "so many helots okay"),
        ("for every one hot sorry", "for every one helot sorry"),
        ("10 Hots Spartan", "10 helots Spartan"),
        ("control the hots", "control the helots"),
        ("some Hots would break Khufu", "some helots would break curfew"),
        ("spawning young man", "Spartan young man"),
        ("a hellot be", "a helot be"),
        ("the hots to prevent", "the helots to prevent"),
        ("many Hots and the SP were", "many helots and the Spartans were"),
        ("the spars were", "the Spartans were"),
        ("the spaans were", "the Spartans were"),
        ("the spers really", "the Spartans really"),
        ("what are the spers", "what are the Spartans"),
        ("the hots remember", "the helots remember"),
        ("10 hots for everyone", "10 helots for everyone"),
        ("the hots hate", "the helots hate"),
        ("the HS would run", "the helots would run"),
        ("let the hots run", "let the helots run"),
        ("the hels are going", "the helots are going"),
        ("aens has two", "Athens has two"),
        ("aens is a democracy", "Athens is a democracy"),
        ("Spartan aens are", "Spartan Athenians are"),
        ("but aens has", "but Athens has"),
        ("Healy but the Healy", "hilly but the hilly"),
        ("achilles", "Achilles"),
        ("yonia", "eudaimonia"),
        ("OST ostracized", "ostracism"),
        ("the aan", "the Aegean"),
        ("the agan", "the Aegean"),
        ("Ians versus", "Athenians versus"),
        ("the PES were", "the Persians were"),
        ("use calry", "use cavalry"),
        ("Greek Poes", "Greek poleis"),
        ("concept of aus", "concept of the polis"),
        ("the benedic King", "the benevolent King"),
        ("King xeres", "King Xerxes"),
        ("King Xerxes", "King Xerxes"),
        ("sell around", "sail around"),
        ("they sell off", "they sail off"),
        ("sell off West", "sail off West"),
        ("king xeres", "King Xerxes"),
        ("per comes into power", "Pericles comes into power"),
        ("those who criticized Pericles were now exiled from a therefore Peres", "those who criticized Pericles were now exiled from Athens therefore Pericles"),
        ("Greek puses", "Greek poleis"),
        ("Greek poets had", "Greek poleis had"),
        ("Sparta was the hedgemon sparta", "Sparta was the hegemon Sparta"),
        ("including the hots belong", "including the helots belong"),
        ("the hots so they", "the helots so they"),
        ("control over the hots", "control over the helots"),
        ("the hots to be slaves", "the helots to be slaves"),
        ("want the hots to be", "want the helots to be"),
        ("fre the hots", "free the helots"),
        ("the hots if you", "the helots if you"),
        ("hot if you fight", "helot if you fight"),
        ("lot of Hots fight", "lot of helots fight"),
        ("what the spars could", "what the Spartans could"),
        ("so what the spars", "so what the Spartans"),
        ("defeat the bamus", "defeat the barbarians"),
        ("Playdoh um socres aoso", "Plato, Socrates, Aristotle"),
    ]
    return normalize_hellenic(text, reps)


def normalize_civ09(text: str) -> str:
    reps = [
        ("chence newspaper", "Chinese newspaper"),
        ("Festival of dionis", "Festival of Dionysus"),
        ("dionis was the god", "Dionysus was the god"),
        ("Festival of dianis", "Festival of Dionysus"),
        ("festival Dianes", "festival Dionysus"),
        ("fesal of dines", "festival of Dionysus"),
        ("Festival of dianis", "Festival of Dionysus"),
        ("were Isis um sopes and Europe", "were Aeschylus, Sophocles, and Euripides"),
        ("europees okay", "Euripides okay"),
        ("talk about issus okay", "talk about Aeschylus okay"),
        ("play called oresa", "play called Oresteia"),
        ("plot of the Ora", "plot of the Oresteia"),
        ("so therea um", "so the Oresteia um"),
        ("called Aros and", "called Argos and"),
        ("collaps Ming in", "collapse meant in"),
        ("iselis is a profit", "Aeschylus is a prophet"),
        ("iselis", "Aeschylus"),
        ("issist sopes", "Aeschylus, Sophocles"),
        ("sop sopes", "Sophocles"),
        ("sop wrote", "Sophocles wrote"),
        ("edus trilogy", "Oedipus trilogy"),
        ("edus Trilogy", "Oedipus Trilogy"),
        ("named him edus", "named him Oedipus"),
        ("edus grows", "Oedipus grows"),
        ("edus freaks", "Oedipus freaks"),
        ("edus volunteers", "Oedipus volunteers"),
        ("edus now the king", "Oedipus now the king"),
        ("what edus does", "what Oedipus does"),
        ("edus Rex", "Oedipus Rex"),
        ("the idus", "the Oedipus"),
        ("pois polyes", "Polynices"),
        ("polyus who rebelled", "Polynices who rebelled"),
        ("polyus who", "Polynices who"),
        ("cron who is", "Creon who is"),
        ("cron finds", "Creon finds"),
        ("cron says", "Creon says"),
        ("Kan on says", "Creon says"),
        ("Kanon says", "Creon says"),
        ("integnity", "Antigone"),
        ("integy", "Antigone"),
        ("integon", "Antigone"),
        ("antagony", "Antigone"),
        ("anany", "Antigone"),
        ("hymon", "Haemon"),
        ("himon", "Haemon"),
        ("yides was", "Euripides was"),
        ("ubid he", "Euripides he"),
        ("Yus got", "Euripides got"),
        ("Ides are", "Euripides are"),
        ("Ides is", "Euripides is"),
        ("Ides was", "Euripides was"),
        ("Ides he", "Euripides he"),
        ("ues is", "Euripides is"),
        ("Europe is", "Euripides is"),
        ("god named diis", "god named Dionysus"),
        ("diis another", "Dionysus another"),
        ("diis is bakas", "Dionysus is Bacchus"),
        ("worship dianis", "worship Dionysus"),
        ("dianis The Legend", "Dionysus The Legend"),
        ("including diis but", "including Dionysus but"),
        ("refus to worship dianis", "refuse to worship Dionysus"),
        ("diis is worshiped", "Dionysus is worshiped"),
        ("dianis has always", "Dionysus has always"),
        ("worship of dianis", "worship of Dionysus"),
        ("dianis the wanderer", "Dionysus the wanderer"),
        ("dianus panus", "Dionysus Pentheus"),
        ("dianis says", "Dionysus says"),
        ("backai in Macedonia", "Bacchae in Macedonia"),
        ("play backy", "play Bacchae"),
        ("plot of the Bai", "plot of the Bacchae"),
        ("the baky are", "the Bacchae are"),
        ("the backy", "the Bacchae"),
        ("the backai", "the Bacchae"),
        ("pentus panthus", "Pentheus"),
        ("pantheus climbs", "Pentheus climbs"),
        ("panthus is", "Pentheus is"),
        ("panus is", "Pentheus is"),
        ("King prome", "King Priam"),
        ("pram um", "Priam um"),
        ("prum is", "Priam is"),
        ("fation is considered", "oration is considered"),
        ("the Bacchae is", "the Bacchae is"),
        ("the bakai is", "the Bacchae is"),
        ("names him edus", "names him Oedipus"),
        (" edus asks", " Oedipus asks"),
        ("ask edus a", "ask Oedipus a"),
        ("if edus can", "if Oedipus can"),
        ("edus gets it", "Oedipus gets it"),
        ("will eat edus", "will eat Oedipus"),
        ("daughter of um edus", "daughter of Oedipus"),
        ("the baky how", "the Bacchae how"),
        ("interpret the Bai", "interpret the Bacchae"),
        ("play backa", "play Bacchae"),
        ("power of dionis and", "power of Dionysus and"),
        (" the bakai are", " the Bacchae are"),
        (" uh UB is", " Euripides is"),
        ("poesis she", "Polynices she"),
        ("P poesis", "Polynices"),
        # civ-09 second pass — Oresteia / Antigone quote-safety
        ("playright", "playwright"),
        ("named at trees okay", "named Atreus okay"),
        ("a treaties won", "Atreus won"),
        ("a treaties being", "Atreus being"),
        ("what a treat a treaties does", "what Atreus does"),
        ("he curses a treaties", "he curses Atreus"),
        ("so a treaties becomes king", "so Atreus becomes king"),
        ("his son agus okay", "his son Orestes okay"),
        ("remaining son is agus", "remaining son is Orestes"),
        ("agus is responsible", "Orestes is responsible"),
        ("the first is Egan who", "the first is Agamemnon who"),
        ("his brother is menw who", "his brother is Menelaus who"),
        ("AG man on marri's clestra", "Agamemnon marries Clytemnestra"),
        ("menas marries Helen", "Menelaus marries Helen"),
        ("remember helin runs", "remember Helen runs"),
        ("Menos tells his brother", "Menelaus tells his brother"),
        ("EG Menan gets upset", "Agamemnon gets upset"),
        ("EG Manan consults", "Agamemnon consults"),
        ("sacrifice your daughter ifia", "sacrifice your daughter Iphigenia"),
        ("Egan man should be", "Agamemnon should be"),
        ("daughter Eugenia so", "daughter Iphigenia so"),
        ("death of Eugenia so", "death of Iphigenia so"),
        ("hell is not my wife", "Helen is not my wife"),
        ("daughter in Virginia the wind", "daughter at Aulis the wind"),
        ("clan mestra right", "Clytemnestra right"),
        ("wife of a Manar because", "wife of Agamemnon because"),
        ("so clra while Agamemnon", "so Clytemnestra while Agamemnon"),
        ("she finds Aus and", "she finds Aegisthus and"),
        ("Victorious kestra kills", "Victorious Clytemnestra kills"),
        ("she makes agius now king", "she makes Aegisthus now king"),
        ("son named aristes and aristes", "son named Orestes and Orestes"),
        ("now aristes upon", "now Orestes upon"),
        ("so R's goes back", "so Orestes goes back"),
        ("mother clestra and Augustus", "mother Clytemnestra and Aegisthus"),
        ("and aristes um becomes", "and Orestes um becomes"),
        ("and Ori says to them", "and Orestes says to them"),
        ("and arises has broken", "and Orestes has broken"),
        ("so now orisses is", "so now Orestes is"),
        ("aristes tells Athena", "Orestes tells Athena"),
        ("both aristes and the fairies", "both Orestes and the Furies"),
        ("clestra killed man on", "Clytemnestra killed Agamemnon"),
        ("eg Manon was an", "Agamemnon was an"),
        ("EG Manan killed their", "Agamemnon killed their"),
        ("decided aesus was guilty", "decided Orestes was guilty"),
        ("vote in favor of aristes", "vote in favor of Orestes"),
        ("now aristes is free", "now Orestes is free"),
        ("the FY say to her", "the Furies say to her"),
        ("the fies say okay", "the Furies say okay"),
        ("arus is allowed to go", "Orestes is allowed to go"),
        ("we thethan people will", "we the Athenian people will"),
        ("ensure democ stays", "ensure democracy stays"),
        ("secretly buries polyes Creon", "secretly buries Polynices Creon"),
        ("poesis has done", "Polynices has done"),
        ("integ says to", "Antigone says to"),
        ("then Tey responds", "then Antigone responds"),
        ("this makes cron very", "this makes Creon very"),
        ("who is Cron's son", "who is Creon's son"),
        ("so hmon the", "so Haemon the"),
        ("cron thinks his son", "Creon thinks his son"),
        ("cron gets very angry", "Creon gets very angry"),
        ("cron and his guards", "Creon and his guards"),
        ("that scares cron so cron", "that scares Creon so Creon"),
        ("body of Antigone is hmon", "body of Antigone is Haemon"),
        ("cron sees his son", "Creon sees his son"),
        ("Antigone and hmon are", "Antigone and Haemon are"),
        ("when hyon's mother", "when Haemon's mother"),
        ("now Kon is a", "now Creon is a"),
        ("in the Ora the play", "in the Oresteia the play"),
        ("with a furious the old", "with the Furies the old"),
        ("talk about um yides okay", "talk about Euripides okay"),
        ("see the Ora in the", "see the Oresteia in the"),
        ("in 4115 BCE", "in 415 BCE"),
        ("when he was a liive", "when he was alive"),
        ("obviously thean people", "obviously the Athenian people"),
        ("reimagines his fation as", "reimagines his funeral oration as"),
        ("then diis the wanderer", "then Dionysus the wanderer"),
        ("pentas says okay", "Pentheus says okay"),
        ("as a backai are about", "as the Bacchae are about"),
        ("people develop huis arrogance", "people develop hubris arrogance"),
        ("challenge the spin to", "challenge the Sphinx to"),
        ("there's a Spinx an", "there's a Sphinx an"),
        ("the spins um ask", "the Sphinx um ask"),
        ("the spin will go", "the Sphinx will go"),
        ("the spin will eat", "the Sphinx will eat"),
        ("the Spinx loses", "the Sphinx loses"),
        ("answer is yeah man okay", "answer is a man okay"),
        ("or uh divor okay", "or uh diviner okay"),
        ("Orestes okay agus escapes", "Orestes escapes"),
        ("aristes goes talks", "Orestes goes talks"),
        ("behalf of aristes and the F say", "behalf of Orestes and the Furies say"),
        ("Athena takes pity on aristes", "Athena takes pity on Orestes"),
        ("so the fies accept", "so the Furies accept"),
        ("that scares cron so Creon", "that scares Creon so Creon"),
        ("then hmon says no", "then Haemon says no"),
        ("before thean people", "before the Athenian people"),
        ("saying toan people", "saying to Athenian people"),
        ("offending thean people", "offending the Athenian people"),
        ("sister of P Polynices", "sister of Polynices"),
        ("it's men's wife", "it's Menelaus's wife"),
        ("and the the say to him", "and the Furies say to him"),
        ("Agamemnon was an right Agamemnon", "Agamemnon was in the right Agamemnon"),
        ("hecubus daughter", "Hecuba's daughter"),
        ("daughter of Oedipus and the BR and", "daughter of Oedipus and Jocasta and"),
        ("achilles is dead", "Achilles is dead"),
        ("one character is hecuba and hecuba", "one character is Hecuba and Hecuba"),
        ("okay hecuba is", "okay Hecuba is"),
        ("so hecuba must", "so Hecuba must"),
        ("Odus okay then", "Odysseus okay then"),
        ("a Maki and J Maki", "Andromache and Andromache"),
        ("draki must witness", "Andromache must witness"),
        ("and then and then heot\nis dragged", "and then she is dragged"),
        ("and then and then heot is dragged", "and then she is dragged"),
        ("Greek General aysus", "Greek general"),
        ("what the play rades did", "what the playwrights did"),
        ("fights for the thr the two brothers", "fights for the throne the two brothers"),
        ("in Thebes to a fean princess", "in Thebes to a Theban princess"),
        ("insulted by the F people", "insulted by the Theban people"),
        ("Fe F people don't", "Theban people don't"),
        ("they are uh aoral okay", "they are uh immoral okay"),
        ("he Hecuba's daughter", "Hecuba's daughter"),
        ("in many ways children the Trojan Women", "in many ways essentially the Trojan Women"),
        ("including melow an island called melow", "including Melos an island called Melos"),
        ("happened in Melos okay", "happened at Melos okay"),
    ]
    return normalize_hellenic(text, reps)


def normalize_civ10(text: str) -> str:
    reps = [
        ("iselis sopes and Ides", "Aeschylus, Sophocles, and Euripides"),
        ("play intey um", "play Antigone um"),
        ("sentences Integrity To Death", "sentences Antigone to death"),
        ("Ina ises told", "Aeschylus told"),
        ("what sakes did", "what Socrates did"),
        ("socres did", "Socrates did"),
        ("socres", "Socrates"),
        ("sakes was", "Socrates was"),
        ("sakes", "Socrates"),
        ("SES did", "Socrates did"),
        ("SES refused", "Socrates refused"),
        ("SES was put", "Socrates was put"),
        ("SES to apologize", "Socrates to apologize"),
        ("SES insisted", "Socrates insisted"),
        ("condemning SES", "condemning Socrates"),
        ("Sak said", "Socrates said"),
        ("Sak students", "Socrates' students"),
        ("soes did not", "Socrates did not"),
        ("saulty student", "Socrates' student"),
        ("path of leas resistance", "path of least resistance"),
        ("satus in Athens", "satirist in Athens"),
        ("the economy okay", "the Academy okay"),
        ("Alo decade", "allegory of the cave"),
        ("CH sakes", "Socrates"),
        ("issist he wanted", "Aeschylus he wanted"),
        ("sopes Andes", "Sophocles and Euripides"),
        ("PlayDoh", "Plato"),
        ("shes was not", "Socrates was not"),
        ("sensorship", "censorship"),
        ("democratus", "Democritus"),
        ("alab 8es", "Alcibiades"),
        ("the aan people", "the Aegean people"),
        ("ultimately the aan", "ultimately the Aegean"),
    ]
    return normalize_hellenic(text, reps)


def normalize_civ11(text: str) -> str:
    reps = [
        ("social stAttalus", "social status"),
        ("he made the caly which was full nobility", "he made the cavalry which was full nobility"),
        ("the spars had discipline", "the Spartans had discipline"),
        ("Philip the Second", "Philip II"),
    ]
    return normalize_hellenic(text, reps)


def normalize_civ12(text: str) -> str:
    reps = [
        ("what a the great did", "what Alexander the Great did"),
        ("that's what a wants", "that's what Alexander wants"),
        ("white Kingdom", "wide kingdom"),
        ("processes the greatest", "possesses the greatest"),
        ("coronated okay", "coordinated okay"),
        ("hear and it seems", "heir and it seems"),
        ("legitimate hear", "legitimate heir"),
        ("nadon will", "Macedon will"),
        ("at Atlas okay", "Attalus okay"),
        ("de devotion", "devotion"),
    ]
    return normalize_hellenic(text, reps)


ARCH_NOTE = (
    'asr_normalization_note: "2026-06-09 pilot Volume II block (civ-01–12); '
    'AI-assisted proper nouns only; not human-verified; verify before quotation."\n'
)
OLD_NOTE_MARKERS = (
    "pilot pass (civ-01/civ-07)",
    "pilot archaeology block (civ-01–07)",
)


def patch_frontmatter(head: str, slug: str) -> str:
    if "normalization_state:" in head:
        if any(marker in head for marker in OLD_NOTE_MARKERS):
            head = re.sub(
                r'asr_normalization_note:.*\n',
                ARCH_NOTE,
                head,
                count=1,
            )
        return head
    insert = (
        "transcript_fidelity: exact_body_match\n"
        "normalization_state: ai_assisted_proper_noun_cleanup\n"
        + ARCH_NOTE
    )
    return head.replace(
        "transcript_fidelity: exact_body_match\n",
        insert,
        1,
    )


NORMALIZERS = {
    "civ-01": normalize_civ01,
    "civ-02": normalize_civ02,
    "civ-03": normalize_civ03,
    "civ-04": normalize_civ04,
    "civ-05": normalize_civ05,
    "civ-06": normalize_civ06,
    "civ-07": normalize_civ07,
    "civ-08": normalize_civ08,
    "civ-09": normalize_civ09,
    "civ-10": normalize_civ10,
    "civ-11": normalize_civ11,
    "civ-12": normalize_civ12,
}


def main() -> None:
    import sys

    slugs = sys.argv[1:] if len(sys.argv) > 1 else list(NORMALIZERS.keys())
    for slug in slugs:
        fn = NORMALIZERS[slug]
        path = ROOT / "book" / "volume-ii" / slug / f"{slug}-transcript.md"
        raw = path.read_text(encoding="utf-8")
        marker = "## Part I: Full transcript"
        head, body = raw.split(marker, 1)
        new_body = fn(body)
        new_head = patch_frontmatter(head, slug)
        path.write_text(new_head + marker + new_body, encoding="utf-8")
        print(f"{slug}: wrote ({'changed' if new_body != body else 'body unchanged'})")


if __name__ == "__main__":
    main()
