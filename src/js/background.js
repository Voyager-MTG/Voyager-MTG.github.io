let gradients;

function prepareGradients() {
	let defaultGradient = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt = document.createElement("option");
	opt.value = defaultGradient.replace(' ', '-');
	opt.text = defaultGradient;
	try { document.getElementById("color-select").appendChild(opt); } catch {}
	let random_card = localStorage.getItem("settings.gradient").replace('-', ' ');
	const opt_rand = document.createElement("option");
	opt_rand.value = "Random-Card";
	opt_rand.text = "Random Card";

	try { document.getElementById("color-select").appendChild(opt_rand); } catch {}
	for (const gradient of gradients) {
		const opt = document.createElement("option");
		opt.value = gradient.name.replace(' ', '-');
		opt.text = gradient.name;
		if (gradient.name != defaultGradient) {
			try { document.getElementById("color-select").appendChild(opt); } catch {}
		}
	}

	for (const gradient in card_backgrounds) {
		const opt = document.createElement("option");
		opt.value = gradient.replace(' ', '-');
		opt.text = gradient;
		if (gradient.name != defaultGradient) {
			try { document.getElementById("color-select").appendChild(opt); } catch {}
		}
	}
}

function setGradient(gradient = false) {
	let artistCredit = "";
	if (!gradient) {
		gradient = document.getElementById("color-select").value;
	}

	gradTop = "#000000";
	gradBottom = "#FFFFFF";
	for (const grad of gradients) {
		if (gradient == grad.name.replace(' ', '-')) {
			gradImage = `linear-gradient(to bottom, ${grad.color1}, ${grad.color2})`
		}
	}

	for (const background in card_backgrounds) {
		if (gradient == background.replace(' ', '-')) {
			gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
			artistCredit = card_backgrounds[background][0];
			setTextColor(card_backgrounds[background][1]);
		}
	}

	if (gradient == "Random-Card") {
		const bgs = Object.keys(card_backgrounds);
		const background = bgs[reallyRand(bgs.length)];
		gradImage = `url("/img/backgrounds/${background.toLowerCase()}.jpg")`;
		artistCredit = card_backgrounds[background][0];
		setTextColor(card_backgrounds[background][1]);
	}


	document.body.style.backgroundImage = gradImage;
	localStorage.setItem("settings.gradient", gradient);
	// console.log("CHANGE");
	if (document.getElementsByClassName("artist-credit")[0])
		document.getElementsByClassName("artist-credit")[0].remove();
	const credit_text = document.createElement("span");
	credit_text.className = "artist-credit text";
	credit_text.innerText = `background by ${artistCredit}`;
	if (artistCredit && document.getElementById("color-select"))
		document.getElementById("color-select").parentElement.appendChild(credit_text);
}

function reallyRand(x, seed = false) {
	const date = new Date();
	seed = seed ? seed : date.getUTCFullYear() * 10000 +
		date.getUTCMonth() * 100 +
		date.getUTCDate();

	const a = 1103515245;
	const c = 12345;
	const m = Math.pow(2, 31);

	let randomNumber = (a * seed + c) % m;
	randomNumber = randomNumber / m;

	return Math.floor(randomNumber * x);
}

function setTextColor(c = false) {
	if (c) {
		localStorage.setItem("settings.textcolor", c);
	}
	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));
}

const delay = ms => new Promise(res => setTimeout(res, ms));

function defaultSetting(name, default_) {
	// if you dont have a value in localstorage, set that value to default_
	if (localStorage.getItem(name) == null) {
		localStorage.setItem(name, default_);
	}
}

function toggleHeader() {
	const header = document.querySelector('.header');
	header.style.transform = header.style.transform === '' ? 'translate(0)' : '';
}

document.addEventListener("DOMContentLoaded", async () => {
	defaultSetting('settings.autosave', 'On');
	defaultSetting('settings.searchalias', 'On');
	defaultSetting('settings.exportcube', 'On');
	defaultSetting('settings.maxcopies', 'On');
	defaultSetting('settings.sanctumbasic', 'On');
	defaultSetting('settings.textcolor', 'Black');
	defaultSetting('settings.gradient', 'Random-Card');
	defaultSetting('settings.format', 'Eternal');
	defaultSetting('settings.deck_privacy', 'Public');
	defaultSetting("settings.compactaccount", "Off");
	defaultSetting("settings.resultgradient", "On");
	defaultSetting("settings.darktheme", "Off");
	defaultSetting("settings.theme", "Light");

	let theme = localStorage.getItem("settings.theme");

	if (!theme && localStorage.getItem("settings.darkthememenu") == "On") {
		theme = "Dark";
	}
	if (!theme && localStorage.getItem("settings.darkthememenu") == "Off") {
		theme = "Light";
	}

	document.body.dataset.theme = theme;

	document.body.style.setProperty("--text-color", localStorage.getItem("settings.textcolor"));

	try {
		const response = await fetch('/data/gradients.json');
		raw_gradients = await response.json();
	}
	catch (error) {
		console.error('Error:', error);
	}

	gradients = raw_gradients.gradients;
	card_backgrounds = raw_gradients.cards;
	setGradient(localStorage.getItem("settings.gradient"));
	prepareGradients();

	handleDeckView();

	if (window.location.href.includes('#nobg')) {
		document.body.style.background = 'rgba(0,0,0,0)';
		document.querySelector('.header').style.display = 'none';
		document.getElementById("color-select").style.display = 'none';
		if (document.getElementsByClassName("artist-credit")[0])
			document.getElementsByClassName("artist-credit")[0].remove();
	}
});

async function handleDeckView() {
	const deckview_container = document.createElement('div');
	deckview_container.className = 'deck-view-container';

	deckview_container.appendChild(createDeckView());

	const deckview = document.createElement('div');
	deckview.className = 'deck-view';

	const pop_out_button = document.createElement('div');
	pop_out_button.className = 'open-deckview-button';
	pop_out_button.innerText = '⮝';
	pop_out_button.onclick = async () => {
		const is_expanded = localStorage.getItem('settings.deckexpanded') != 'true';
		localStorage.setItem('settings.deckexpanded', is_expanded);
		if (is_expanded) { 
			deckview.style.display = 'block';
			await delay(10)
			pop_out_button.innerText = '⮟';
		}
		deckview.style.transform = is_expanded ? 'translate(0, 12vh)' : 'translate(0, 70vh)';
		if (!is_expanded) { 
			pop_out_button.innerText = '⮝';
			await delay(500);
			deckview.style.display = 'none';
		}
	}
	
	deckview_container.appendChild(deckview);
	deckview_container.appendChild(pop_out_button);
	document.body.appendChild(deckview_container);

	const is_expanded = localStorage.getItem('settings.deckexpanded') == 'true';
	if (is_expanded) {
		deckview.style.display = 'block';
		await delay(10);
		deckview.style.transform ='translate(0, 12vh)';
		pop_out_button.innerText = '⮟';
	}
}

function createDeckView() {
	const deck_name = localStorage.getItem('info.lastdeck');
	const deck = localStorage.getItem(deck_name);
	console.log(deck);
	return document.createElement('div');
}

function readDeckText(text, name) {
	document.getElementById("deck-name").value = name || 'Untitled Deck';

	deck = [];
	sideboard = [];
	sanctum = [];
	sb_cards = false;
	sc_cards = false;
	cockatrice_file = false;

	const lines = text.split('\n');

	let deck_map = new Map();
	let sb_map = new Map();
	let sc_map = new Map();

	for (let line of lines) {
		if (line.startsWith('//')) {
			cockatrice_file = true;
			continue;
		};
		if (line.startsWith('SB:')) {
			if (!sb_cards) sb_cards = true;
			line = line.split('SB: ')[1];
		} 
		if (line == 'sideboard' || (line == '' && !cockatrice_file)) // '' for Draftmancer files
		{
			sb_cards = true;
		}
		else if (line == 'sanctum' || (sb_cards && line == '')) // '' for Draftmancer files
		{
			sc_cards = true;
			sb_cards = false;
		}
		else if (!sb_cards && !sc_cards) {
			// get the count and card name
			count = parseInt(line.substring(0, line.indexOf(' ')));
			card_name = line.substring(line.indexOf(' ') + 1).split(" (")[0];
			card_set = line.match(/[0-9]+ .*? \((.*?)\)/);
			card_num = line.match(/[0-9]+ .*? \(.*?\) ([0-9]+)/);

			card_set = card_set == null ? "XXX" : card_set[1];
			card_num = card_num == null ? "0" : card_num[1];
			
			if (deck_map.has([card_name, card_set, card_num])) // if the deck has card name, add the new value, if it doesnt, set the value to stop keyerrors
			{
				deck_map.set([card_name, card_set, card_num], deck_map.get(card_name) + count);
			}
			else {
				deck_map.set([card_name, card_set, card_num], count);
			}
		}
		else if (sb_cards) // sideboard cards, do the same thing but with sb_map
		{
			count = parseInt(line.substring(0, line.indexOf(' ')));
			card_name = line.substring(line.indexOf(' ') + 1).split(" (")[0];
			card_set = line.match(/[0-9]+ .*? \((.*?)\)/);
			card_num = line.match(/[0-9]+ .*? \(.*?\) ([0-9]+)/);

			card_set = card_set == null ? "XXX" : card_set[1];
			card_num = card_num == null ? "0" : card_num[1];

			if (sb_map.has([card_name, card_set, card_num])) {
				sb_map.set([card_name, card_set, card_num], sb_map.get(card_name) + count);
			}
			else {
				sb_map.set([card_name, card_set, card_num], count);
			}
		} else if (sc_cards) // sanctum cards, do the same thing but with sc_map
		{
			count = parseInt(line.substring(0, line.indexOf(' ')));
			card_name = line.substring(line.indexOf(' ') + 1).split(" (")[0];
			card_set = line.match(/[0-9]+ .*? \((.*?)\)/);
			card_num = line.match(/[0-9]+ .*? \(.*?\) ([0-9]+)/);

			card_set = card_set == null ? "XXX" : card_set[1];
			card_num = card_num == null ? "0" : card_num[1];

			if (sc_map.has([card_name, card_set, card_num])) {
				sc_map.set([card_name, card_set, card_num], sc_map.get(card_name) + count);
			}
			else {
				sc_map.set([card_name, card_set, card_num], count);
			}
		}
	}

	for (const card of card_list_arrayified) {
		for (const [ key, value ] of deck_map.entries()) {
			if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX") && (key[2] == card.number.toString() || key[2] == "0")) {
				for (let i = 0; i < value; i++) {
					addCardToDeck(JSON.stringify(card), false);
				}
				deck_map.delete(key);
			}
		}

		for (const [ key, value ] of sb_map.entries()) {
			if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX") && (key[2] == card.number.toString() || key[2] == "0")) {
				for (let i = 0; i < value; i++) {
					addCardToSideboard(JSON.stringify(card), false);
				}
				sb_map.delete(key);
			}
		}

		for (const [ key, value ] of sc_map.entries()) {
			if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX") && (key[2] == card.number.toString() || key[2] == "0")) {
				for (let i = 0; i < value; i++) {
					addCardToSanctum(JSON.stringify(card), false);
				}
				sc_map.delete(key);
			}
		}
	}

	if (deck_map.size > 1 || sb_map.size > 1 || sc_map.size > 1) {
		for (const card of card_list_arrayified) {
			for (const [ key, value ] of deck_map.entries()) {
				if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX")) {
					for (let i = 0; i < value; i++) {
						addCardToDeck(JSON.stringify(card), false);
					}
					deck_map.delete(key);
				}
			}

			for (const [ key, value ] of sb_map.entries()) {
				if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX")) {
					for (let i = 0; i < value; i++) {
						addCardToSideboard(JSON.stringify(card), false);
					}
					sb_map.delete(key);
				}
			}

			for (const [ key, value ] of sc_map.entries()) {
				if (key[0] == card.card_name && (key[1] == card.set || key[1] == "XXX")) {
					for (let i = 0; i < value; i++) {
						addCardToSanctum(JSON.stringify(card), false);
					}
					sc_map.delete(key);
				}
			}
		}
	}

	if (deck_map.size > 1 || sb_map.size > 1 || sc_map.size > 1) {
		for (const card of card_list_arrayified) {
				for (const [ key, value ] of deck_map.entries()) {
				if (key[0] == card.card_name) {
					for (let i = 0; i < value; i++) {
						addCardToDeck(JSON.stringify(card), false);
					}
					deck_map.delete(key);
				}
			}

			for (const [ key, value ] of sb_map.entries()) {
				if (key[0] == card.card_name) {
					for (let i = 0; i < value; i++) {
						addCardToSideboard(JSON.stringify(card), false);
					}
					sb_map.delete(key);
				}
			}

			for (const [ key, value ] of sc_map.entries()) {
				if (key[0] == card.card_name) {
					for (let i = 0; i < value; i++) {
						addCardToSanctum(JSON.stringify(card), false);
					}
					sc_map.delete(key);
				}
			}
		}
	}
	
	document.getElementById("modal-container").style.display = "none";
	document.getElementById("file-menu").value = "default";

	processDeck();
}

function processDeck() {
	const display_style = document.getElementById("display-select").value;
	if (display_style != "stats") {
		document.getElementsByClassName("deck-cards-container")[0].innerHTML = deck_cards_html;
	}

	if (localStorage.getItem("settings.resultgradient") == "Off") {
		document.getElementsByClassName("search-image-gradient")[0].style.display = "none";
	} else if (localStorage.getItem("settings.darkthememenu") == "On") {
		document.getElementsByClassName("search-image-gradient")[0].style.display = "block";
	}

	if (localStorage.getItem("settings.scrollbar") == "On") {
		document.getElementsByClassName("search-image-grid-container")[0].style.scrollbarWidth = "auto";
	} else if (localStorage.getItem("settings.scrollbar") == "Off") {
		document.getElementsByClassName("search-image-grid-container")[0].style.scrollbarWidth = "none";
	}

	// add the no-cards-text if there's no cards in the deck or sideboard, otherwise hide it
	const nct = document.getElementById("no-cards-text");
	nct.style.display = (deck.length == 0 && sideboard.length == 0 && sanctum.length == 0) ? "block" : "none";

	// set the deck count thing in the deck header
	const dc = document.getElementById("deck-count");
	dc.innerText = "(" + deck.length + " / " + sideboard.length + " / " + sanctum.length + ")";

	// initialize card types (and sideboard, sanctum)
	let deck_cards = new Map([
		['land', new Map([])],
		['creature', new Map([])],
		['instant', new Map([])],
		['planeswalker', new Map([])],
		['artifact', new Map([])],
		['enchantment', new Map([])],
		['sorcery', new Map([])],
		['battle', new Map([])],
		['other', new Map([])],
		['sideboard', new Map([])],
		['sanctum', new Map([])]
	]);

	for (const card of deck) {
		// loop through each card and get the cardtype
		card_type = JSON.parse(card).type.toLowerCase();

		let not_found = true;
		for (const [key, map] of deck_cards) {
			if (card_type.includes(key)) {
				if (map.has(card)) {
					map.set(card, map.get(card) + 1);
				}
				else {
					map.set(card, 1);
				}

				not_found = false;
				break;
			}
		}
		if (not_found) {
			let map = deck_cards.get("other");
			if (map.has(card)) {
				map.set(card, map.get(card) + 1);
			}
			else {
				map.set(card, 1);
			}
		}
	}
	for (const card of sideboard) {
		// loop through the sideboard and assign the cards to the map
		let map = deck_cards.get("sideboard");
		if (map.has(card)) {
			map.set(card, map.get(card) + 1);
		}
		else {
			map.set(card, 1);
		}
	}
	for (const card of sanctum) {
		// loop through the sanctum and assign the cards to the map
		let map = deck_cards.get("sanctum");
		if (map.has(card)) {
			map.set(card, map.get(card) + 1);
		}
		else {
			map.set(card, 1);
		}
	}

	for (const [key, map] of deck_cards) {
		// assign the id based on the card type, then get the container div
		deck_section_id = "deck-" + key;
		outer_ele = document.getElementById(deck_section_id);

		if (map.size == 0) // if the card type has no cards in the deck, hide the element
		{
			outer_ele.style.display = "none";
		}
		else {
			// if it does have cards, make the display grid and get both the cards and title element
			outer_ele.style.display = "grid";
			deck_section_cards_id = deck_section_id + "-cards";
			deck_section_title_id = deck_section_id + "-title";
			title_ele = document.getElementById(deck_section_title_id);

			title_ele.style.color = localStorage.getItem('settings.textcolor');

			// get the number of copies of the card type and add it to the title
			let count = 0;
			for (const val of Array.from(map.values())) {
				count += val;
			}
			const numregex = /[0-9]+/;
			title_ele.innerText = title_ele.innerText.replace(numregex, count);

			// get the cards section and and reset its html
			cards_ele = document.getElementById(deck_section_cards_id);
			cards_ele.innerHTML = "";
			const sort_order = localStorage.getItem('settings.deck_sort') || 'Name';
			const cards_list = Array.from(map.keys()).map(c => JSON.parse(c)).sort((a, b) => {
				if (sort_order == 'Name') return a.card_name.localeCompare(b.card_name);
				if (sort_order == 'Mana value') return convertToMV(a.cost) - convertToMV(b.cost);
				if (sort_order == 'Color') return sortColor(a, b);
			});
			// console.log(Array.from(map.keys()));
			// const cards_list = Array.from(map.keys()).sort();
			for (const card_stats of cards_list) {
				// loop through each card in the deck with the card type
				// get the display style (text or image), the card json, and the name
				const card_name = card_stats.card_name;
				const card = JSON.stringify(card_stats);

				if (display_style == "text") // if text is selected as the display mode
				{
					generateCardHTML("text", map, card, key, card_stats, cards_list);
				}
				else if (display_style == "images") // the display style is image
				{
					generateCardHTML("image", map, card, key, card_stats, cards_list);
				}
			}
		}
	}
	if (display_style == "stats") {
		document.getElementsByClassName("deck-cards-container")[0].innerHTML = "";
		makeStatsTab(deck_cards);
	}
}

function generateCardHTML(display_style, map, card, key, card_stats, cards_list) {
	const card_name = card_stats.card_name;
	// make a div for the card line (will contain the name, copies, and - button)
	card_row = document.createElement("div");
	card_row.className = "deck-line";

	card_in_deck = document.createElement("div"); // make a div
	card_in_deck.innerText += map.get(card) + " " + card_name + "\n"; // add the card name to it
	card_in_deck.style.cursor = "pointer"; // make the cursor style pointer

	if (display_style == "text") {
		card_in_deck = document.createElement("div"); // make a div
		card_in_deck.innerText += map.get(card) + " " + card_name + "\n"; // add the card name to it
		card_in_deck.style.cursor = "pointer"; // make the cursor style pointer
		// card_in_deck.onmouseover = updateCardGrid(card_stats);
		card_in_deck.style.color = localStorage.getItem("settings.textcolor");
	} else if (display_style == "image") {
		// make the card image container div & give it the class
		card_row = document.createElement("div");
		card_row.className = "card-img-container";
		// if its the last one, give it auto height and 100% maxheight
		if (card == cards_list[cards_list.length - 1]) {
			card_row.style.height = "auto";
			card_row.style.maxHeight = "100%";
		}

		// make an image element and give it the correct url
		card_in_deck = document.createElement("img");
		card_in_deck.src = "/sets/" + card_stats.set + "-files/img/" + card_stats.number + "_" + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
		card_in_deck.style.borderRadius = "8px";
		// card_in_deck.onmouseover = updateCardGrid(card_stats);

		card_count = document.createElement("div");
		card_count.innerText = map.get(card) + "x";
		card_count.className = "card-fx";
		if (localStorage.getItem("settings.textcolor") == "On") {
			card_count.style.color = "black";
		} else {
			card_count.style.color = "white";
		}
	}

	// create an image with the class icon, add the pointer cursor style, this is the delete button
	del_btn = document.createElement("img");
	del_btn.className = "icon";
	del_btn.style.cursor = "pointer";

	// do the same for the add button
	add_btn = document.createElement("img");
	add_btn.className = "icon";
	add_btn.style.cursor = "pointer";
	if (key == "sideboard") {
		// if its the sideboard, add the sideboard delete button and setup the onclick accordingly
		del_btn.src = "/img/deckbuilder/sb-delete.png";
		del_btn.onclick = function () {
			sideboard.splice(sideboard.indexOf(card), 1);
			processDeck();
		}

		// if its the sideboard, add the sideboard add button and setup the onclick accordingly
		add_btn.src = "/img/deckbuilder/sb-add.png";
		add_btn.onclick = function () {
			addCardToSideboard(card);
			processDeck();
		}

		card_in_deck.onclick = function () {
			openCardModal(card_stats, "sideboard");
		}

		// when a card in the sideboard is clicked, remove it from the sideboard and add it to the maindeck
		card_in_deck.oncontextmenu = function (event) {
			event.preventDefault();
			sideboard.splice(sideboard.indexOf(card), 1);
			let parsed_card = JSON.parse(card);
			addCardToDeck(card);
		}
	} else if (key == "sanctum") {
		// if its the sanctum, add the sideboard delete button and setup the onclick accordingly
		del_btn.src = "/img/deckbuilder/sb-delete.png";
		del_btn.onclick = function () {
			sanctum.splice(sanctum.indexOf(card), 1);
			processDeck();
		}

		// if its the sanctum, add the sideboard add button and setup the onclick accordingly
		add_btn.src = "/img/deckbuilder/sb-add.png";
		add_btn.onclick = function () {
			addCardToSanctum(card);
		}

		card_in_deck.onclick = function () {
			openCardModal(card_stats, "sanctum");
		}

		// when a card in the sanctum is clicked, remove it from the sanctum and add it to the maindeck
		card_in_deck.oncontextmenu = function (event) {
			event.preventDefault();
			sanctum.splice(sanctum.indexOf(card), 1);
			let parsed_card = JSON.parse(card);
			addCardToDeck(card);
		}
	}
	else {
		// make the delete button have the normal delete image
		del_btn.src = "/img/deckbuilder/delete.png";
		add_btn.src = "/img/deckbuilder/add.png";
		let card_parsed = JSON.parse(card);
		del_btn.onclick = function () {
			deck.splice(deck.indexOf(card), 1);
			processDeck();
		}

		// do the same for the add button
		add_btn.onclick = function () {
			addCardToDeck(card);
			processDeck();
		}

		card_in_deck.onclick = function () {
			openCardModal(card_stats, "deck");
		}

		// when a card in the deck is clicked, remove it from the deck and add it to the sideboard
		card_in_deck.oncontextmenu = function (event) {
			event.preventDefault();
			deck.splice(deck.indexOf(card), 1);
			addCardToSideboard(card);
			processDeck();
		}
	}

	card_in_deck.onmouseover = () => {
		hover_card.src = "/sets/" + card_stats.set + "-files/img/" + card_stats.number + "_" + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
		hover_card.style.display = 'block';
	}

	card_in_deck.onmousemove = event => {
		hover_card.style.left = event.pageX + "px";
		const cardHeight = 523 * window.getComputedStyle(hover_card).getPropertyValue('--scale');
		const posY = event.pageY - cardHeight;
		const bottom = event.pageY + cardHeight;
		hover_card.style.top = bottom > window.innerHeight ? posY : event.pageY;
	}

	card_in_deck.onmouseout = () => {
		hover_card.style.display = '';
	}

	// card_img_container.appendChild(db_container);
	// card_img_container.appendChild(card_count);
	// card_img_container.appendChild(card_img);
	// cards_ele.appendChild(card_img_container);

	// make a container div with the card-fx class and add the delete button to it, do the same for the add button
	db_container = document.createElement("div");
	db_container.className = "card-fx";
	ab_container = document.createElement("div");
	ab_container.className = "card-fx";
	db_container.appendChild(del_btn);
	ab_container.appendChild(add_btn);

	// add all of our elements to the card_row and cards_ele elements
	card_row.appendChild(db_container);
	card_row.appendChild(ab_container);
	if (display_style == "image") card_row.appendChild(card_count);
	card_row.appendChild(card_in_deck);
	// sanctum stuff, similar to delete button
	if (display_style == "text" && localStorage.getItem("settings.sanctumsym") == "On") {
		let sanctum_coll = JSON.parse(localStorage.getItem("colls.collections"))["Sanctum cards"];
		for (card_ of sanctum_coll) {
			if ((card_stats.card_name == card_.substring(card_.indexOf(' ') + 1, card_.length)) && (!card_stats.type.includes("Basic") || localStorage.getItem("settings.sanctumbasic") == "On")) {
				sanctum_container = document.createElement("div");
				sanctum_container.className = "card-fx sanctum-img";
				sanctum_img = document.createElement("img");
				sanctum_img.className = "icon";
				sanctum_img.src = "/img/sanctum.png";
				sanctum_container.appendChild(sanctum_img);
				card_row.appendChild(sanctum_container);
				break;
			}
		}
	}
	cards_ele.appendChild(card_row);
}

function closeModal() {
	document.getElementById("modal-container").style.display = "none";
}