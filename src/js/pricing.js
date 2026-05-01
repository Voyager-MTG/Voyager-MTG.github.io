let card_list;
let stats;
let seed = false;

function sigmoid(x, b = 1) {
    return 1 / (1 + Math.exp((-1 / b) * x));
}

// const rarityN = {
//     common: 0.1,
//     uncommon: 0.25,
//     rare: 0.75,
//     mythic: 1
// };

const buyValues = {
    common: 30,
    uncommon: 50,
    rare: 200,
    mythic: 500
};

const sellValues = {
    common: 5,
    uncommon: 10,
    rare: 50,
    mythic: 100
};

// const set_price = {
//     AKT: ,
//     EXPT: ,
//     FOE: ,
//     HOD: ,
//     ITD: ,
//     PVR: ,
//     PTN: ,
//     VNM: ,
//     WAW: ,
//     'TZE-01': 
// };

// const now = '2026-05';

// function priceFactor(set) {
//     const date = releaseDates[set];
//     const [year, month] = date.split('-').map(n => parseInt(n));
//     const [currentY, currentM] = now.split('-').map(n => parseInt(n));
//     const d = ((currentY - year) * 12 + (currentM - month));
//     return 5 / (d + 5) + Math.sqrt(d) / 6;
// }

document.addEventListener("DOMContentLoaded", main);
async function main() {
    await fetch('https://voyager-mtg.github.io/lists/all-cards.json')
        .then(response => response.json())
        .then(json => {
            card_list = json.cards;
        }).catch(error => console.error('Error:', error));

    await fetch('https:/voyager-api-pq2h.onrender.com/stats')
        .then(response => response.json())
        .then(json => {
            stats = json;
        }).catch(error => console.error('Error:', error));
}

function round5(n) {
    return Math.ceil(n / 5) * 5;
}

function cardPrice(card) {
    // if (card.set == 'LAIR') return 100;
    if (card.type.includes('Basic')) return 0;
    // const card_stats = stats[card.card_name];
    // const weighted_pr = 6 * card_stats.playrate_event + 4 * card_stats.playrate_user;
    // const games_played = sigmoid(card_stats.games_played - 12, 50);
    // const rarity = rarityN[card.rarity];
    // const set_price = setP[card.set];

    // seed = reallyRand(250, seed);
    // console.log(`${card.card_name}\npr: ${2000 * weighted_pr}\ngames: ${1000 * games_played}\nrar: ${1000 * rarity}\nage: ${1000 * set_price}\nrand: -${seed}\nstatic: -1000\n`)
    // const unfilteredPrice = (2000 * weighted_pr + 1000 * games_played + 1000 * rarity + 1000 * set_price - 800 - seed + (isRemoval(card) ? 300 : 0)) * 1.8;
    // return 3000 * rarity;
    return buyValues[card.rarity];
}