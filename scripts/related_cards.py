import re

NO_SCRIPT_SETS = [ 'ABY' ]

def xml_escape(text: str):
	return text.replace('&', '&amp;') \
				.replace('"', '&quot;') \
				.replace('“', '&quot;') \
				.replace('”', '&quot;') \
				.replace('\'', '&apos;') \
				.replace('’', '&apos;') \
				.replace('<', '&lt;') \
				.replace('>', '&gt;') \

def englishToNumber(s):
	n = 1

	if "one" == s or "a" == s or "an" == s:
		n = 1
	elif "two" == s:
		n = 2
	elif "three" == s:
		n = 3
	elif "four" == s:
		n = 4
	elif "five" == s:
		n = 5
	elif "six" == s:
		n = 6
	elif "seven" == s:
		n = 7
	elif "eight" == s:
		n = 8
	elif "nine" == s:
		n = 9
	elif "ten" == s:
		n = 10
	elif "eleven" == s:
		n = 11
	elif "twelve" == s:
		n = 12
	elif "thirteen" == s:
		n = 13
	elif "fourteen" == s:
		n = 14
	elif "fifteen" == s:
		n = 15
	elif "sixteen" == s:
		n = 16
	elif "seventeen" == s:
		n = 17
	elif "eighteen" == s:
		n = 18
	elif "nineteen" == s:
		n = 19
	elif "twenty" == s:
		n = 20
	elif "x" in s or "that many" in s or "a number" in s:
		n = "x"

	return n

def getCount(n):
	if n != 1:
		return f" count=\"{n}\""
	else:
		return ""

def getSubtype(typ):
	if "–" in typ:
		return typ.split("–")[1].strip()
	else:
		return ""
	
def convertColors(c):
	s = ""
	colormap = {
		"white" : "W",
		"blue"  : "U",
		"black" : "B",
		"red"   : "R",
		"green" : "G",
		"silver": "I",
		"all colors": "WUBRGI"
	}
	for k, v in colormap.items():
		s += v if k in c else ""
	
	return s

def getToken(tokens, type = None, colors = None, pt = None, set = None):
	if type == "" and colors == "":
		return None
	
	possible_tokens = []
	for card in tokens:
		type_eq   = type   == None or str(type).strip()          == str(getSubtype(card.get("type")))
		colors_eq = colors == None or str(card["color"]).strip() == str(convertColors(colors))
		pt_eq	  = pt	   == None or str(card.get("pt"))        == str(pt).strip()
		
		if (type_eq and colors_eq and pt_eq and set == card["set"]):
			return card
		elif (type_eq and colors_eq and pt_eq):
			possible_tokens.append(card)

	return possible_tokens[0] if possible_tokens else None

TOKENMATCHES = {
	"Can Be Cast From Exile EXPT": "(play|cast) ([^\\n.]+ (from exile|exiled)|(one of )?those cards|them|it this turn|it until)",
	"Embraced Cards AKT": "(E|e)mbrace",
	"Liberated Dragon AKT": "(L|l)iberate",
	"Trace Reminder VNM": "(C|c)reate (a|two|three|four|five|X) trace(s?) of",
	"Vertex Reminder PVR": "{V",
	"Luminous VNM": "(L|l)uminous",
	"Reserves HOD": "(I|i)n your reserves",
	"~ WAW": "Reflect {[0-9WUBRGIXYZ]+?}",
	"~ ITD": "Iterate",
	"Cleric PTN": "Induct"
}

def auto_related(card, tokens):
	related_cards = []

	for token in TOKENMATCHES.keys():
		exp = TOKENMATCHES[token]
		if not card["rules_text"] or card["rules_text"] == None or card["rules_text"] == "" or card['set'] == 'ABY':
			continue

		token = token.replace("~", card["card_name"])
		token = token.replace("CARDNAME", card["card_name"])
		# token = token.replace("CARDTYPE", card["type"])
		token = token.replace("CARDSET" , card["set"])
		
		if re.findall(exp, card["rules_text"]):
			for tk in tokens:
				if f'{tk['card_name']} {tk['set']}' == token: 
					related_cards.append([tk, 1, '!conjured' in tk['notes'], False])
					break

	big_match = re.findall(r'creates? [^.]+', card["rules_text"], flags=re.I)
	if big_match and not "!noscript" in card["notes"] and not card['set'] in NO_SCRIPT_SETS:
		for phrase in big_match:
			token_regex = re.compile("[C|c]reate (X|X plus one|a number of|that many|a|an|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty)( tapped| goaded)?( and attacking)?( legendary)?( basic)?( snow)? ?([XYZ0-9]+/[XYZ0-9]+ )?(colorless|white|blue|black|red|green|silver)?(, (?:white|blue|black|red|green|silver),)?( and white| and blue| and black| and red| and green| and silver)? ?([A-Z][a-z]+)?( [A-Z][a-z]+)?( [A-Z][a-z]+)? ?(enchantment )?(artifact )?(land )?(creature )?tokens?( (with|named|that[’']s|that is|that are|attached|that can't block) [^\n.]+)?")
			matched_tokens = token_regex.search(phrase)

			if matched_tokens:
				tokenMatch = matched_tokens.groups()

				token_type = ''
				for type in tokenMatch[10:13]:
					if type: token_type += type
				token_type = token_type.strip()

				token_colors = ''
				for c in tokenMatch[7:10]:
					if c: token_colors += c
				token_colors = token_colors.strip()

				pt = tokenMatch[6].strip() if tokenMatch[6] else ""

				count = englishToNumber(tokenMatch[0])
				token_to_script = getToken(tokens, token_type, token_colors, pt, card["set"])

				if token_type == "":
					token_name = re.findall("[N|n]amed (.*?) (with|that)", str(tokenMatch[17]))

					for tk in tokens:
						if tk['card_name'] == token_name: 
							related_cards.append([tk, 1, '!conjured' in tk['notes'], False])
							break
						
				else:
					if token_to_script: related_cards.append([token_to_script, count, '!conjured' in token_to_script['notes'], False])

	return related_cards

def  get_related(notes, instruction, tag):
	related = []
	for line in notes.split('\n'):
		if not line.startswith(instruction):
			continue

		tokens = line[len(instruction) + 1:].split(';')
		for token in tokens:
			match = re.match(r'([^<]+)(?:<([^<]+)>)?', token)
			if not match:
				if token == '': continue
				print(f'Warning: could not process {instruction} name "{token}". Ignoring.')
				continue

			name, num = match.groups()
			if num == 'attach': continue
			
			is_persistent = num == "persistent" or num == "conjure"
			related.append([xml_escape(name).strip(), num or 1, is_persistent, tag == 'reverse-related'])

	return related

def notes_related(card, all_cards):
	related = get_related(card['notes'], '!tokens', 'related') + get_related(card['notes'], '!addtoken', 'related') + get_related(card['notes'], '!related', 'reverse-related')

	for i, relation in enumerate(related):
		for _card in all_cards:
			if relation[0] == _card['card_name']:
				related[i][0] = _card
				break

	i = 0
	while i < len(related):
		relation = related[i]
		if isinstance(relation[0], str):
			related.pop(i)
		else:
			i += 1

	# print(related)
	return related