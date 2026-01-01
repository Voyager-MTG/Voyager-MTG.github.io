import os
import json
import re
from datetime import datetime

def get_picurl(card, back=False):
	return (
		f'https://voyager-mtg.github.io/sets/{card['set']}-files/img/' +
		(f'{card['position']}' if 'position' in card else f'{card['number']}{'t' if 'token' in card['shape'] else ''}_{card[f'card_name']}') +
		('' if 'double' not in card['shape'] else '_back' if back else '_front') +
		f'.jpg'
	)

def xml_escape(text: str):
	return text.replace('&', '&amp;') \
				.replace('"', '&quot;') \
				.replace('“', '&quot;') \
				.replace('”', '&quot;') \
				.replace('\'', '&apos;') \
				.replace('’', '&apos;') \
				.replace('<', '&lt;') \
				.replace('>', '&gt;') \

def format_cost(cost):
	if len(cost) == 0: return ''
	symbols = re.split(r'\{([^{}]+)\}', cost)
	cost = ''
	for symbol in symbols:
		if len(symbol) == 0: continue
		if symbol.isdecimal(): 
			cost += symbol
			continue
		cost += '/'.join(symbol)
	return cost

def cost_to_cmc(cost):
	symbols = re.split(r'\{([^{}]+)\}', cost)
	cmc = 0
	for symbol in symbols:
		if len(symbol) == 0 or symbol == "X" or symbol == "Y": continue
		try:
			num = re.match(r'\d+', symbol).group(0)
			cmc += int(num)
		except:
			cmc += 1
	return cmc

def get_maintype(type):
	first_half = type.split('\u2014')[0].strip()
	return first_half.split(' ')[-1].strip()

def get_related(notes, instruction, tag):
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
			if not num:
				extra = ''
			elif num.isdecimal() or num == "x" or num == "X":
				extra = f' count="{num}"'
			elif num == "persistent" or num == "conjure":
				extra = ' persistent=""'
			else:
				print(f'Warning: unknown {instruction} parameter <{num}>. Ignoring.')
				extra = ''
			related.append(f'<{tag}{extra}>{xml_escape(name).strip()}</{tag}>')

	return related

def get_number(card, back):
	return f'{card['number']}{'' if 'double' not in card['shape'] else 'b' if back else 'a'}'

def get_tablerow(card_type):
	return (
		2 if 'Creature' in card_type else
		0 if 'Land' in card_type else
		3 if 'Instant' in card_type or 'Sorcery' in card_type else
		1
	)

def get_text(card, back, flipped):
	combine_texts = not back and not flipped and ('split' in card['shape'] or 'adventure' in card['shape'] or 'aftermath' in card['shape'])
	return (
		f'{card[f'rules_text{'2' if back or flipped else ''}']}' +
		(f'\n---\n({'Front' if back else 'Back'}): {card[f'card_name{'' if back else '2'}']}' if 'double' in card['shape'] else '') +
		(f'\n{card['rules_text3']}' if 'rules_text3' in card and card['rules_text3'] else '') +
		(f'\n\n---\n\n{get_text(card, True, False)}' if combine_texts else '')
	).strip()

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
	}
	for k, v in colormap.items():
		s += v if k in c else ""
	
	return s if s else None

def getToken(tokens, type = None, colors = None, pt = None, set = None):
	if type == "" and colors == "":
		return None
	
	possible_tokens = []
	for card in tokens:
		type_eq   = type   == None or str(type).strip() == str(getSubtype(card.get("type")))
		colors_eq = colors == None or str(card["color"]).strip() == str(convertColors(colors))
		pt_eq	 = pt	 == None or str(card.get("pt")) == str(pt).strip()
		
		if (type_eq and colors_eq and pt_eq and set == card["set"]):
			return card["card_name"] + ' ' + card['set']
		elif (type_eq and colors_eq and pt_eq):
			possible_tokens.append(card["card_name"] + ' ' + card['set'])

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
	"~ ITD": "Iterate"
}

def auto_related(card, tokens):
	related_cards = []

	for token, exp in TOKENMATCHES.items():
		if not card["rules_text"] or card["rules_text"] == None or card["rules_text"] == "":
			continue

		token = token.replace("~", card["card_name"])
		token = token.replace("CARDNAME", card["card_name"])
		# token = token.replace("CARDTYPE", card["type"])
		token = token.replace("CARDSET" , card["set" ])
		
		if re.findall(exp, card["rules_text"]):
			related_cards.append([token, 1])

	big_match = re.findall(r'creates? [^.]+', card["rules_text"], flags=re.I)
	if big_match and not "!noscript" in card["notes"]:
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

					if token_name:
						token_to_script = token_name[0][0] + " " + card["set"]
						related_cards.append([token_to_script, count])
						
				else:
					if token_to_script == None: print(card, token_type, token_colors, pt, card['set'])
					related_cards.append([token_to_script, count])

	return format_auto_related(related_cards)

def format_auto_related(related):
	# if len(related) != 0: print('related', related)
	return [f"<related{getCount(card[1])}>{card[0]}</related>" for card in related]

def render_card(card, tokens, /, *, back=False, flipped=False, token=False):
	is_split = 'split' in card['shape'] or 'aftermath' in card['shape']
	is_two_cards = is_split or 'adventure' in card['shape']
	suffix = '2' if back or flipped else ''

	card_type = card[f'type{suffix}'].strip() + (f' // {card[f'type2'].strip()}' if is_two_cards and card[f'type2'] and card[f'type2'] != card[f'type'] else '')
	layout = (
		'mutate' if 'Mutate' in card[f'rules_text{suffix}'] else
		'saga' if 'Saga' in card_type else
		'normal'
	)
	shape_to_layout = {
		'double': 'transform',
		'flip': 'flip',
		'split': 'split',
		'battle': 'battle',
		'adventure': 'adventure',
		'aftermath': 'aftermath',
		'leveler': 'leveler',
	}
	for shape, new_layout in shape_to_layout.items():
		if shape in card['shape']:
			layout = new_layout
			break

	mana_cost = format_cost(card[f'cost{suffix}']) + (f' // {format_cost(card[f'cost2'])}' if is_two_cards else '')
	cmc = cost_to_cmc(card[f'cost{suffix}']) + (cost_to_cmc(card[f'cost2']) if is_split else 0)
	# For the <side>, canon flip cards have their side set to "back" in Cockatrice for their flipped version to transform it back when it leaves the battlefield
	props = f'''
				<layout>{layout}</layout>
				<side>{'back' if back or flipped else 'front'}</side>
				<type>{xml_escape(card_type)}</type>
				<maintype>{xml_escape(get_maintype(card[f'type{suffix}']))}</maintype>
				<manacost>{xml_escape(mana_cost)}</manacost>
				<cmc>{cmc}</cmc>'''

	if len(card[f'color{suffix}']):
		props += f'''
				<colors>{card[f'color{suffix}']}</colors>'''

	color_identity = card['color_identity'].replace('C', '')
	if len(color_identity):
		props += f'''
				<coloridentity>{color_identity}</coloridentity>'''

	if len(card[f'pt{suffix}']):
		props += f'''
				<pt>{xml_escape(card[f'pt{suffix}'])}</pt>'''

	if len(card[f'loyalty{suffix}']):
		props += f'''
				<loyalty>{xml_escape(card[f'loyalty{suffix}'])}</loyalty>'''

	card_name = (f'{card[f'card_name']} // {card[f'card_name2']}' if is_two_cards else card[f'card_name{suffix}'] if not 'token' in card['shape'] else card['card_name'] + ' ' + card['set'])
	card_string = f'''
		<card>
			<name>{xml_escape(card_name)}</name>
			<text>{re.sub(r'\[/?i\]', '', xml_escape(get_text(card, back, flipped)))}</text>
			<set rarity="{'rare' if card['rarity'] == 'cube' else card['rarity']}" picurl="{xml_escape(get_picurl(card, back))}" num="{get_number(card, back)}">{xml_escape(card['set'])}</set>
			<prop>{props}
			</prop>
			<tablerow>{get_tablerow(card_type)}</tablerow>'''

	if flipped:
		card_string += '''
			<upsidedown>1</upsidedown>'''

	related = get_related(card['notes'], '!tokens', 'related')
	if 'double' in card['shape']:
		related.append(f'<related attach="transform">{xml_escape(card['card_name' if back else 'card_name2'])}</related>')
	if 'flip' in card['shape']:
		related.append(f'<related attach="transform">{xml_escape(card['card_name' if flipped else 'card_name2'])}</related>')
	if len(related):
		card_string += f'''
			{'\n			'.join(related)}'''

	reverse_related = get_related(card['notes'], '!related', 'reverse-related')
	auto_reverse_related = auto_related(card, tokens)
	print(auto_reverse_related)
	if len(reverse_related):
		card_string += f'''
			{'\n			'.join(reverse_related)}
			{'\n			'.join(auto_reverse_related)}'''

	if '!tapped' in card['notes']:
		card_string += f'''
			<cipt>1</cipt>'''

	card_string += '''
		</card>'''

	if 'double' in card['shape'] and not back:
		card_string += render_card(card, tokens, back=True)

	if 'flip' in card['shape'] and not flipped:
		card_string += render_card(card, tokens, flipped=True)

	return card_string

def generateSet(code):
	with open(os.path.join('sets', code + '-files', code + '.json'), encoding='utf-8-sig') as j:
		set_data = json.load(j)

	return f'''
			<set>
				<name>{xml_escape(code)}</name>
				<longname>{xml_escape(set_data['name'])}</longname>
			</set>
	'''

def generateSets(set_codes):
	res = ''

	for code in set_codes:
		res += generateSet(code)
		res += '\n'

	return res

def generateFile(set_codes):
	tokens = []
	cards = []

	with open(os.path.join('lists', 'all-cards.json'), encoding='utf-8-sig') as j:
		all_cards = json.load(j)

	for card in all_cards['cards']:
		if 'token' in card['shape']:
			tokens.append(card)
			continue
		cards.append(card)

	cards_xml = f'''<?xml version='1.0' encoding='UTF-8'?>
<cockatrice_carddatabase version='4'>
	<sets>
		
		{generateSets(set_codes)}
	</sets>
	<cards>'''

	for card in cards:
		cards_xml += render_card(card, tokens)

	cards_xml += '''
	</cards>
</cockatrice_carddatabase>'''

	with open(os.path.join('lists', 'cards.xml'), 'w', encoding='utf-8') as f:
		f.write(cards_xml)

		tokens_xml = f'''<?xml version='1.0' encoding='UTF-8'?>
<cockatrice_carddatabase version='4'>
	<cards>'''

	for token in tokens:
		tokens_xml += render_card(token, tokens, token=True)

	tokens_xml += '''
	</cards>
</cockatrice_carddatabase>'''

	with open(os.path.join('lists', 'tokens.xml'), 'w', encoding='utf-8') as f:
		f.write(tokens_xml)