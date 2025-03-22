WORLD_LAYERS: dict[str: int] = {
	'water': 0,
	'bg': 1,
	'shadow': 2,
	'main': 3,
	'top': 4
}

COLORS: dict[str: str] = {
	'white': '#f4fefa',
	'pure white': '#ffffff',
	'dark': '#2b292c',
	'light': '#c8c8c8',
	'gray': '#3a373b',
	'gold': '#ffd700',
	'light-gray': '#4b484d',
	'fire':'#f8a060',
	'water':'#50b0d8',
	'plant': '#64a990',
	'black': '#000000',
	'red': '#f03131',
	'blue': '#66d7ee',
	'normal': '#ffffff',
	'dark white': '#f0f0f0'
}

TILE_SIZE = 64
WIDTH = 1280
HEIGHT = 720
SPRITE_WIDTH = 80
SPRITE_HEIGHT = 60
ANIMATION_SPEED = 6

TILE_SETTINGS = {
    "Terrain": {
        "wall": ["17"],
        "closedWindow": ["29", "30", "39", "40"],
        "brickFloor": ["9"],
        "woodenFloor": ["4"],
        "openedWindow": ["24", "25", "34", "35"]
    },
    "Objects": {
        "TableSideLeft": ["61"],
        "TableSideRight": ["62"],
        "TableLeftBottomCorner": ["81"],
        "TableSideBottom": ["82"],
        "TableRightBottomCorner": ["83"],
        "TableRightSide": ["73"],
        "TableRightTopSize": ["63"]
    }
}
