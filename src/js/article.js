let image_bank = {};

function parseMarkdown(md) {
    md = md.replaceAll("\r", "");

    // Name
    md = md.replaceAll(/name: (.*?)\n/g, function (_1, name) {
        document.title = name;
        return "# " + name;
    });

    // Writer
    md = md.replaceAll(/author: (.*?)\n/g, function (_1, author) {
        return "#### Written by " + author;
    });

    // Change preview
    md = md.replaceAll(/<change-preview>\n?(.*?)\n(.*?)\n?<\/change-preview>/gm, function (_1, image_1, image_2) {
        return `<div style="display: grid; grid-template-columns: 1fr 0.1fr 1fr; gap: 10px; align-items: center; justify-items: center; width: 100%;"><img style="max-height: 300px;" src="${image_1}"><span style="font-weight: bold; font-size: 100px;">›</span><img style="max-height: 300px;" src="${image_2}"></div>`;
    });

    // Change preview ban
    md = md.replaceAll(/<change-preview ban>\n?(.*?)\n(.*?)\n?<\/change-preview>/gm, function (_1, image_1, image_2) {
        return `<div style="display: grid; grid-template-columns: 1fr 0.1fr 1fr; gap: 10px; align-items: center; justify-items: center; width: 100%;"><img style="max-height: 300px;" src="${image_1}"><span style="font-weight: bold; font-size: 100px;">›</span><img style="max-height: 300px; filter: grayscale() brightness(0.8);" src="${image_2}"></div>`;
    });

    // Italic bold
    md = md.replaceAll(/\*\*\*(.*?)\*\*\*/g, function (_1, _2) {
        return `<i><b>${_2}</i></b>`;
    });

    // Bold
    md = md.replaceAll(/\*\*(.*?)\*\*/g, function (_1, _2) {
        return `<b>${_2}</b>`;
    });

    // Italic
    md = md.replaceAll(/\*(.*?)\*/g, function (_1, _2) {
        return `<i>${_2}</i>`;
    });

    // Underline
    md = md.replaceAll(/\_\_(.*?)\_\_/g, function (_1, _2) {
        return `<span style="text-decoration: underline;">${_2}</span>`;
    });

    // Strikethrough
    md = md.replaceAll(/\~\~(.*?)\~\~/g, function (_1, _2) {
        return `<span style="text-decoration: line-through;">${_2}</span>`;
    });

    // Links
    md = md.replaceAll(/\[(.*?)\]\((.*?)\)/g, function (_1, _2, _3) {
        return `<a href="${_3}" target="_blank">${_2}</a>`;
    });

    // Headers
    md = md.replaceAll(/(\#+)(.*?)\n/g, function (_1, _2, _3, _4) {
        return `<h${_2.length} id="${_3}">${_3}</h${_2.length}>`;
    });

    // Cards
    md = md.replaceAll(/\[\[(.*?)\]\]/g, function (_1, card_name) {
        return `<span class="card-hover-text" onmouseover="showCardHover('${card_name}')" onmousemove="moveCardHover(event)" onmouseout="hideCardHover()">${card_name}</span>`
    });

    // Card images
    md = md.replaceAll(/\{\{(.*?)\}\}/g, function (_1, card_name) {
        if (!image_bank[card_name]) {
            const card_stats = card_list_arrayified.find(c => c.card_name == card_name);
            image_bank[card_name] = "/sets/" + card_stats.set + "-files/img/" + card_stats.position + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
        }
        console.log(card_name, image_bank[card_name]);
        return `<img class="card-image" src="${image_bank[card_name]}">`
    });

    // Horizontal Line
    md = md.replaceAll(/\-\-\-/g, '<hr></hr>');

    // Linebreaks
    md = md.replaceAll(/\n\n/gm, "<br><br>");

    return `<div class="article-content">${md}</div>`;
}