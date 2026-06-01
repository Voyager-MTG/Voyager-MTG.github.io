import fs from 'fs';

function sigmoid(x, b = 1) {
    return 1 / (1 + Math.exp((-1 / b) * x));
}

const rarityMult = {
    common: 1,
    uncommon: 4,
    rare: 8,
    mythic: 16
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
    TZE01: "2026-04",
    TDD02: "2026-05",
    ABY: "2026-05",
    LAIR: "2026-01"
};

const now = '2026-06';

function priceFactor(set) {
    const date = releaseDates[set];
    const [year, month] = date.split('-').map(n => parseInt(n));
    const [currentY, currentM] = now.split('-').map(n => parseInt(n));
    const d = ((currentY - year) * 12 + (currentM - month));
    return 1 / (d + 1) + Math.sqrt(d) / 6;
}

async function main() {
    let card_list;
    let set_list;
    let stats;
    await fetch('https://voyager-mtg.github.io/lists/all-cards.json')
        .then(response => response.json())
        .then(json => {
            card_list = json.cards.filter(c => !c.type.match(/Basic|Token/));
        }).catch(error => console.error('Error:', error));

    await fetch('https://voyager-mtg.github.io/lists/all-sets.json')
        .then(response => response.json())
        .then(json => {
            set_list = json.sets;
        }).catch(error => console.error('Error:', error));

    await fetch('https:/voyager-api-pq2h.onrender.com/stats')
        .then(response => response.json())
        .then(json => {
            stats = json;
        }).catch(error => console.error('Error:', error));
    
    let card_prices = [];
    const set_prices = {};
    const set_counts = {};
    const set_names = {};
    const totalWeight = {};
    const weights = {};

    for (const set of set_list) {
        set_counts[set.set_code] = 0;
        set_names[set.set_code] = [];
        weights[set.set_code] = [];
        totalWeight[set.set_code] = 0;
    }

    for (const card of card_list) {
        set_counts[card.set]++;
        set_names[card.set].push(card.card_name);
    }

    for (const set of set_list) {
        const code = set.set_code;

        if (code == 'LAIR') continue;

        let cardFactor = 300;
        if (set.pack) cardFactor = 150;
        if (set.set_code == 'EXPT') cardFactor = 200;
        if (set.set_code == 'ITD') cardFactor = 180;
        const totalPr = Object.entries(stats)
            .filter(([c, s]) => set_names[code].includes(c))
            .reduce((acc, i) => i[1].playrate_event * 3 + i[1].playrate_user + acc, 0);
        const avgPr = totalPr / set_counts[code];

        set_prices[code] = priceFactor(code) * cardFactor * avgPr * 40;
        console.log(code, set_prices[code]);
    }

    for (const card of card_list) {
        if (card.set == 'LAIR') continue;
        const card_stats = stats[card.card_name];
        
        const reprints = card_list.filter(c => c.card_name == card.card_name && c.set != card.set).length || 1;
        const rarityFactor = rarityMult[card.rarity] || 4;
        const demand = card_stats.playrate_user + card_stats.playrate_event * 3 + 0.0025;
        // const K = 0.15;
        const landFactor = card.type.includes('Land') ? 0.5 : 1;

        const cardWeight = rarityFactor * demand * landFactor / reprints;
        // const price = cardWeight * set_prices[card.set];

        const card_id = `${card.card_name} (${card.set}) ${card.number}`;
        totalWeight[card.set] += cardWeight;
        // card_prices.push([card_id, price]);
        weights[card.set].push([card_id, cardWeight]);
    }

    for (const set in weights) {
        for (const [id, weight] of weights[set]) {
            const fraction = weight / totalWeight[set];
            const price = fraction * set_prices[set];
            card_prices.push([id, price]);
        }
    }

    card_prices.sort((a, b) => b[1] - a[1]);
    card_prices = Object.fromEntries(card_prices);

    fs.writeFileSync('out.json', JSON.stringify(card_prices, null, 2));
}

main();