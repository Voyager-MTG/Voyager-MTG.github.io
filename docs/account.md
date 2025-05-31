## Account page

### HTML structure

.header {
    Standard header present across all pages. Contains the links for the core pages at the top.
}

.#selects {
	The Gradient dropdown
	Additional dropdowns could be added here but are unnecessary and unused currently
}

.page-container {
	The container for the main page

	.top-section {
		Container for a header section
		Currently only contains the username heading
	}

	.deck-section-header {
		Header containing the text “My Decks”
	}

	.decks-container #decks {
		This section will be modified by the js to add all of the users decks
		Displayed as a grid
	}

	.deck-section-header (#2) {
		Header containing the text “My Collections”
	}

	.collections-container #colls{
		This section will be modified by the js to add all of the users collections
		Displayed as a grid
	}

}

### Javascript functions

setGradient(gradient = false: string|bool) -> void {
    args:
        gradient: The gradient to set to, if false, grab it from #color-select

    sets the background image of the page to be a linear gradient defined in lists/gradients.json
}

prepareGradients() -> void {
    sets up the gradient dropdown on page initialization by grabbing all of the gradients from lists/gradients.json
}

async reload() -> void {
    generates the whole page content and is called whenever data is changed and the page needs to be remade

    loops through decks and grabs the formats, and appends decks into their format containers

    does the same with collections, minus the formats bit
}

createFormatContainer(format_name: string) -> Element {
    args:
        format_name: The name of the format
    
    creates a format container HTML element with a name passed in args containing a header, an <hr>, and an empty container with an id to be used by reload()
}

createDeckContainer(deck: object) -> Element {
    args:
        deck: The deck object we're generating a container for
    
    Creates a deck container for the provided deck object, including all of the buttons, preview image, and deck title
}

createDeckIcon(img: string, color: string) -> Element {
    args:
        img: the image name to be used in the icon
        color: the deck-icon class to be used

    Creates an element with the image /img/<img>.png and the class deck-icon-<color> deck-icon-shadow and returns it
}