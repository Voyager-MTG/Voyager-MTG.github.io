// import * as fs from 'fs';
// const draftlog = JSON.parse(fs.readFileSync('log.json').toString());
// console.log(JSON.stringify(draftlog).length);

function toBase94(n) {
    let res = '';
    while (n > 0) {
        res += String.fromCharCode(n % 94 + 32);
        n = Math.floor(n / 94);
    }
    return res;
}

function fromBase94(s) {
    let n = 0;
    let digit = 0;
    for (c of s) {
        n += (c.charCodeAt(0) - 32) * Math.pow(94, digit);
        digit++;
    }
    return n;
}

async function compressLog(draftlog, set) {
    let hash;
    let set_json;
    // const set = 'PTN';
    // const set_json = JSON.parse(fs.readFileSync(`../../../sets/${set}-files/${set}.json`).slice(3).toString()).cards;
    await fetch(`https://api.github.com/repos/Voyager-MTG/Voyager-MTG.github.io/commits/main`)
        .then(response => response.json())
        .then(json => {
            hash = json.sha;
        }).catch(error => console.error('Error:', error));

    // console.log(`https://raw.githubusercontent.com/Voyager-MTG/Voyager-MTG.github.io/${hash}/sets/${set}-files/${set}.json`)
    await fetch(`https://raw.githubusercontent.com/Voyager-MTG/Voyager-MTG.github.io/${hash}/sets/${set}-files/${set}.json`)
        .then(response => response.json())
        .then(json => {
            set_json = json.cards;
        }).catch(error => console.error('Error:', error));

    const compressed_obj = {};

    for (const user of Object.values(draftlog.users)) {
        compressed_obj[user.userName] = user.cards.map(c => c.split('_')[0]);
    }

    compressed_obj.boosters = draftlog.boosters.map(l => l.map(c => c.split('_')[0]));
    const cards = {};

    for (const booster of compressed_obj.boosters) {
        for (const card of booster) {
            if (cards[card]) continue;
            cards[card] = set_json.findIndex(c => c.card_name == card);
        }
    }

    let compressed = '';
    compressed += `${hash}~${set}\n`;
    for (const name in cards) {
        cards[name] = toBase94(cards[name]);
    }

    for (const [key, value] of Object.entries(compressed_obj)) {
        if (key != 'boosters') {
            compressed += key + '~\n';
            compressed += value.map(c => cards[c]).join('\n') + '\n';
        } else {
            compressed += key + '~\n';
            compressed += value.map(b => b.map(c => cards[c]).join('\n')).join('~');
        }
    }

    return compressed;
}

async function decompressLog(compressed) {
    const data = {};
    const [hash, set] = compressed.split('\n')[0].split('~');
    compressed = compressed.slice(compressed.split('~' + set + '~')[1]);
    const keys = compressed.match(/^(.*?)~\n/gm);

    let set_json;
    await fetch(`https://raw.githubusercontent.com/Voyager-MTG/Voyager-MTG.github.io/${hash}/sets/${set}-files/${set}.json`)
        .then(response => response.json())
        .then(json => {
            set_json = json.cards;
        }).catch(error => console.error('Error:', error));


    for (let i = 0; i < keys.length - 1; i++) {
        const current_key = keys[i];
        const next_key = keys[i + 1];
        const value = compressed.split(current_key)[1].split(next_key[0])[0];
        const cards = value.split('\n').map(c => fromBase94(c)).map(i => set_json[i]);
        data[current_key] = cards;
    }

    const boosters = compressed
        .split('boosters~\n')[1]
        .split('~')
        .map(b => 
            b.split('\n')
                .map(c => fromBase94(c))
                .map(i => set_json[i])
        );

    data.boosters = boosters;
    return data;        
}