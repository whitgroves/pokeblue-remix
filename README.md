# Pokémon Blue Remix

This is a fork of [pret's disassembly of Pokémon Red/Blue](https://github.com/pret/pokered) inspired by [TheSmithPlays' Yellow Legacy project](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy).

The goal is not to reproduce or backport YL, but to see what gen 1 would feel like with a rebalanced type chart and some unhinged retypings (e.g., Fire is super effective vs Ghost, Kangaskhan is now Normal/Dragon).

However, some changes from Yellow, the Legacy hacks, and the [pret tutorials](https://github.com/pret/pokered/wiki/Tutorials) are duplicated here, such as the Nidos getting *Double Kick* early, making *Cut* Bug-type, and auto-sorting the items in the backpack.

## Changes (Revision 1.3)
- Updated interactions for the original 15 types ✓
- Updated typings to make certain Pokemon lore-friendly, interesting, or unique ✓
- Updated learnsets to better fit each Pokemon's kit ✓
- Several updates to the movepool, detailed [here](./MOVES.md) ✓
- TM's 04, 37, and 41 now teach *Twineedle*, *Sludge*, and *Flamethrower*, respectively ✓
- Updated TMs at the Celadon mart, including the girl on the roof ✓
- The Ghost type is special instead of physical ✓
- All 151 Pokemon are available on a single save ✓
- Fast text speed and Set battles by default ✓
- Auto-sort the backpack by pressing Start (thanks to [devolov](https://github.com/pret/pokered/wiki/Add-Item-Sorting-In-Bag)) ✓
- The good rod is good and the super rod is super ✓
- Trashed the Vermilion trash can puzzle ✓
- The "Down + B" trick actually works ✓

These changes are largely untested, so if you run into issues please reach out on X: [@whitgroves](https://x.com/whitgroves)

## Why *Blue* Remix?
While *Red Remix* does roll off the tongue, Pokemon Blue was the first Pokemon game I played and the first video game I bought for myself, so I chose that name for nostalgia's sake.

## Why Not Yellow?
Again, Blue was the game I made memories with, plus I didn't want to lock up a party slot.

## The Power Is Yours
While working on this I developed a script, **easy_edit.py**, to convert type, move, and pokemon data from assembly to csv and back again for easier editing.

It should be compatible with any gen 1 disassembly and only relies on the python3 standard library, so feel free to use it for your own projects.

### Example 1
To make changes for another repo, copy [easy_edit.py](./tools/easy_edit.py) into your project, then call:
```
$ easy_edit.py -e --matchups
$ easy_edit.py -e --moves
$ easy_edit.py -e --mon <pokemon name, all lowercase, no spaces>
$ easy_edit.py -e --all
```
To generate your csv files for editing, then run:
```
$ easy_edit.py -u --matchups
$ easy_edit.py -u --moves
$ easy_edit.py -u --mon <pokemon name, all lowercase, no spaces>
$ easy_edit.py -u --all
```
To overwrite the game's assembly files with any of those updates.

### Example 2
To make changes to this build using `make`:
```
$ git clone https://github.com/whitgroves/pokeblue-remix.git
$ cd pokeblue-remix
$ make edits
<< update csv files as desired >>
$ make updates
```

### Disclaimer

Please note that this script is not "smart", so values in the csv (except for "PSYCHIC", which is an edge case) must match the assembly code (case-insensitive).

Also, consider making a backup of the original values before updating so you can rollback changes:
```
$ easy_edit.py -e --all -c .edits
$ cp -r .edits .backups
```