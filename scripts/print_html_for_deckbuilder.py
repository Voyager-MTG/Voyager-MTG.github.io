import os
import sys

def generateHTML(codes):
	output_html_file = "deckbuilder.html"

	# Start creating the HTML file content
	html_content = '''<html>
<head>
	<title>Deckbuilder</title>
	<link rel="icon" type="image/x-icon" href="/img/deck.png">
	<link rel="stylesheet" href="resources/mana.css">
	<link rel="stylesheet" href="/resources/header.css">
</head>
<style>
	@font-face {
		font-family: Beleren;
		src: url('/resources/beleren.ttf');
	}
	body {
		font-family: 'Helvetica', 'Arial', sans-serif;
		overscroll-behavior: none;
		margin: 0px;
		background-color: #bbbbbb;
		display: block;
	}
	.page-container {
		width: 2000px;
		max-width: 98%;
		height: 89%;
		padding-top: 10px;
		display: grid;
		grid-template-columns: 3fr 2fr;
		margin: auto;
		gap: 5px;
	}
	.deckbuilder-container {
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
		gap: 5px;
	}
	.search-results-container {
		display: grid;
		grid-template-columns: 3fr 2fr;
		overflow-y: hidden;
		overflow-x: hidden;
		height: 100%;
	}
	.search-container {
		height: 100%;
		border: 1px solid #d5d9d9;
		border-top: 4px solid #171717;
		border-bottom: 4px solid #171717;
		background-color: #f3f3f3;
		border-radius: 6px;
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
	}
	.deckbuilder-search-grid {
		width: 80%;
		max-width: 1200px;
		min-height: 36px;
		display: grid;
		grid-template-columns: 4fr 1fr;
		gap: 8px;
		padding: 5px 10%;
		border-bottom: 1px solid #898989;
		justify-items: center;
		align-items: center;
	}
	input {
		width: 100%;
		height: 35px;
		font-size: 16px;
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 2px;
		padding-left: 10px;
		padding-right: 10px;
		-webkit-box-sizing: border-box;
		-moz-box-sizing: border-box;
		box-sizing: border-box;
	}
	input:focus {
		outline-color: #4f4f4f;
	}
	button {
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 8px;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		color: #171717;
		cursor: pointer;
		font-size: 13px;
		width: 100%;
		height: 35px;
		min-width: 85px;
	}
	button:hover {
		background-color: #ffffff;
	}
	button:focus {
		border-color: #171717;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		outline: 0;
	}
	button:disabled {
		cursor: auto;
		background-color: #f7fafa;
		font-style: italic;
		box-shadow: none;
		color: #cccccc;
	}
	.deckbuilder-search-grid .select-text {
		width: 100%;
		display: flex;
		align-items: center;
		justify-content: left;
		gap: 4px;
		font-size: 14.5px;
		text-align: center;
	}
	select {
		background-color: #fafafa;
		border: 1px solid #d5d9d9;
		border-radius: 8px;
		box-shadow: rgba(213, 217, 217, .5) 0 2px 5px 0;
		text-align: center;
		color: #171717;
		font-size: 13px;
		height: 30px;
	}
	select:focus {
		outline-color: #4f4f4f;
	}
	.search-image-grid-container {
		overflow-y: scroll;
		scrollbar-width: none;
	}
	.search-image-grid {
		display: grid;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		width: 98%;
		height: fit-content;
		gap: 3px;
		justify-items: center;
		padding: 8px 1%;
	}
	@media ( max-width: 750px ) {
		.image-grid {
			grid-template-columns: 1fr 1fr;	
		}
	}
	.image-grid {
		display: flex;
		flex-direction: column;
		height: 100%;
	}
	.card-text {
		border-top: 3px solid #171717;
		overflow-y: scroll;
		scrollbar-width: none;
		height: 50%;
	}
	.card-text div {
		white-space: normal;
		font-size: 13px;
		padding-bottom: 10px;
		padding-left: 12px;
		padding-right: 12px;
		line-height: 155%;
	}
	.card-text .name-cost {
		font-weight: bold;
		font-size: 16px;
		white-space: pre-wrap;
		padding-top: 10px;
	}
	.card-text .type {
		font-size: 14px;
	}
	.card-text .pt {
		font-weight: bold;
	}
	.card-text br {
		content: "";
		display: block;
		margin-bottom: 5px;
	}
	.img-container {
		position: relative;
		align-self: center;
		text-align: center;
	}
	.img-container img {
		width: 100%;
		height: auto;
	}
	.img-container .btn {
		background: url('img/flip.png') no-repeat;
		background-size: contain;
		background-position: center;
		width: 15%;
		height: 11%;
		cursor: pointer;
		border: none;
		position: absolute;
		top: 6.5%;
		left: 8.5%;
		transform: translate(-50%, -85%);
		border-radius: 0px;
		box-shadow: none;
	}
	.img-container .btn:hover {
		background: url('img/flip-hover.png') no-repeat;
		background-size: contain;
		background-position: center;
	}
	.img-container .hidden-text {
		position: absolute;
		font-family: Beleren;
		top: 5%;
		left: 9%;
		font-size: .97vw;
		color: rgba(0, 0, 0, 0);
	}
	.card-grid-container {
		border-left: 1px solid #d5d9d9;
		width: 100%;
		height: 100%;
		overflow-y: hidden;
	}
	.card-grid-container .img-container {
		width: 100%;
		height: 50%;
		padding: 10px 0;
	}
	.img-container a {
		height: 100%;
		max-width: 80%;
		display: grid;
		justify-self: center;
	}
	.img-container a > * {
		grid-row: 1;
		grid-column: 1;
	}
	.card-grid-container img {
		width: auto;
		min-width: 0;
		max-width: 100%;
		height: auto;
		min-height: 0;
		max-height: 100%;
		display: block;
		margin: auto;
	}
	.card-grid-container .btn {
		left: 50%;
		top: 48%;
		transform: translate(-50%, -50%);
		opacity: 0.5;
	}
	.hidden {
		display: none;
	}
	.no-cards-text {
		position: absolute;
		top: 50%;
		left: 50%;
		transform: translate(-50%, -50%);
		width: 100%;
		text-align: center;
		font-style: italic;
		color: #494949;
	}
	.deck-container {
		height: 100%;
		border: 1px solid #d5d9d9;
		border-top: 4px solid #171717;
		border-bottom: 4px solid #171717;
		background-color: #f3f3f3;
		border-radius: 6px;
		display: flex;
		flex-direction: column;
		overflow-y: hidden;
		position: relative;
	}
	.deck-info-grid {
		width: 95%;
		max-width: 1200px;
		min-height: 36px;
		display: grid;
		grid-template-columns: 1.5fr .65fr .75fr .5fr .75fr;
		gap: 3px;
		padding: 5px 2.5%;
		border-bottom: 1px solid #898989;
		justify-items: center;
		align-items: center;
	}
	.deck-info-grid select {
		width: 100%;
	}
	.deck-count {
		font-weight: bold;
	}
	.static-deck-container {
		height: 100%;
		overflow-y: hidden;
	}
	.deck-cards-container {
		display: grid;
		grid-template-columns: 1fr 1fr;
		overflow-y: scroll;
		scrollbar-width: none;
		font-size: 14px;
		height: 100%;
	}
	.deck-container span {
		font-size: 15px;
		font-weight: bold;
		padding-top: 10px;
		padding-bottom: 5px;
		padding-left: 22px;
	}
	.deck-container .icon {
		width: 60%;
	}
	.deck-section {
		display: none;
	}
	.deck-inner-section {
		padding-bottom: 10px;
		line-height: 1.5;
	}
	.deck-line {
		border-top: 1px solid #d5d9d9;
		display: grid;
		grid-template-columns: 1fr 13fr;
		gap: 5px;
		align-items: center;
	}
	.deck-col {
		padding: 0 15px;
		height: 100%;
	}
	.card-img-container {
		height: 2.1vw;
		max-height: 45px;
		display: grid;
		grid-template-columns: 1fr 2fr 12fr;
		gap: 2px;
		font-weight: bold;
		line-height: 1;
	}
	.card-img-container img {
		width: 100%;
	}
	.card-fx {
		display: grid;
		align-items: center;
		justify-items: center;
		text-align: center;
	}
	.card-img-container .card-fx {
		height: 2.7vw;
		max-height: 63px;
	}
	.img-container .h-img {
		transform: rotate(90deg);
		width: 85%;
	}
	.rc-menu {
		display: none;
		position: absolute;
		background-color: #f3f3f3;
		border-top: 1px solid #d5d9d9;
		box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
		z-index: 2;
		font-size: 12px;
	}
	.rc-menu ul {
		list-style: none;
		padding: 0;
		margin: 0;
	}
	.rc-menu li {
		padding: 8px 12px;
		border: 1px solid #d5d9d9;
		border-top: none;
		cursor: pointer;
	}
	.rc-menu li:hover {
		background-color: #ffffff;
	}
	.search-grid {
		justify-content: center;
	}
	.sg-icon {
		cursor: pointer;
	}
	.load-modal-container {
		display: none; 
		position: fixed; 
		z-index: 1; 
		padding-top: 100px;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto; 
		background-color: rgb(0,0,0); 
		background-color: rgba(0,0,0,0.4); 
	}
	.load-modal-content {
		background-color: #fefefe;
		margin: auto;
		padding: 20px;
		border: 1px solid #888;
		width: 80%;
	}
	.close {
		color: #aaaaaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}
	.close:hover,
	.close:focus {
		color: #000;
		text-decoration: none;
		cursor: pointer;
	}
	#modal-container {
		display: none; 
		position: fixed; 
		z-index: 1; 
		padding-top: 100px;
		left: 0;
		top: 0;
		width: 100%;
		height: 100%;
		overflow: auto; 
		background-color: rgb(0,0,0); 
		background-color: rgba(0,0,0,0.4); 
	}
	#modal-content {
		background-color: #fefefe;
		margin: auto;
		padding: 20px;
		border: 1px solid #888;
		width: 80%;
	}
	.close {
		color: #aaaaaa;
		float: right;
		font-size: 28px;
		font-weight: bold;
	}
	.close:hover,
	.close:focus {
		color: #000;
		text-decoration: none;
		cursor: pointer;
	}
	.load-btn {
		color: #fff;
		background-color: rgba(14, 126, 246, 1);
		padding: 10px;
		margin: 10px;
		display: inline-block;
		margin-bottom: 3px;
		margin-top: 3px;
	}
	.del-btn {
		color: #fff;
		background-color: rgb(215, 69, 59);
		padding: 10px;
		margin: 10px;
		display: inline-block;
		margin-bottom: 3px;
		margin-top: 3px;
	}
	.name-cost {
		font-family: beleren;
	}
	.settings-dropdown {
		margin-right: 15px;
	}
</style>
<body>
	<div class="header">
		<div class="search-grid">
			<a href="/"><img class="sg-logo" src="/img/banner.png"></a>
			<img class="sg-icon" src="/img/search.png" onclick="goToSearch()">
			<a href="/all-sets"><img src="/img/sets.png" class="sg-icon">Sets</a>
			<a href="/deckbuilder"><img src="/img/deck.png" class="sg-icon">Deckbuilder</a>
			<a onclick="randomCard()"><img src="/img/random.png" class="sg-icon">Random</a>
		</div>
	</div>
	<div id="myContextMenu" class="rc-menu">
		<ul>
			<li id="add-to-deck">Add to Deck</li>
			<li id="add-to-sideboard">Add to Sideboard</li>
		</ul>
	</div>
	<input type="text" id="display" class="hidden" value="cards-and-text"> <!-- here to make img-container-defs snippet work properly -->
	<div class="page-container">
		<div class="search-container">
			<div class="deckbuilder-search-grid">
				<input type="text" inputmode="search" placeholder="Search ..." name="search" id="search" spellcheck="false" autocomplete="off" autocorrect="off" spellcheck="false">
				<div class="select-text">
					<select name="sort-by" id="sort-by">
						<option value="name">Name</option>
						<option value="set-code">Set / Number</option>
						<option value="mv">Mana Value</option>
						<option value="color">Color</option>
						<option value="rarity">Rarity</option>
					</select>:<select name="sort-order" id="sort-order">
						<option value="ascending">Asc</option>
						<option value="descending">Desc</option>
					</select>
				</div>
			</div>
			<div class="search-results-container">
				<div class="search-image-grid-container">
					<div class="search-image-grid" id="imagesOnlyGrid">
					</div>
				</div>
				<div class="card-grid-container" id="card-grid-container">
				</div>
			</div>
		</div>
		<div class="deck-container">
			<div class="no-cards-text" id="no-cards-text">
				Click on a card to add it to the deck
			</div>
			<div class="deck-info-grid">
				<input type="text" value="Untitled Deck" id="deck-name" spellcheck="false" autocomplete="off" autocorrect="off" spellcheck="false">
				<div id="deck-count" class="deck-count">
					(0 / 0)
				</div>
				<select name="display-select" class="display-select" id="display-select">
					<option value="text">Text</option>
					<option value="images">Images</option>
				</select>
				<div></div> <!-- empty div for spacing -->
				<select name="file-menu" class="file-menu" id="file-menu">
					<option value="default">Actions ...</option>
					<option value="settings">Settings</option>
					<option value="new">New deck</option>
					<option value="import">Import deck</option>
					<option value="save-collection">Save as collection</option>
					<option value="load-collection">Load collection</option>
					<option value="save">Save deck</option>
					<option value="load">Load deck</option>
					<option value="delete">Delete saved deck</option>
					<option value="get-url">Get deck URL</option>
					<option value="copy">Copy decklist</option>
					<option value="export-dek">Export .dek</option>
					<option value="export-txt">Export .txt</option>
					<option value="draftmancer">Export Draftmancer File</option>
				</select>
				<input type="file" class="hidden" id="import-file" onclick="this.value=null;">
			</div>
			<div class="static-deck-container">
				<div class="deck-cards-container">
					<div class="deck-col" id="col1">
						<div class="deck-section" id="deck-creature">
							<span id="deck-creature-title">Creatures (0)</span>
							<div class="deck-inner-section" id="deck-creature-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-planeswalker">
							<span id="deck-planeswalker-title">Planeswalkers (0)</span>
							<div class="deck-inner-section" id="deck-planeswalker-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-artifact">
							<span id="deck-artifact-title">Artifacts (0)</span>
							<div class="deck-inner-section" id="deck-artifact-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-enchantment">
							<span id="deck-enchantment-title">Enchantments (0)</span>
							<div class="deck-inner-section" id="deck-enchantment-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-battle">
							<span id="deck-battle-title">Battles (0)</span>
							<div class="deck-inner-section" id="deck-battle-cards">
							</div>
						</div>
					</div>
					<div class="deck-col" id="col2">
						<div class="deck-section" id="deck-instant">
							<span id="deck-instant-title">Instants (0)</span>
							<div class="deck-inner-section" id="deck-instant-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-sorcery">
							<span id="deck-sorcery-title">Sorceries (0)</span>
							<div class="deck-inner-section" id="deck-sorcery-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-land">
							<span id="deck-land-title">Lands (0)</span>
							<div class="deck-inner-section" id="deck-land-cards">
							</div>
						</div>
						<div class="deck-section" id="deck-sideboard">
							<span id="deck-sideboard-title">Sideboard (0)</span>
							<div class="deck-inner-section" id="deck-sideboard-cards">
							</div>
						</div>
					</div>
				</div>
			</div>
		</div>
		<div id="modal-container">
			<div id="modal-content">
				<span class="close" onclick="closeModal()">&times;</span> <!--close button-->
			</div>
		</div>
	</div>

<script src="https://cdn.jsdelivr.net/gh/pieroxy/lz-string/libs/lz-string.js"></script>

	<script>
		let search_results = [];
		let card_list_arrayified = [];
		let specialchars = "";
		let deck = [];
		let sideboard = [];
		let active_card = [];
		let sets_json = {};
		let collection_copies = {};
		let deck_2 = {};
		let sideboard_2 = {};

		document.addEventListener("DOMContentLoaded", async function () {
			'''

	with open(os.path.join('resources', 'snippets', 'load-files.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

await fetch('/lists/all-sets.json')
					.then(response => response.json())
					.then(data => {
						sets_json = data; 
				}).catch(error => console.error('Error:', error));

			cardGrid = document.getElementById("imagesOnlyGrid");
			card_list_arrayified.sort(compareFunction);

			gridified_card = gridifyCard(card_list_arrayified[0], true, true);
			gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
			gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
			document.getElementById("card-grid-container").appendChild(gridified_card);

						// initial search on load
			preSearch();

			// get url params
			const urlParams = new URLSearchParams(window.location.search);
			if (urlParams.get('deck') != null) { // check if deck exists
				if (urlParams.get('deck').includes(';')) { // check if deck has the ';' (for deck names)
					let splitted = urlParams.get('deck').split(';'); // get the deck name and text by splitting
					readDeckText(atob(splitted[1]), splitted[0]);  
				} else {
					readDeckText(atob(urlParams.get('deck')));
				}
			}	
			// If a deck name is not imported, set the name to 'Untitled Deck'
			if (document.getElementById("deck-name").value == "undefined" || document.getElementById("deck-name").value == "") {
				document.getElementById("deck-name").value = "Untitled Deck";
			}

			// COLLECTIONS
			// initialize collections if they don't exist
			var colls = JSON.parse(localStorage.getItem("colls.collections"));
			if (colls == null) {
				colls = {}
			}
			// initialize default collections
			let sanctum_coll = [];
			let common_coll = [];
			for (const card of card_list_arrayified) { // loop through all cards
				// sanctum regex tests
				let regex = new RegExp("((P|p)athbound|(H|h)eir–)"); // check pathbounds and heirs, in the future other mechanics
				if (regex.test(card.rules_text)) {
					sanctum_coll.push(`1 ${card.card_name}`); // push just 1 because of sanctum limit
				} else if (card.type.includes("wonder") || card.type.includes("erysite") || card.type.includes("realm") || card.type.includes("frontier")) {  // check if it has a type that lets it be in the sanctum
					sanctum_coll.push(`1 ${card.card_name}`);
				}
				else if (card.special_text.includes("sanctum")) { // check evobars
					sanctum_coll.push(`1 ${card.card_name}`); 
				}
				else if (card.type.includes("Basic")) { // add basic lands
					sanctum_coll.push(`7 ${card.card_name}`); // push 7 as it's the max sanctum size
				}
				// check if the card is a common, isn't a token/reminder/boon, and isn't distant vulture astral (this will be fixed on apr 15 when the next update is pushed)
				if (card.rarity == "common" && !card.type.includes("Token") && !card.type.includes("Reminder") && !card.card_name.includes("Token") && !card.type.includes("Boon") && !card.card_name.includes("Distant Vulture Astral")) {
					console.log(card);
					common_coll.push(`4 ${card.card_name}`);
				}
			}
			// send the created collections to localstorage
			colls["Sanctum cards"] = sanctum_coll;
			colls["Pauper"] = common_coll;
			colls["Full card pool"] = "This is a dummy, the code handles this";
			localStorage.setItem("colls.collections", JSON.stringify(colls));
			// Initialize default settings
			defaultSetting('settings.autosave', 'On');
			defaultSetting('settings.searchalias', 'On');
			defaultSetting('settings.exportcube', 'On');
			defaultSetting('settings.maxcopies', 'On');
		});

		function displayChangeListener() {
			preSearch();
		}

		document.getElementById("sort-by").onchange = displayChangeListener;
		document.getElementById("sort-order").onchange = displayChangeListener;

		document.getElementById("file-menu").addEventListener("change", function(event) { // Watch the dropdown that says Actions...
			let option = document.getElementById("file-menu").value; // get the chosen option

			if (option == "new") // Create a new deck by initializing empty variables
			{
				deck = [];
				sideboard = [];
				deck_2 = {};
				sideboard_2 = {};
				processDeck();
				document.getElementById("file-menu").value = "default"; // set the value back
			}
			else if (option == "import")
			{
				document.getElementById("import-file").click(); // Import a file by clicking a certain element
			}
			else if (option == "save") {
				localStorage.setItem(document.getElementById("deck-name").value, generateDeckText()); // save the deck text with the key of the deck name to localstorage
				document.getElementById("file-menu").value = "default"; // set the value back
				openSaveModal(); // open the modal giving the user a notification
			}
			else if (option == "load") {
				loadDeck(); // open the modal for loading decks
			}
			else if (option == "delete") {
				deleteModal(); // open the modal for deleting decks
			}
			else if (option == "get-url") {
				navigator.clipboard.writeText(`https://voyager-mtg.github.io/deckbuilder?deck=${document.getElementById("deck-name").value.replaceAll(" ", "%20") + ';' + btoa(generateDeckText())}&main=${deck.length}&side=${sideboard.length}`); // write the url + ?deck= + the name with spaces replaced + ; + base64 encoded deck text + &main = deck count + &side= + sideboard count
				openCopyModal(); // open the modal notifying the user
			}
			else if (option == "copy") {
				navigator.clipboard.writeText(generateDeckText()); // copy the deck text to clipboard
				document.getElementById("file-menu").value = "default"; // set the dropdown back
				openCopy2Modal(); // open the modal to notify the user
			}
			else if (option == "save-collection") {
				let colls = JSON.parse(localStorage.getItem("colls.collections")); // get the collections object from colls.collections
				colls[document.getElementById("deck-name").value.toString()] = deckTextToCollection(); // save the deck text converted to collection text in the colls object with the deck name as the key
				localStorage.setItem("colls.collections", JSON.stringify(colls));
				document.getElementById("file-menu").value = "default"; // set colls back stringified
				openSaveCollModal(); // open the modal to notify the user
			}
			else if (option == "load-collection") {
				openLoadCollectionWindow(); // open the load collection modal
			}
			else if (option.startsWith("export"))
			{
				exportFile(option); // line 2637
			}
			else if (option == "draftmancer")
			{
				exportDraftmancer(); // line 2691
			}
			else if (option == "settings") {
				openSettingsModal(); // open the settings modal to notifyt he user
			}
		});

		document.addEventListener("click", (event) => {
			// if the rightclick menu is clicked on, get rid of it
			if (!contextMenu.contains(event.target)) {
				contextMenu.style.display = "none";
			}
		});

		document.getElementById("add-to-deck").addEventListener("click", () => {
			// if the add to deck button in the right click menu is clicked, add the card to the deck, then hide the menu
			addCardToDeck(active_card);
			contextMenu.style.display = "none";
		});

		document.getElementById("add-to-sideboard").addEventListener("click", () => {
			// if the add to sideboard button in the right click menu is clicked, add the card to the deck, then hide the menu
			addCardToSideboard(active_card);
			contextMenu.style.display = "none";
		});

		document.getElementById("display-select").addEventListener("change", function(event) {
			processDeck(); // when the user chooses the option to change the deck, re-process it
		});

		function openSaveModal() {
			// make the modal visible and add the text 'Deck saved as DECK NAME', then add the X
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Deck Saved as " + document.getElementById("deck-name").value + '<span class="close" onclick="closeModal()">&times;</span>';
		}

		function openCopyModal() {
			// make the modal visible and add the text 'Url copied to clipboard', then add the X			
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Url copied to clipboard" + '<span class="close" onclick="closeModal()">&times;</span>';
		}

		function openCopy2Modal() {
			// make the modal visible and add the text 'Decklist copied to clipboard', then add the X
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Decklist copied to clipboard" + '<span class="close" onclick="closeModal()">&times;</span>';
		}

		function closeModal() {
			// hide the modal and change the file menu to default
			document.getElementById("modal-container").style.display = "none";
			document.getElementById("file-menu").value = "default";
		}

		function openSaveCollModal() {
			// make the modal visible and add the text 'Deck saved as collection: DECK NAME', then add the X
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Deck Saved as collection: " + document.getElementById("deck-name").value + '<span class="close" onclick="closeModal()">&times;</span>';
		}

		function openSettingsModal() {
			// initialize empty HTML then add each option and the X to it, then make the modal visible and add the content
			let modalContent = '';
			modalContent += settingsOptionHtml("Auto save decks", "settings.autosave");
			modalContent += settingsOptionHtml("Export draftmancer as cube", "settings.exportcube");
			modalContent += settingsOptionHtml("Include aliases in name searching", "settings.searchalias");
			modalContent += settingsOptionHtml("Disable adding over max copies in collection", "settings.maxcopies");
			modalContent += `</select><span class="close" onclick="closeModal()">&times;</span>`;
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = modalContent;
		}

		function settingsOptionHtml(settingname, settingtag) {
			// add the text then ':'
			let generatedContent = settingname + ": ";
			// add the dropdown with an onchange to set the localStorage value of the settingtag
			generatedContent += `<select class="settings-dropdown" id="${settingtag}" onchange="localStorage.setItem('${settingtag}', document.getElementById('${settingtag}').value)">`;
			// add On and Off in the order they need to be based on the value stored in localstorage
			if (localStorage.getItem(settingtag) == "Off") {
				generatedContent += '<option>Off</option>';
				generatedContent += '<option>On </option>';
			} else {
				generatedContent += '<option>On </option>';
				generatedContent += '<option>Off</option>';
			}
			generatedContent += '</select>';
			return generatedContent;
		}

		function defaultSetting(name, default_) {
			// if you dont have a value in localstorage, set that value to default_
			if (localStorage.getItem(name) == null) {
				localStorage.setItem(name, default_);
			}
		}

		function loadDeck() { // this name is misleading, this opens the load modal
			// Unide the modal and add the text 'Loading Deck:'
			document.getElementById("modal-container").style.display = "block"; 
			document.getElementById("modal-content").innerHTML = "Loading Deck:";
			Object.keys(localStorage).forEach(function(key){ // Loop through each localstorage value, then check if its not a setting or collections
				if (key != "colls.collections" && !key.startsWith("settings.")) { 
					document.getElementById("modal-content").innerHTML += `<span class="load-btn" onclick="readDeckText(localStorage.getItem('${key}'),'${key}')">${key}</span>`; // add a button that loads the deck using readDeckText and has the name of the deck (key = deck name)
				}	
			});
			document.getElementById("modal-content").innerHTML += '<span class="close" onclick="closeModal()">&times;</span>'; // add the X
		} 

		function openLoadCollectionWindow() {
			// make the modal visible and add the text 'Loading Collection:'
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Loading Collection:";
			Object.keys(JSON.parse(localStorage.getItem("colls.collections"))).forEach(function(key){ // Loop through each item in the collections object
				// add a button that loads the collection using loadCollection and has the name of the collection (key = collection name)
				document.getElementById("modal-content").innerHTML += `<span class="load-btn" onclick="loadCollection('${key}')">${key}</span>`;			
			});
			document.getElementById("modal-content").innerHTML += '<span class="close" onclick="closeModal()">&times;</span>';
		} 

		function loadCollection(name) {
			// remove the copies style so we can change it later
			var e = document.getElementById("copies-style");
			if (e != null){ e.remove(); }
			if (name == "Full card pool") { // This is a special collection, so loading it is hard coded; we set card_list_arrayified to the original json, then close the modal and initialize the search
				card_list_arrayified = card_list.cards;
				closeModal();
				preSearch();
				return;
			}
			// get the collections object and find the collection to load, then initialize some variables
			let colls = JSON.parse(localStorage.getItem("colls.collections"));
			let collectionToLoad_ = colls[name];
			let new_list = [];
			let collectionToLoad = [];
			let cssStr = "";
			let i = 0;
			for (const item of collectionToLoad_) {
				// for each item in collections, push the card name (the number will be cut off)
				collectionToLoad.push(item.slice(2));
			}
			console.log(collectionToLoad);
			for (const card of card_list.cards) { // Loop through the card JSON
				if (collectionToLoad.includes(card.card_name)) { // If the collection has this card, add it to new_list, if it's undefined, don't do the next part
					new_list.push(card);
					if (collectionToLoad_[i] == undefined) {
						continue;
					}
					// add to the css to add the copy indicator in the topleft corner
					collection_copies[`${card["set"]}-${card["number"]}`] = Number(collectionToLoad_[i].split(" ")[0]);
					cssStr += `.img-container:has(> #${card["set"]}-${card["number"]}-cards-and-text):before {background-color: rgba(0,0,0,0.8); padding: 10px; color: white; font-size: 20px; content: "${collectionToLoad_[i].split(" ")[0]}x"; z-index: 999; display: block; position: absolute; border-radius: 20px;}\n`
					// modify deck and sideboard 2 and incrementy i
					i++;
					deck_2[`${card["set"]}-${card["number"]}`] = 0;
					sideboard_2[`${card["set"]}-${card["number"]}`] = 0;
				}
			}
			// set the card list to te new list, then add a style element with the css string we just made, then add it to the body. Close the modal, then initialize the search
			card_list_arrayified = new_list;
			const cssElem = document.createElement("style");
			cssElem.id = "copies-style";
			cssElem.innerHTML = cssStr;
			document.body.appendChild(cssElem);
			closeModal();
			preSearch();
		}

		function deckTextToCollection() {
			// get the deck text then split it into lines
			var text = generateDeckText();
			var lines = text.split("\n");
			var cardlist = [];
			for (const line of lines) {
				// for each line, add the line to the list
				cardlist.push(line);
			}
			return cardlist;
		}

		function readDeckText(text, name) {

			document.getElementById("deck-name").value = name;

			deck = [];
			sideboard = [];
			sb_cards = false;

			const lines = text.split('\\n');

			let deck_map = new Map();
			let sb_map = new Map();

			for (const line of lines)
			{
				if (line == 'sideboard' || line == '') // '' for Draftmancer files
				{
					sb_cards = true;
				}
				else if (!sb_cards)
				{
					count = parseInt(line.substring(0, line.indexOf(' ')));
					card_name = line.substring(line.indexOf(' ') + 1);

					if (deck_map.has(card_name))
					{
						deck_map.set(card_name, deck_map.get(card_name) + count);
					}
					else
					{
						deck_map.set(card_name, count);
					}
				}
				else
				{
					count = parseInt(line.substring(0, line.indexOf(' ')));
					card_name = line.substring(line.indexOf(' ') + 1);

					if (sb_map.has(card_name))
					{
						sb_map.set(card_name, sb_map.get(card_name) + count);
					}
					else
					{
						sb_map.set(card_name, count);
					}
				}
			}
			console.log(card_list_arrayified);
			for (const card of card_list_arrayified)
			{
				if (deck_map.has(card.card_name))
				{
					for (let i = 0; i < deck_map.get(card.card_name); i++)
					{
						addCardToDeck(JSON.stringify(card));
					}
					deck_map.delete(card.card_name);
				}

				if (sb_map.has(card.card_name))
				{
					for (let i = 0; i < sb_map.get(card.card_name); i++)
					{
						addCardToSideboard(JSON.stringify(card));
					}
					sb_map.delete(card.card_name);
				}
			}
		// reader.readAsText(file);
		document.getElementById("modal-container").style.display = "none";
		document.getElementById("file-menu").value = "default";
		}
		

		function deleteModal() {
			document.getElementById("modal-container").style.display = "block";
			document.getElementById("modal-content").innerHTML = "Deleting Deck:";
			Object.keys(localStorage).forEach(function(key){
				console.log(key);
   				console.log(localStorage.getItem(key));
				document.getElementById("modal-content").innerHTML += `<span id="delete-${key}" class="del-btn" onclick="deleteDeck('${key}')">${key}</span>`;
			});
			document.getElementById("modal-content").innerHTML += '<span class="close" onclick="closeModal()">&times;</span>';
		}

		function deleteDeck(name) {
			localStorage.removeItem(name);
			document.getElementById(`delete-${name}`).remove();
		}

		document.getElementById("import-file").addEventListener("change", function(event) {
			const files = event.target.files;

			if (files.length > 0) {
				const file = files[0];
				const name = file.name.replace(/\\.[^/.]+$/, "");
				const import_type = file.name.replace(/^[^/.]+\\./, "");

				document.getElementById("deck-name").value = name;

				deck = [];
				sideboard = [];
				sb_cards = false;

				const reader = new FileReader();
				reader.onload = function(e) {
					const fileContent = e.target.result;

					const lines = fileContent.split('\\n');
					if (import_type == 'dek')
					{
						for (const line of lines)
						{
							if (line == 'sideboard' || line == '') // '' for Draftmancer files
							{
								sb_cards = true;
							}
							else
							{
								const count = line.substring(0, line.indexOf(' '));
								const card = line.substring(line.indexOf(' ') + 1);

								for (let i = 0; i < count; i++)
								{
									if (sb_cards)
									{
										addCardToSideboard(card);
									}
									else
									{
										addCardToDeck(card);
									}
								}						
							}
						}
					}
					else if (import_type == 'txt')
					{
						let deck_map = new Map();
						let sb_map = new Map();

						for (const line of lines)
						{
							if (line == 'sideboard' || line == '') // '' for Draftmancer files
							{
								sb_cards = true;
							}
							else if (!sb_cards)
							{
								count = parseInt(line.substring(0, line.indexOf(' ')));
								card_name = line.substring(line.indexOf(' ') + 1);

								if (deck_map.has(card_name))
								{
									deck_map.set(card_name, deck_map.get(card_name) + count);
								}
								else
								{
									deck_map.set(card_name, count);
								}
							}
							else
							{
								count = parseInt(line.substring(0, line.indexOf(' ')));
								card_name = line.substring(line.indexOf(' ') + 1);

								if (sb_map.has(card_name))
								{
									sb_map.set(card_name, sb_map.get(card_name) + count);
								}
								else
								{
									sb_map.set(card_name, count);
								}
							}
						}
						for (const card of card_list_arrayified)
						{
							if (deck_map.has(card.card_name))
							{
								for (let i = 0; i < deck_map.get(card.card_name); i++)
								{
									addCardToDeck(JSON.stringify(card));
								}
								deck_map.delete(card.card_name);
							}

							if (sb_map.has(card.card_name))
							{
								for (let i = 0; i < sb_map.get(card.card_name); i++)
								{
									addCardToSideboard(JSON.stringify(card));
								}
								sb_map.delete(card.card_name);
							}
						}
					}
				};
				reader.readAsText(file);
			}

			document.getElementById("file-menu").value = "default";
		});

		'''

	with open(os.path.join('resources', 'snippets', 'compare-function.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function preSearch() {
			card_list_arrayified.sort(compareFunction);
			if (document.getElementById("sort-order").value == "descending")
			{
				card_list_arrayified.reverse();
			}
			search_results = [];

			search();
		}

		function search() {
			searchTerms = document.getElementById("search").value.toLowerCase();

			cardGrid = document.getElementById("imagesOnlyGrid");
			cardGrid.innerHTML = "";

			for (const card of card_list_arrayified) {
				if (card.shape.includes("token") && !searchTerms.includes("*t:token") && !searchTerms.includes("t:token"))
				{
					continue;
				}

				searched = searchAllTokens(card, tokenizeTerms(searchTerms));

				if (searched)
				{
					search_results.push(card);
				}
			}

			for (let i = 0; i < search_results.length; i++)
			{
				const imgContainer = document.createElement("div");
				const card_stats = search_results[i];
				const id = card_stats.set + "-" + card_stats.number + "-" + document.getElementById("display").value;
				imgContainer.className = "img-container";
				const card_sr_grid = gridifyCard(search_results[i]);
				const card_sr = card_sr_grid.getElementsByTagName("img")[0];

				card_sr.onmouseover = function() {
					cgc = document.getElementById("card-grid-container");
					cgc.innerHTML = "";
					const gridified_card = gridifyCard(card_stats, true, true);
					gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
					gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
					if (card_stats.shape.includes("double"))
					{
						gridified_card.getElementsByTagName("button")[0].onclick = function() {
							imgFlip("image-grid-card", card_stats.type.includes("Battle"));
						}
					}
					cgc.appendChild(gridified_card);
				};

				card_sr.onclick = function() {
					addCardToDeck(JSON.stringify(card_stats));
				}
				card_sr.style.cursor = "pointer";

				contextMenu = document.getElementById("myContextMenu");
				card_sr.addEventListener("contextmenu", (event) => {
					event.preventDefault(); // Prevent default context menu

					contextMenu.style.display = "block";
					contextMenu.style.left = event.pageX + "px";
					contextMenu.style.top = event.pageY + "px";

					active_card = JSON.stringify(card_stats);
				});

				imgContainer.appendChild(card_sr);
				cardGrid.appendChild(imgContainer);
			}
		}

		'''

	with open(os.path.join('resources', 'snippets', 'search-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	# INSERT THE CODE HERE

	with open(os.path.join('resources', 'snippets', 'tokenize-symbolize.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function gridifyCard(card_stats, card_text = false, rotate_card = false, designer_notes = false) {
			const card_name = card_stats.card_name;

			if (!card_text)
			{
				return buildImgContainer(card_stats, true, rotate_card);			
			}

		'''

	with open(os.path.join('resources', 'snippets', 'img-container-defs.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''

		function hasAllChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (!strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal;
		}

		function hasNoChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal;
		}

		function hasAllAndMoreChars(strOut, strIn) {
			let retVal = true;

			for (let i = 0; i < strIn.length; i++)
			{
				if (!strOut.includes(strIn.charAt(i)))
				{
					retVal = false;
				}
			}

			return retVal && (strOut.length > strIn.length);
		}

		function addCardToDeck(card) {
			let card_parsed = JSON.parse(card);
			if (modifyDeck2(`${card_parsed['set']}-${card_parsed['number']}`, '+')) {
				return;
			}
			deck.push(card);
			processDeck();
		}

		function addCardToSideboard(card) {
			let card_parsed = JSON.parse(card);
			if (modifySB2(`${card_parsed['set']}-${card_parsed['number']}`, '+')) {
				return;
			}
			sideboard.push(card);
			processDeck();
		}

		function processDeck() {
			const nct = document.getElementById("no-cards-text");
			nct.style.display = (deck.length == 0 && sideboard.length == 0) ? "block" : "none";

			const dc = document.getElementById("deck-count");
			dc.innerText = "(" + deck.length + " / " + sideboard.length + ")";

			let deck_cards = new Map([
				['land', new Map([])],
				['creature', new Map([])],
				['instant', new Map([])],
				['planeswalker', new Map([])],
				['artifact', new Map([])],
				['enchantment', new Map([])],
				['sorcery', new Map([])],
				['battle', new Map([])],
				['sideboard', new Map([])]
			]);

			for (const card of deck)
			{
				card_type = JSON.parse(card).type.toLowerCase();

				for (const [key, map] of deck_cards)
				{
					if (card_type.includes(key))
					{
						if (map.has(card))
						{
							map.set(card, map.get(card) + 1);
						}
						else
						{
							map.set(card, 1);
						}

						break;
					}
				}
			}
			for (const card of sideboard)
			{
				let map = deck_cards.get("sideboard");
				if (map.has(card))
				{
					map.set(card, map.get(card) + 1);
				}
				else
				{
					map.set(card, 1);
				}
			}

			for (const [key, map] of deck_cards)
			{
				dsec_id = "deck-" + key;
				outer_ele = document.getElementById(dsec_id);

				if (map.size == 0)
				{
					outer_ele.style.display = "none";
				}
				else
				{
					outer_ele.style.display = "grid";
					dsec_c_id = dsec_id + "-cards";
					
					dsec_t_id = dsec_id + "-title";
					title_ele = document.getElementById(dsec_t_id);
					let count = 0;
					for (const val of Array.from(map.values()))
					{
						count += val;
					}
					const numregex = /[0-9]+/;
					title_ele.innerText = title_ele.innerText.replace(numregex, count);

					cards_ele = document.getElementById(dsec_c_id);
					cards_ele.innerHTML = "";
					const cards_list = Array.from(map.keys()).sort();				
					for (const card of cards_list)
					{
						const display_style = document.getElementById("display-select").value;
						const card_stats = JSON.parse(card);
						const card_name = card_stats.card_name;

						if (display_style == "text")
						{
							card_row = document.createElement("div");
							card_row.className = "deck-line";
							
							card_in_deck = document.createElement("div");
							card_in_deck.innerText += map.get(card) + " " + card_name + "\\n";
							card_in_deck.style.cursor = "pointer";
							card_in_deck.onmouseover = function() {
								cgc = document.getElementById("card-grid-container");
								cgc.innerHTML = "";
								const gridified_card = gridifyCard(card_stats, true, true);
								gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
								gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
								if (card_stats.shape.includes("double"))
								{
									gridified_card.getElementsByTagName("button")[0].onclick = function() {
										imgFlip("image-grid-card", card_stats.type.includes("Battle"));
									}
								}
								cgc.appendChild(gridified_card);
							};

							del_btn = document.createElement("img");
							del_btn.className = "icon";
							del_btn.style.cursor = "pointer";
							if (key == "sideboard")
							{
								del_btn.src = "/img/sb-delete.png";
								del_btn.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									processDeck();
								}

								card_in_deck.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									let parsed_card = JSON.parse(card);
									modifySB2(`${parsed_card['set']}-${parsed_card['number']}`, '-');
									addCardToDeck(card);
								}
							}
							else
							{
								// console.log(card);
								del_btn.src = "/img/delete.png";
								let card_parsed = JSON.parse(card);
								del_btn.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									let card_parsed = JSON.parse(card);
									modifyDeck2(`${card_parsed['set']}-${card_parsed['number']}`, "-");
									processDeck();
								}

								card_in_deck.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									let card_parsed = JSON.parse(card);
									modifyDeck2(`${card_parsed['set']}-${card_parsed['number']}`, "-");						
									addCardToSideboard(card);
								}
							}

							db_container = document.createElement("div");
							db_container.className = "card-fx";
							db_container.appendChild(del_btn);

							card_row.appendChild(db_container);
							card_row.appendChild(card_in_deck);
							cards_ele.appendChild(card_row);
						}
						else
						{
							card_img_container = document.createElement("div");
							card_img_container.className = "card-img-container";
							if (card == cards_list[cards_list.length - 1])
							{
								card_img_container.style.height = "auto";
								card_img_container.style.maxHeight = "100%";
							}

							card_img = document.createElement("img");
							card_img.src = "/sets/" + card_stats.set + "-files/img/" + card_stats.number + "_" + card_stats.card_name + ((card_stats.shape.includes("double")) ? "_front" : "") + "." + card_stats.image_type;
							card_img.style.cursor = "pointer";
							card_img.onmouseover = function() {
								cgc = document.getElementById("card-grid-container");
								cgc.innerHTML = "";
								const gridified_card = gridifyCard(card_stats, true, true);
								gridified_card.getElementsByTagName("img")[0].id = "image-grid-card";
								gridified_card.getElementsByTagName("a")[0].removeAttribute("href");
								if (card_stats.shape.includes("double"))
								{
									gridified_card.getElementsByTagName("button")[0].onclick = function() {
										imgFlip("image-grid-card", card_stats.type.includes("Battle"));
									}
								}
								cgc.appendChild(gridified_card);
							};

							card_count = document.createElement("div");
							card_count.innerText = map.get(card) + "x";

							del_btn = document.createElement("img");
							del_btn.className = "icon";
							del_btn.style.cursor = "pointer";
							if (key == "sideboard")
							{
								del_btn.src = "/img/sb-delete.png";
								del_btn.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									processDeck();
								}

								card_img.onclick = function() {
									sideboard.splice(sideboard.indexOf(card), 1);
									let parsed_card = JSON.parse(card);
									modifySB2(`${parsed_card['set']}-${parsed_card['number']}`, '-');
									addCardToDeck(card);
								}
							}
							else
							{
								// console.log(card);
								del_btn.src = "/img/delete.png";
								let card_parsed = JSON.parse(card);
								del_btn.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									modifyDeck2(`${card_parsed['set']}-${card_parsed['number']}`, "-");
									processDeck();
								}

								card_in_deck.onclick = function() {
									deck.splice(deck.indexOf(card), 1);
									modifyDeck2(`${card_parsed['set']}-${card_parsed['number']}`, "-");
									addCardToSideboard(card);
								}
							}

							db_container = document.createElement("div");
							db_container.className = "card-fx";
							db_container.appendChild(del_btn);
							card_count.className = "card-fx";

							card_img_container.appendChild(db_container);
							card_img_container.appendChild(card_count);
							card_img_container.appendChild(card_img);
							cards_ele.appendChild(card_img_container);
						}
					}
				}
			}
		}

		function generateDeckText() {
			let deck_text = "";
			let map = new Map([]);
			for (const card of deck)
			{
				if (map.has(card))
				{
					map.set(card, map.get(card) + 1);
				}
				else
				{
					map.set(card, 1);
				}
			}
			for (const card_map of Array.from(map.keys()))
			{
				deck_text += map.get(card_map) + " " + (JSON.parse(card_map).card_name) + "\\n";
			}
			if (sideboard.length != 0)
			{
				deck_text += "sideboard\\n";
				map = new Map([]);
				for (const card of sideboard)
				{
					if (map.has(card))
					{
						map.set(card, map.get(card) + 1);
					}
					else
					{
						map.set(card, 1);
					}
				}
				for (const card_map of Array.from(map.keys()))
				{
					deck_text += map.get(card_map) + " " + (JSON.parse(card_map).card_name) + "\\n";
				}
			}
			return deck_text;
		}

		async function exportFile(export_as) {	
			let deck_text = "";
			let map = new Map([]);
			for (const card of deck)
			{
				if (map.has(card))
				{
					map.set(card, map.get(card) + 1);
				}
				else
				{
					map.set(card, 1);
				}
			}
			for (const card_map of Array.from(map.keys()))
			{
				deck_text += map.get(card_map) + " " + (export_as == "export-dek" ? card_map : JSON.parse(card_map).card_name) + "\\n";
			}
			if (sideboard.length != 0)
			{
				deck_text += "sideboard\\n";
				map = new Map([]);
				for (const card of sideboard)
				{
					if (map.has(card))
					{
						map.set(card, map.get(card) + 1);
					}
					else
					{
						map.set(card, 1);
					}
				}
				for (const card_map of Array.from(map.keys()))
				{
					deck_text += map.get(card_map) + " " + (export_as == "export-dek" ? card_map : JSON.parse(card_map).card_name) + "\\n";
				}
			}
			//let deck_text = generateDeckText()
			let downloadableLink = document.createElement('a');
			downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(deck_text));
			downloadableLink.download = document.getElementById("deck-name").value + (export_as == "export-dek" ? ".dek" : ".txt");
			document.body.appendChild(downloadableLink);
			downloadableLink.click();
			document.body.removeChild(downloadableLink);

			document.getElementById("file-menu").value = "default";
		}

		function convertManaCostForDraftmancer(mana_cost) {
			return mana_cost
				.replace(/{([A-Z])([A-Z])}/g, "{$1/$2}");
		}

		async function exportDraftmancer() {	
			let output_text = "";
			let cards = new Map();
			
			console.log("deck:", deck);
			
			for (const card of deck)
			{
				const c = JSON.parse(card);
				if (cards.has(c.card_name))
				{
					cards.get(c.card_name).count += 1;
				}
				else
				{
					cards.set(c.card_name, {...c, count: 1});
				}
			}

			const URLDomain = "https://voyager-mtg.github.io"; // FIXME: Shouldn't be hardcoded.

			let slots = '';

			if (localStorage.getItem('settings.exportcube') == "On") {
				slots = 'rare: 15';
			} else {
				slots = '"rare": 1,\\n"uncommon": 3,\\n"common": 10"';
			}

			output_text += `[Settings]
{
  "layouts": {
    "default": {
      "weight": 1,
      "slots": {
		${slots}
      }
	}
  }
}
`;
			output_text += "[CustomCards]\\n[\\n";
			for (const c of cards.values())
			{
				const img_url = URLDomain + "/sets/" + c.set + "-files/img/" + c.number + "_" + c.card_name + ((c.shape.includes("double")) ? "_front" : "") + "." + c.image_type;
				output_text += "  {\\n";
				output_text += `    "name": "${c.card_name}",\\n`;
				if(c.cost)
					output_text += `    "mana_cost": "${convertManaCostForDraftmancer(c.cost)}",\\n`;
				else 
					output_text += `    "mana_cost": "",\\n`;
				if(c.rarity)
					output_text += `    "rarity": "${c.rarity}",\\n`;
				if(c.set)
					output_text += `    "set": "${c.set}",\\n`;
				if(c.number)
					output_text += `    "collector_number": "${c.number}",\\n`;
				if(c.type) {
					output_text += `    "type": "${c.type.split(" – ")[0]}",\\n`;
					const subtypes = c.type.split(" – ")[1];
					if(subtypes)
						output_text += `    "subtypes": ["${subtypes.split(" ").join("", "")}"],\\n`;
				}
				if(c.rules_text)
					output_text += `    "oracle_text": ${JSON.stringify(c.rules_text)},\\n`;
				output_text += `    "image": "${img_url}",\\n`;
				if(c.shape.includes("double")) {
					const back_url = URLDomain + "/sets/" + c.set + "-files/img/" + c.number + "_" + c.card_name + "_back" + "." + c.image_type;
					output_text += `    "back": {`
					output_text += `      "name": "${c.card_name2}",\\n`;
					if(c.cost2)
						output_text += `      "mana_cost": "${convertManaCostForDraftmancer(c.cost2)}",\\n`;
					else 
						output_text += `    "mana_cost": "",\\n`;
					if(c.rarity2)
						output_text += `      "rarity": "${c.rarity2}",\\n`;
					if(c.set2)
						output_text += `      "set": "${c.set2}",\\n`;
					if(c.number2)
						output_text += `      "collector_number": "${c.number2}",\\n`;
					if(c.type2) {
						output_text += `      "type": "${c.type2.split(" – ")[0]}",\\n`;
						const subtypes = c.type2.split(" – ")[1];
						if(subtypes)
							output_text += `    "subtypes": ["${subtypes.split(" ").join("", "")}"],\\n`;
					}
					if(c.rules_text2)
						output_text += `      "oracle_text": ${JSON.stringify(c.rules_text2)},\\n`;
					output_text += `      "image": "${back_url}",`
					output_text += `    },\\n`;
				}
				output_text += "  },\\n";
			}
			output_text += "]\\n";

			if (localStorage.getItem('settings.exportcube')) {
				output_text += `[rare]\n`;
				for (const c of cards.values()) {
					output_text += `${c.count} ${c.card_name}\n`;
				}
			} else {
				const rarities = [...(new Set([...cards.values().map(c => c.rarity)]))];

				for(const r of rarities) {
					output_text += `[${r}]\n`;
					for (const c of cards.values()) {
						if(c.rarity === r) 
							output_text += `${c.count} ${c.card_name}\n`;
					}
				}
			}	

			let downloadableLink = document.createElement('a');
			downloadableLink.setAttribute('href', 'data:text/plain;charset=utf-8,' + encodeURIComponent(output_text));
			downloadableLink.download = document.getElementById("deck-name").value + ".txt";
			document.body.appendChild(downloadableLink);
			downloadableLink.click();
			document.body.removeChild(downloadableLink);

			document.getElementById("file-menu").value = "default";
		
		}

		function goToSearch() {
			window.location = ("/search");
		}

		document.getElementById("search").addEventListener("keypress", function(event) {
			if (event.key === "Enter") {
				event.preventDefault();
				preSearch();
			}
		});
		modal = document.getElementById("modal-container");
		window.onclick = function(event) {
			if (event.target == modal) {
				closeModal();
			}
		}

				function modifyDeck2(setNum, op) {
			if (op == "+") {
				console.log(deck_2[setNum], sideboard_2[setNum], collection_copies[setNum], setNum)
				if ((deck_2[setNum] + sideboard_2[setNum]) >= collection_copies[setNum]) {
					console.log('ret');
					return true;
				}
				if (setNum in deck_2) {
					deck_2[setNum] += 1;
				} else {
					deck_2[setNum] = 1;
				}
			}
			if (op == "-") {
				deck_2[setNum] -= 1;
			}
			console.log(deck_2);
			return false;
		}
		function modifySB2(setNum, op) {
			if (op == "+") {
				console.log(deck_2[setNum], sideboard_2[setNum], collection_copies[setNum], setNum)
				if ((deck_2[setNum] + sideboard_2[setNum]) >= collection_copies[setNum]) {
					console.log('ret');
					return true;
				}
				if (setNum in sideboard_2) {
					sideboard_2[setNum] += 1;
				} else {
					sideboard_2[setNum] = 1;
				}
			}
			if (op == "-") {
				sideboard_2[setNum] -= 1;
			}
			console.log(sideboard_2, op, setNum);
			return false;
		}

		window.onbeforeunload = function() {
			if (localStorage.getItem("settings.autosave") == "On") {
				localStorage.setItem(document.getElementById("deck-name").value, generateDeckText());
			}
		}


		'''

	with open(os.path.join('resources', 'snippets', 'random-card.txt'), encoding='utf-8-sig') as f:
		snippet = f.read()
		html_content += snippet

	html_content += '''
	</script>
</body>
</html>'''

	# Write the HTML content to the output HTML file
	with open(output_html_file, 'w', encoding='utf-8-sig') as file:
		file.write(html_content)

	print(f"HTML file saved as {output_html_file}")