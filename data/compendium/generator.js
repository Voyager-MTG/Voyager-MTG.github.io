import { initializeApp } from "firebase/app";
import { setDoc, addDoc, updateDoc, doc, collection, getFirestore, query, where, getDocs, getDoc, deleteDoc } from "firebase/firestore";
import * as fs from "fs"

function isWish(card) {
    const regex = /(reveal|put) (.*?) from your sanctum/gi;

    return regex.test(card.rules_text) && !/^pathbound/gi.test(card.rules_text);
}

function isWipe(card) {
    const regex = /(((destroy|exile) (all|each)( other)? creatures?)|(deals [0-9]+? damage to each [^\n]*? ?creature)|(each ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ gets [+-][0-9]+?\/-[0-9]+?)|((put|return) each ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ (to its owner['’]s hand|on (the)? ?(top|bottom)|(into its owner['’]s sanctum))))/gi;

    return regex.test(card.rules_text);
}

function isCA(card) {
    const regex = /(Clue token|[Ii]nvestigate)|[Dd]raw|[Dd]raft|(play|cast) ([^\n.]+ (from exile|exiled)|(one of )?those cards|them|it this turn|it until)|(graveyard to|into) your hand|\b(?:return\W+(?:\w+\W+){0,5}?to your hand|to your hand\W+(?:\w+\W+){0,5}?return)\b/gi;

    return regex.test(card.rules_text);
}


function isRemoval(card) {
    const regex = /(destroy)|(deals [0-9]+? damage to (any|target|each) (creature|nonplayer|target|planeswalker))|((target|each) (player|opponent) sacrifices?)|(Exile (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ ?[^c][^a][^r][^d])|(fights)|(return (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ to its owner['’]s hand)|(loses all abilities)|(can['’]t attack or block)|(doesn['’]t untap during its controllers untap)|((target|each) (((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+) gets [+-][0-9X]+?\/-[1-9X]+?)|(put (target|each) ((nonland|permanent|creature|artifact|enchantment|planeswalker|battle|land|kindred|legendary|snow) ?)+ on the (top|bottom))/gi;
    
    if (isWipe(card)) return false;
    if (card.rules_text.match(/exile/i) && card.rules_text.match(/return it to the/i)) return false;
    if (card.rules_text.match(/(named|copies of) (spark|through violence)/i)) return false;

    return regex.test(card.rules_text);
}

function isRecurrable(card) {
    const re = `((You may cast (this card|${card.card_name}) from your graveyard)|(return (this card|${card.card_name}) from your graveyard)|(put (this card|${card.card_name}) from your graveyard))`;
    const regex = new RegExp(re, "gi");

    return regex.test(card.rules_text);
}

function isUtilityLand(card) {
    const regex = /({.}+?): [^a][^d][^d].*/gi;

    return regex.test(card.rules_text) && card.type.match(/land/i) && !card.card_name.match(/drifting/i);
}

function isDiscard(card) {
    const regex = /(look at (target|each|an?) (player|opponent)('s)? hand)|((target|each|an?) (player|opponent) reveals [^\n]+? hand)|((player|opponent) discards)/gi;
    return regex.test(card.rules_text);
}

function isPermanent(card) {
    return !card.type.match(/instant|sorcery/i);
}

function isTutor(card) {
    const searchRegex = /search your library for a [^\n]+?card/gi;
    const landRegex = /search your library for a [^\n]*?(land|plains|island|swamp|mountain|forest|fault) card/gi;
    return searchRegex.test(card.rules_text) && !landRegex.test(card.rules_text);
}

function isCounterspell(card) {
    return /counter target [\w^\n]*? ?spell/gi.test(card.rules_text);
}

function isThreat(card) {
    return card.rules_text.match(/creature token|becomes? a? ?creatures?|are creature|is a creature/gi) || card.type.match(/creature/gi);
}

function isRamp(card) {
    return /Treasure token|[Aa]dd ({|(one|two|three|X) mana|an amount of {|)|additional land|\b(?:((land|Plains|Island|Swamp|Mountain|Forest|Fault))\W+(?:\w+\W+){0,6}?the battlefield)\b|(land|Plains|Island|Swamp|Mountain|Forest|Fault) token /gi.test(card.rules_text) && !/land/gi.test(card.type);
}

const compendium_rules = {
    Interaction: {
        'Small Removal': card => convertToMV(card.cost) < 4 && isRemoval(card) && card.rules_text.match(/(\/-[1-4X])|(deals [1-4])|(mana value [1-3])|((power|toughness) [1-3])/gi),
        'Unconditional Removal': card => isRemoval(card) && card.rules_text.match(/exile target|destroy/gi) && !isInCategory(card, 'Interaction', 'Small Removal') && !card.rules_text.match(/target (artifact|enchantment)/gi),
        'Other Removal': card => isRemoval(card) && !isInCategory(card, 'Interaction', 'Small Removal') && !isInCategory(card, 'Interaction', 'Unconditional Removal'),
        'Countermagic': card => isCounterspell(card),
        'Boardwipes': card => isWipe(card),
        'Discard': card => isDiscard(card)
    },
    Threats: {
        'Early Threats': card => isThreat(card) && !isCA(card) && convertToMV(card.cost) < 3,
        'Midrange Threats': card => isThreat(card) && convertToMV(card.cost) < 5 && convertToMV(card.cost) > 2,
        'Topend Threats': card => isThreat(card) && convertToMV(card.cost) > 4
    },
    Value: {
        'Draw/Selection': card => isCA(card) && !card.type.match(/land/i),
        'Ramp': card => isRamp(card),
        'Tutors': card => isTutor(card),
        'Combo': card => false // Manual ordering
    },
    Sanctum: {
        'Pathbound': card => /^pathbound/gi.test(card.rules_text),
        'Erysites': card => /^transcend/gi.test(card.rules_text),
        'Wonders': card => /wonder/gi.test(card.type),
        'Fetchers': card => isWish(card)
    }
};

function isInCategory(card, category, subcategory) {
    return (compendium_rules[category]?.[subcategory]?.(card) || manual_include[category]?.[subcategory]?.includes?.(card.card_name)) && !manual_exclude[category]?.[subcategory]?.includes?.(card.card_name);
}

const delay = ms => new Promise(res => setTimeout(res, ms));

function generateCompendium() {
    const compendium = {};

    for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
        compendium[headingName] = {};
        for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
            compendium[headingName][subheadingName] = [];
        }
    }
    
    for (const card of card_list_arrayified) {
        if (card.shape.includes("token") || card.card_name.includes('ITD')) continue;
        for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
            for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
                // if ((rule(card) && meetsPlayrate(card) && !manual_exclude[headingName]?.[subheadingName]?.includes?.(card.card_name)) || manual_include[headingName]?.[subheadingName]?.includes?.(card.card_name)) 
                if (card.card_name === "Delete" && subheadingName === 'Small Removal') 
                    console.log(isInCategory(card, headingName, subheadingName) && meetsPlayrate(card));
                if (isInCategory(card, headingName, subheadingName) && meetsPlayrate(card))
                    compendium[headingName][subheadingName].push(card.card_name);
            }
        }
    }

    for (const [ headingName, subheadings ] of Object.entries(compendium_rules)) {
        for (const [ subheadingName, rule ] of Object.entries(subheadings)) {
            compendium[headingName][subheadingName] = [...new Set(compendium[headingName][subheadingName])];
            compendium[headingName][subheadingName].sort(playrateFn);
            const size = sizes?.[headingName]?.[subheadingName] || 12;
            compendium[headingName][subheadingName] = compendium[headingName][subheadingName].slice(0, size);
        }
    }

    return compendium;
}

function isDecimal(char) {
	return char >= '0' && char <= '9';
}

function convertToMV(cost) {
    let mv = 0;

    const costTokens = cost.substring(1, cost.length - 1).replaceAll("}{", " ").split(' ');
    for (const token of costTokens) {
        if (isDecimal(token)) {
            mv += parseInt(token);
        }
        // 2brid
        else if (token.includes('2')) {
            mv += 2;
        }
        else if (token != "x" && token != '') {
            mv += 1;
        }
    }

    return mv;
}

function meetsPlayrate(card) {
    const pr = playrates[card.card_name] / numDecks;
    return pr > 0.015;
}

function playrateFn(a, b) {
    return playrates[b] - playrates[a];
}

const firebaseConfig = {
    apiKey: "AIzaSyCPurnKVn2caCn3L-gKF2tMFwWur73YAuw",
    authDomain: "voyager-78e30.firebaseapp.com",
    projectId: "voyager-78e30",
    storageBucket: "voyager-78e30.firebasestorage.app",
    messagingSenderId: "411191248476",
    appId: "1:411191248476:web:591349be169d823e5f8899",
    measurementId: "G-TQ1L48F25M"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const db = getFirestore(app);

async function getCardStats() {
    const stats = {};

    for (const card of card_list_arrayified) {
        stats[card.card_name] = 0;
    }

    for (const deck of all_decks) {
        const decklist = atob(deck.url.split(';')[1].split('&main')[0]);
        for (const line of decklist.split("\n")) {
            const card_name = line.substring(line.indexOf(" ") + 1, line.length).split('(')[0].trim();

            if (stats[card_name] == null) continue;

            stats[card_name]++;
        }
    }

    return stats;
}

const all_decks = [];
let q;

q = query(collection(db, "events"));
const all_events_docs = await getDocs(q);

q = query(collection(db, "users"));
const all_users_docs = await getDocs(q);

all_events_docs.forEach((doc) => {
    const data = doc.data();
    for (const user in data.decks) {
        const deck = data.decks[user];
        all_decks.push({ ...deck, "user": user, "event": true });
    }
});

all_users_docs.forEach((doc) => {
    const data = doc.data();
    for (const deck of data.decks) {
        all_decks.push({ ...deck, "user": data.username, "event": false });
    }
});

const { manual_exclude, manual_include, sizes } = JSON.parse(fs.readFileSync('input.json'));
let card_list_arrayified, playrates, numDecks;


fs.readFile('../../lists/all-cards.json', 'utf8', async (err, data) => {
    const all_cards = JSON.parse(data);
    card_list_arrayified = all_cards.cards;

    playrates = await getCardStats();
    numDecks = all_decks.length;

    const compendium = generateCompendium();

    fs.writeFileSync('compendium.json', JSON.stringify(compendium));
    process.exit(0);
});