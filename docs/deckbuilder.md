## Deckbuilder Page

### HTML structure

.preload-hiddens {
    images we want to preload but not show
}

.header {
    Standard header present across all pages. Contains the links for the core pages at the top.
    The header on this page is aligned differently and has no search input bar
}

.rc-menu #myContextMenu {
    The right click menu that appears on cards in #imagesOnlyGrid
}

.page-container {
    Container for the main page

    .search-container {
        Container for the left portion of the page dedicated to the card search

        .deckbuilder-search-grid {
            Contains the settings at the top of the search area, including the search input, sort type & order
        }

        .search-results-container {
            Container for the things below .deckbuilder-search-grid

            .search-image-grid-container {
                Container for the grid containing search results

                .search-image-grid #imagesOnlyGrid {
                    The element where the images of all of the searched cards are actually added in the js
                }

                .search-image-gradient-container {
                    Container for:

                    .search-image-gradient {
                        Gradient at the bottom of the search results, disablable in settings
                    }
                }

            }
        }
    }

    .deck-container {
        Contains the other half of the page that has the deck

        .#no-cards-text {
            The text that appears if you have no cards in your deck
        }

        .deck-info-grid {
            Similar to .deckbuilder-search-grid, contains all the deckbuilder options, the card count, actions dropdown, etc.
        }

        .static-deck-container {
            Container for the deck

            .deck-cards-container {
                Contains the 2 deck columns and has scrolling
                Displayed as a grid

                .deck-col #col1 {
                    column 1
                    contains the creature, planesalkwer, artifact, and enchantment deck sections
                }

                .deck-col #col2 {
                    column 2
                    contains the instant, sorcery, sideboard, and sanctum deck sections
                }
            }
        }
    }
}