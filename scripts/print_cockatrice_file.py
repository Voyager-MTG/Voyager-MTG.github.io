import os
import json
import re
from datetime import datetime

uuid = 0

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
	first_half = type.split('–')[0].strip()
	return first_half.split(' ')[-1].strip()

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

def render_card(card, tokens, /, *, back=False, flipped=False, token=False):
	global uuid
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

	props += f'''
				<colors>{card[f'color{suffix}']}</colors>'''

	color_identity = card['color_identity'].replace('C', '')
	props += f'''
				<coloridentity>{color_identity}</coloridentity>'''

	if len(card[f'pt{suffix}']):
		props += f'''
				<pt>{xml_escape(card[f'pt{suffix}'])}</pt>'''

	if len(card[f'loyalty{suffix}']):
		props += f'''
				<loyalty>{xml_escape(card[f'loyalty{suffix}'])}</loyalty>'''
		
	tags = re.findall('!tag (^\n+)', card['notes'])
	if len(tags):
		props += f'''
				<tag>{','.join(tags)}</tag>'''

	card_name = (f'{card[f'card_name']} // {card[f'card_name2']}' if is_two_cards else card[f'card_name{suffix}'] if not 'token' in card['shape'] else card['card_name'] + ' ' + card['set'])
	card_string = f'''
		<card>
			<name>{xml_escape(card_name)}</name>
			<text>{re.sub(r'\[/?i\]', '', xml_escape(get_text(card, back, flipped)))}</text>
			<set rarity="{'rare' if card['rarity'] == 'cube' else card['rarity']}" picurl="{xml_escape(get_picurl(card, back))}" num="{get_number(card, back)}" uuid="{uuid}">{xml_escape(card['set'])}</set>
			<prop>{props}
			</prop>
			<tablerow>{get_tablerow(card_type)}</tablerow>'''

	uuid += 1

	if flipped:
		card_string += '''
			<upsidedown>1</upsidedown>'''

	if card.get('related'):
		for name, related in card['related'].items():
			tag = f"{'reverse-' if related['reverse'] else ''}related"
			count = '' if related['count'] == 1 else f' count="{related['count']}"'
			persistent = '' if not related['persistent'] else ' persistent=""'
			_set = '' if related['reverse'] else f' {related['set']}'

			card_string += f'\n\t\t\t<{tag}{count}{persistent}>{name}{_set}</{tag}>'

	# related = related_cards.get_related(card['notes'], '!tokens', 'related')
	if 'double' in card['shape']:
		card_string += f'\n\t\t\t<related attach="transform">{xml_escape(card['card_name' if back else 'card_name2'])}</related>'
	if 'flip' in card['shape']:
		card_string += f'\n\t\t\t<related attach="transform">{xml_escape(card['card_name' if flipped else 'card_name2'])}</related>'
	# if len(related):
	# 	card_string += f'''
	# 		{'\n			'.join(related)}'''

	# reverse_related = related_cards.get_related(card['notes'], '!related', 'reverse-related')
	# auto_reverse_related = format_auto_related(related_cards.auto_related(card, tokens))
	# if len(reverse_related) or len(auto_reverse_related):
	# 	card_string += f'''
	# 		{'\n			'.join(reverse_related)}
	# 		{'\n			'.join(auto_reverse_related)}'''

	if '!tapped' in card['notes']:
		card_string += f'''
			<cipt>1</cipt>'''
		
	if token:
		card_string += f'''
			<token>1</token>'''

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

	return f'''			<set>
				<name>{xml_escape(code)}</name>
				<longname>{xml_escape(set_data['name'])}</longname>
			</set>'''

def generateSets(set_codes):
	res = ''

	for code in set_codes:
		res += generateSet(code)
		res += '\n'

	return res[:-1]

def generateFile(set_codes):
	tokens = []
	cards = []

	with open(os.path.join('lists', 'all-cards.json'), encoding='utf-8') as j:
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