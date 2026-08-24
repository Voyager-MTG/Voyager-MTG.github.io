#### THIS SCRIPT IS MEANT TO BE RUN FROM HERE AND IS NOT A PART OF THE BUILD PROCESS

import related_cards
import json, re

def custom_index(it, f, default=-1):
    return next((i for i, e in enumerate(it) if f(e)), default)

# use this to mark problems as nonexistent/resolved, and these cards will be skipped over
RESOLVED = [
    "Shell's Scraping",
    "Bloodstained Fields",
    "Depthscout",
    "Beacon of Greatness",
    "Terrel Decree",
    "Vance Decree",
    "Explore the Great Unknown",
    "King's Rock Warden",
    "Hexer's Cave",
    "Meet the Beyond",
    "Seven-Coil's Scion",
    "Against the Night",
    "Giant's Blade",
    "Gateway Guardian",
    "Glory on Bloodied Wings",
    "Avlod Bulwark"
]

all_cards = []
with open('lists/all-cards.json', 'r') as f:
    all_cards = json.load(f)['cards']

all_tokens = []
all_created_tokens = []
missing_tokens = []
cards = []

for card in all_cards:
    if 'token' in card['shape']:
        all_tokens.append(card)
    else:
        cards.append(card)

for card in cards:
    expected = []

    for token in related_cards.TOKENMATCHES.keys():
        exp = related_cards.TOKENMATCHES[token]
        if not card["rules_text"] or card["rules_text"] == None or card["rules_text"] == "" or card['set'] == 'ABY':
            continue

        token = token.replace("~", card["card_name"])
        token = token.replace("CARDNAME", card["card_name"])
        # token = token.replace("CARDTYPE", card["type"])
        token = token.replace("CARDSET" , card["set"])
        
        if re.findall(exp, card["rules_text"]):
            for tk in all_tokens:
                if f'{tk['card_name']} {tk['set']}' == token: 
                    expected.append([tk, 1, '!conjured' in tk['notes'], False])
                    break

    big_match = re.findall(r'creates? [^.]+', card["rules_text"], flags=re.I)
    if big_match and not "!noscript" in card["notes"] and not card['set'] in related_cards.NO_SCRIPT_SETS:
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

                count = related_cards.englishToNumber(tokenMatch[0])
                token_to_script = related_cards.getToken(all_tokens, token_type, token_colors, pt, card["set"])
                
                if token_type == "":
                    token_name = re.findall("[N|n]amed (.*?) (with|that)", str(tokenMatch[17]))

                    for tk in all_tokens:
                        if tk['card_name'] == token_name: 
                            related_cards.append([tk, 1, '!conjured' in tk['notes'], False])
                            break
                else:
                    if token_to_script: expected.append([token_to_script, count, '!conjured' in token_to_script['notes'], False])
                    else: expected.append([f'{pt} {token_colors} {token_type} {card['set']}', 1, False, False])

    related = related_cards.auto_related(card, all_tokens) + related_cards.notes_related(card, all_cards)
    related = list(filter(lambda r: not r[3], related))
    if 'get' in card['rules_text'] and 'a Scar' in card['rules_text']:
        expected.append(['Scar EXPT', 1, False, False])

    if len(related) > len(expected):
        if card['card_name'] in RESOLVED: continue
        for r in expected:
            i = custom_index(related, lambda e: e[0] == r[0])
            related.pop(i)

        # print(card['card_name'])
        # print(card['card_name'], ', '.join(map(lambda r: print((r)), related[0])))
        extras = ''
        for r in related:
            # print(r[0]['card_name'])
            extras += f'{r[0]['card_name']} {r[0]['set']}, '

        print(f'On {card['card_name']} ({card['set']}) {card['number']}: Found extra tokens of {extras[:-2]}')

    elif len(related) > len(expected):
            if card['card_name'] in RESOLVED: continue
            for r in related:
                i = custom_index(expected, lambda e: e[0] == r[0])
                expected.pop(i)
    
            # print(card['card_name'])
            # print(card['card_name'], ', '.join(map(lambda r: print((r)), related[0])))
            extras = ''
            for r in related:
                # print(r[0]['card_name'])
                extras += f'{r[0]['card_name']} {r[0]['set']}, '
    
            print(f'On {card['card_name']} ({card['set']}) {card['number']}: Found extra tokens of {extras[:-2]}')