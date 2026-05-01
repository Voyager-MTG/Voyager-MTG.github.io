import fs from 'fs';

function sigmoid(x, b = 1) {
    return 1 / (1 + Math.exp((-1 / b) * x));
}

const rarityN = {
    common: 0.1,
    uncommon: 0.25,
    rare: 0.75,
    mythic: 1
};

const releaseDates = {
    AKT: "2025-02",
    EXPT: "2025-02",
    FOE: "2025-08",
    HOD: "2025-02",
    ITD: "2025-02",
    PVR: "2025-02",
    PTN: "2025-02",
    VNM: "2025-02",
    WAW: "2025-02",
    'TZE-01': "2026-03"
};

const now = '2026-05';

function priceFactor(set) {
    const date = releaseDates[set];
    const [year, month] = date.split('-').map(n => parseInt(n));
    const [currentY, currentM] = now.split('-').map(n => parseInt(n));
    const d = ((currentY - year) * 12 + (currentM - month));
    return 1 / (d + 1) + Math.sqrt(d) / 5;
}

async function main() {
    let card_list;
    let stats;
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
    
    let card_prices = [];

    for (const card of card_list) {
        if (card.set == 'LAIR') continue;
        const card_stats = stats[card.card_name];
        const weighted_pr = 6 * card_stats.playrate_event + 4 * card_stats.playrate_user;
        const games_played = sigmoid(card_stats.games_played, 50);
        const rarity = rarityN[card.rarity];
        const age = priceFactor(card.set);
        const res = Math.floor(500 * weighted_pr + 200 * games_played + 2000 * rarity + 1000 * age + Math.random() * 250);
        card_prices.push([card.card_name, res]);
    }

    card_prices.sort((a, b) => a[1] - b[1]);

    fs.writeFileSync('out.json', JSON.stringify(card_prices, null, 2));
}

main();