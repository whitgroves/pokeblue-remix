# Pokémon Blue Remix

This is a fork of [pret's disassembly of Pokémon Red/Blue](https://github.com/pret/pokered) inspired by [TheSmithPlays' Yellow Legacy project](https://github.com/cRz-Shadows/Pokemon_Yellow_Legacy).

The goal is not to reproduce or backport YL, but to see what gen 1 would feel like with a rebalanced type chart and some unhinged retypings (e.g., Fire is super effective vs Ghost, Kangaskhan is now Normal/Dragon).

However, some changes from Yellow, the Legacy hacks, and the [pret tutorials](https://github.com/pret/pokered/wiki/Tutorials) are duplicated here, such as the Nidos getting *Double Kick* early, making *Cut* Bug-type, and auto-sorting the items in the backpack.

## Changes (✓ = done, ~ = in progress)
- Updated interactions for the original 15 types ✓
- Updated typing to make certain Pokemon lore-friendly, interesting, or unique ✓
- Updated learnsets to better fit each Pokemon's kit ~
- [Several changes to the movepool](./MOVES.md), including:
    - All 95% accurate moves are now 100% accurate ✓
    - Signature moves or moves used mainly by a certain type are now that type ✓
    - Trapping moves (e.g., *Wrap*, *Fire Spin*) no longer trap but have a chance to drop stats ✓
    - Struggle ~~, Self-Destruct, and Explosion are all~~ is Typeless (read: Bird-type) ✓
    - *Punch* moves, *Clamp*, *Waterfall*, and *Crabhammer* are treated as physical ✓
    - *Night Shade* has 60 base power and a 20% chance to inflict sleep ✓
- The Ghost type is special instead of physical ✓
- All 151 Pokemon are available on a single save ✓
- The good rod is good and the super rod is super ✓
- Fast text speed and Set battles by default ✓
- Auto-sort the backpack by pressing Start
- The "Down + B" trick actually works

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
$ easy_edit.py -e --all
$ mv moves.csv moves_old.csv && mv type_matchups.csv type_matchups.old.csv
```