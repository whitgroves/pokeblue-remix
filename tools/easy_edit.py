#!/usr/bin/env python3

# Converts certain game files between assembly and csv for easier editing of the type chart and movepool.

import csv
from pathlib import Path
from argparse import ArgumentParser

# Command-Line Arguments

parser = ArgumentParser()
parser.description = 'Converts certain game files between assembly and csv for easier editing of the type chart and movepool.\
                      By default, assumes cwd is the root folder of the disassembly. Does not support custom types.'
parser.add_argument('-c', '--csv-dir', type=Path, help="Where to read/write the csv files. Defaults to cwd.", default='.')
parser.add_argument('-d', '--data-dir', type=Path, help="Where the game's data files are located.", default='./data/')
parser.add_argument('-e', '--export', action='store_true', help="When set, exports the game's assembly files to csv.")
parser.add_argument('-u', '--update', action='store_true', help="When set, updates the game's assembly files with csv edits.")
parser.add_argument('-q', '--quiet', action='store_true', help="If set, will not print import/export status to the cmd.")
parser.add_argument('--matchups', action='store_true', help="Set to import/export type_matchups.asm.")
parser.add_argument('--moves', action='store_true', help="Set to import/export moves.asm.")
parser.add_argument('--all', action='store_true', help="Set to import/export all applicable game files.")
ARGS, _ = parser.parse_known_args()

# Helper Functions

def effect_map(inverted=False) -> dict:
    effect_text = ['NO_EFFECT', 'NOT_VERY_EFFECTIVE', 'SUPER_EFFECTIVE']
    effect_vals = [0, 0.5, 2]
    if inverted: return dict(zip([str(val) for val in effect_vals], effect_text))
    return dict(zip(effect_text, effect_vals))

def safe_format(field:str, as_code:bool=False) -> str:
    field = field.strip().upper()
    if as_code: return 'PSYCHIC_TYPE' if field == 'PSYCHIC' else field
    return 'PSYCHIC' if field == 'PSYCHIC_TYPE' else field

def rpad(string:str, target:int) -> str: # right-pads `string` if shorter than `target`.
    amount = target - len(string)
    return string + ' '*amount if amount > 0 else string

def lpad(string:str, target:int) -> str: # left-pads `string` if shorter than `tartet`.
    amount = target - len(string)
    return ' '*amount + string if amount > 0 else string

def safe_print(message:str, **kwargs) -> None:
    if ARGS.quiet: return
    print(f'easy_edit.py: {message}', **kwargs)

# Update to support custon types. Except for Psychic, these must appear exactly as they are written in the game's code, and the csv order must match.
types = ['NORMAL', 'FIRE', 'WATER', 'ELECTRIC', 'GRASS', 'ICE', 'FIGHTING', 'POISON', 'GROUND', 'FLYING', 'PSYCHIC', 'BUG', 'ROCK', 'GHOST', 'DRAGON'] 

# Export / Update Functions

def export_matchups() -> None: # exports type_matchups.asm to type_matchups.csv
    safe_print('Exporting type_matchups.asm to type_matchups.csv...', end='\r')
    effects = effect_map()
    matchups = { _type: dict.fromkeys(types) for _type in types } # { Attacker : { Defender : Multiplier } }
    with ARGS.data_dir.joinpath('types', 'type_matchups.asm').open() as infile:
        for line in infile.readlines():
            data = line.split(';')[0].split('\tdb')
            if len(data) <= 1 or '-1' in data[-1]: continue
            attacker, defender, effect = [safe_format(field) for field in data[-1].split(',')]
            matchups[attacker][defender] = effects[effect]
    with Path('type_matchups.csv').relative_to(ARGS.csv_dir).open('w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(['', *types])
        for attacker in matchups:
            writer.writerow([attacker, *matchups[attacker].values()])
    safe_print('Exporting type_matchups.asm to type_matchups.csv...Done.')

def update_matchups() -> None: # overwrites type_matchups.asm using type_matchups.csv
    csv_path = Path('type_matchups.csv').relative_to(ARGS.csv_dir)
    if not csv_path.exists(): safe_print('type_matchups.csv not found. Skipping update.')
    else:
        safe_print('Updating type_matchups.asm using type_matchups.csv...', end='\r')
        effects = effect_map(inverted=True)
        with csv_path.open() as infile:
            with ARGS.data_dir.joinpath('types', 'type_matchups.asm').open('w') as outfile:
                reader = csv.reader(infile, delimiter=',')
                lines = [
                    'TypeEffects:',
                    '\t;  attacker,     defender,     *=',
                ]
                for i, [attacker, *defenders] in enumerate(reader):
                    if i == 0: continue
                    attacker = safe_format(attacker, as_code=True)+','
                    for d, effect in enumerate(defenders):
                        if not effect: continue
                        defender = safe_format(types[d], as_code=True)+','
                        lines.append(f'\tdb {rpad(attacker, 13)} {rpad(defender, 13)} {effects[effect]}')
                lines.append('\tdb -1 ; end')
                lines.append('\n; autogenerated by easy_edit.py')
                outfile.writelines([line+'\n' for line in lines])
        safe_print('Updating type_matchups.asm using type_matchups.csv...Done.')

def export_moves() -> None: # exports moves.asm to moves.csv
    safe_print('Exporting moves.asm to moves.csv...', end='\r')
    with ARGS.data_dir.joinpath('moves', 'moves.asm').open() as infile:
        with Path('moves.csv').relative_to(ARGS.csv_dir).open('w') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['Name', 'Effect', 'Power', 'Type', 'Accuracy', 'PP'])
            for line in infile.readlines():
                data = line.split(';')[0].split('\tmove')
                if len(data) > 1: writer.writerow([safe_format(text) for text in data[-1].split(',')])
    safe_print('Exporting moves.asm to moves.csv...Done.')

def update_moves() -> None: # overwrites moves.asm using moves.csv
    csv_path = Path('moves.csv').relative_to(ARGS.csv_dir)
    if not csv_path.exists(): safe_print('moves.csv not found. Skipping update.')
    else:
        safe_print('Updating moves.asm using moves.csv...', end='\r')
        with csv_path.open() as infile:
            with ARGS.data_dir.joinpath('moves', 'moves.asm').open('w') as outfile:
                reader = csv.reader(infile, delimiter=',')
                lines = [
                    'MACRO move',
                    '\tdb \\1 ; animation (interchangeable with move id)',
                    '\tdb \\2 ; effect',
                    '\tdb \\3 ; power',
                    '\tdb \\4 ; type',
                    '\tdb \\5 percent ; accuracy',
                    '\tdb \\6 ; pp',
                    '\tassert \\6 <= 40, "PP must be 40 or less"',
                    'ENDM',
                    '',
                    'Moves:',
                    '; Characteristics of each move.',
                    '\ttable_width MOVE_LENGTH, Moves',
                ]
                for i, (name, effect, power, _type, accuracy, pp, *_) in enumerate(reader):
                    if i == 0: continue # header
                    if any([not field.isnumeric() for field in [power, accuracy, pp]]): raise ValueError('Power, Accuracy, and PP must be numeric.')
                    name, effect, _type = [safe_format(field, as_code=True)+',' for field in [name, effect, _type]]
                    power, accuracy, pp = [lpad(field, 3)+',' for field in [power, accuracy, pp]]
                    lines.append(f'\tmove {rpad(name, 13)} {rpad(effect, 27)} {rpad(power, 4)} {rpad(_type, 13)} {rpad(accuracy, 4)}{pp[:-1]}')
                lines.append('\tassert_table_length NUM_ATTACKS')
                lines.append('\n; autogenerated by easy_edit.py')
                outfile.writelines([line+'\n' for line in lines])
        safe_print('Updating moves.asm using moves.csv...Done.')

# Showtime

if __name__ == '__main__':
    error = None
    if not ARGS.csv_dir.exists(): error = "CSV data either dosen't exist or wasn't found. Update --csv-dir and try again."
    if not ARGS.data_dir.exists(): error = "Game data either doesn't exist or wasn't found. Update --data-dir and try again."
    if not ARGS.export and not ARGS.update: error = "No operation selected. Set --export or --update and try again."
    if not ARGS.all and not ARGS.matchups and not ARGS.moves: error = "No data category selected. Set --macthups or --moves and try again."
    if error:
        safe_print(f'easyedit.py: {error} (Use -h to see options)')
        exit(1)
    if ARGS.matchups or ARGS.all:
        if ARGS.export: export_matchups()
        if ARGS.update: update_matchups()
    if ARGS.moves or ARGS.all:
        if ARGS.export: export_moves()
        if ARGS.update: update_moves()