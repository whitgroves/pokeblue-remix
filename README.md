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
    - Signature moves or moves used mainly by a certain type are now that type ~
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

These changes are largely untested, so if you try out the hack and run into any issues, please reach out on X: [@whitgroves](https://x.com/whitgroves)

## Why *Blue* Remix?
While *Red Remix* does roll off the tongue, Pokemon Blue was the first Pokemon game I played and the first video game I bought for myself, so I chose that name for nostalgia's sake.

## Why Not Yellow?
Again, Blue was the game I made memories with, plus I didn't want to lock up a party slot.

## The Power Is Yours
While working on this I developed 2 tools, **matchups.py** and **moves.py**, to convert type matchups and move data from assembly to csv and back again for easier editing of the type chart and movepool.

These should be compatible with any gen 1 disassembly and only rely on the python3 standard library, so feel free to use them in your own project.

#### Example 1
To make changes for another repo, copy [matchups.py](./tools/matchups.py) and [moves.py](./tools/moves.py) into your project, then call:
```
$ python3 matchups.py -i <path to type_matchups.asm>
$ python3 moves.py -i <path to moves.asm>
```
Which whill generate **type_matchups.csv** and **moves.csv**, respectively.

Edit these files, then run:
```
$ python3 matchups.py -i type_matchups.csv
$ python3 moves.py -i moves.csv
```
To generate updated copies of **type_matchups.asm** and **moves.asm**.

### Example 2
To make changes to this build using `make`:
```
$ git clone https://github.com/whitgroves/pokeblue-remix.git
$ cd pokeblue-remix
```
And either:
```
$ make matchups moves
- OR -
$ make edits
```
To generate the csv files and make your edits, then run:
```
$ make remix
```
To update the assembly files, or just:
```
$ make
```
To build the entire project.
