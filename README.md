# Pokémon Blue Remix

This is a Pokemon Blue romhack forked from [pret's disassembly of Pokémon Red and Blue](https://github.com/pret/pokered) and inspired by [TheSmithPlays' Yellow Legacy project](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy).

The goal is not to reproduce or backport that project, but to see what gen 1 would feel like with [rebalanced type matchups](./type_matchups.xlsx) and some unhinged retypings for less notable mons, such as changing Ninetales to Fire/Ghost, Venomoth to Bug/Psychic, or Electabuzz to Electric/Fighting.

However, it will still include some changes from Yellow, Yellow Legacy, and the [pret tutorials](https://github.com/pret/pokered/wiki/Tutorials), such as the Nidos getting *Double Kick* early, making *Cut* Bug-type, and auto-sorting the items in the backpack.

## Changes (✓ = done, ~ = in progress)
- Updated interactions for the original 15 types ([spreadsheet](TypeChart.xlsx)) ~
- Updated typing to make certain Pokemon lore-accurate, interesting, or unique ✓
- Updated learnsets to better fit each Pokemon's kit
- Updated typing, power, accuracy, and effects to make certain moves more viable or less frustrating 
    - All 95% accurate moves are now 100% accurate ✓
    - All trapping moves (e.g., *Wrap, Fire Spin*) to damaging moves with a secondary status effect ✓
    - Struggle, Self-Destruct, and Explosion are all "None"-type (read: *Bird*-type) ✓
    - Certain special moves are treated as physical (e.g., *Crabhammer, Thunderpunch*)
- The Ghost type is special instead of physical ✓
- All 151 Pokemon are available on a single save ✓
- The good rod is good and the super rod is super ✓
- Fast text speed and Set battles by default ✓
- Auto-sort the backpack by pressing Start
- The "Down + B" trick actually works

## Why *Blue* Remix?
While *Red Remix* does roll off the tongue, Pokemon Blue was the first Pokemon game I played and the first video game I bought for myself, so I chose that name for nostalgia's sake.

## Why Not Yellow?
Again, Blue was the game I made memories with, plus I didn't want to lock up a party slot. Eventually I'll make a patch with just the updated mon typings so they can be added to any gen 1 rom.

## Bonus Tools
If you want to update the type chart, you can use [type_matchups.py](./type_matchups.py) and [type_macthups.xlsx](./type_matchups.xlsx) in the home directory of this (or any other gen 1) hack to generate a copy of [type_matchups.asm](./data/types/type_matchups.asm), then follow [these instructions](https://github.com/pret/pokered/blob/master/INSTALL.md) to build your own rom.

[moves.py](./moves.py) does a similar thing for the movelist, though it doesn't update learnsets.