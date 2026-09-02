open the voyager mtg github io repo in vscode
navigate to src/js/deckdata-cleaner/main.js
edit the variable to contain the old card names as keys and the new card names as values e.g. "Clerics Claymore": "Cleric's Claymore"
Then in your Vscode Vscodium Terminal, run the following:

cd src/js/deckdata-cleaner
npm i   (In case you've never done this before)
npm start

When logs stop for a couple seconds, terminate the program (ctrl+c)
