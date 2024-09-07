#!/usr/bin/env python3

# Converts certain game files between assembly and csv for easier editing of the type chart and movepool.

import os
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
parser.add_argument('-v', '--verbose', action='store_true', help="If set, overrides --quiet and outputs all messages for --all.")
parser.add_argument('--matchups', action='store_true', help="Set to import/export type_matchups.asm.")
parser.add_argument('--moves', action='store_true', help="Set to import/export moves.asm.")
parser.add_argument('--mon', type=str, help="Set to export the base stats and level_moves of a specific pokemon. Name should exclude punctuation or spaces.")
parser.add_argument('--all', action='store_true', help="Set to import/export all applicable game files.")
ARGS, _ = parser.parse_known_args()

# Update to support custon types. Except for Psychic, these must appear exactly as they are written in the game's code, and the csv order must match.
types = ['NORMAL', 'FIRE', 'WATER', 'ELECTRIC', 'GRASS', 'ICE', 'FIGHTING', 'POISON', 'GROUND', 'FLYING', 'PSYCHIC', 'BUG', 'ROCK', 'GHOST', 'DRAGON']

# Helper Functions

def effect_map(inverted=False) -> dict:
    effect_text = ['NO_EFFECT', 'NOT_VERY_EFFECTIVE', 'SUPER_EFFECTIVE']
    effect_vals = [0, 0.5, 2]
    if inverted: return dict(zip([str(val) for val in effect_vals], effect_text))
    return dict(zip(effect_text, effect_vals))

def format_type(_type:str, as_code:bool=False) -> str:
    _type = _type.strip().upper()
    if as_code: return 'PSYCHIC_TYPE' if _type == 'PSYCHIC' else _type
    return 'PSYCHIC' if _type == 'PSYCHIC_TYPE' else _type

def format_move(move:str, as_code:bool=False) -> str:
    move = move.strip().upper()
    if as_code: return 'PSYCHIC_M' if move == 'PSYCHIC' else move.replace(' ','_')
    return 'PSYCHIC' if move == 'PSYCHIC_M' else move #.replace('_',' ')

def rpad(string:str, target:int) -> str: # right-pads `string` if shorter than `target`.
    amount = target - len(string)
    return string + ' '*amount if amount > 0 else string

def lpad(string:str, target:int) -> str: # left-pads `string` if shorter than `tartet`.
    amount = target - len(string)
    return ' '*amount + string if amount > 0 else string

def safe_print(message:str, **kwargs) -> None:
    if ARGS.quiet and not ARGS.verbose: return
    print(f'easy_edit.py: {message}', **kwargs)

# Export / Update Functions

## Matchups

def export_matchups() -> None: # exports type_matchups.asm to type_matchups.csv
    safe_print('Exporting type_matchups.asm to type_matchups.csv...', end='\r')
    effects = effect_map()
    matchups = { _type: dict.fromkeys(types) for _type in types } # { Attacker : { Defender : Multiplier } }
    with ARGS.data_dir.joinpath('types', 'type_matchups.asm').open() as infile:
        for line in infile.readlines():
            data = line.split(';')[0].split('\tdb')
            if len(data) <= 1 or '-1' in data[-1]: continue
            attacker, defender, effect = [format_type(field) for field in data[-1].split(',')]
            matchups[attacker][defender] = effects[effect]
    with ARGS.csv_dir.joinpath('type_matchups.csv').open('w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        writer.writerow(['', *types])
        for attacker in matchups:
            writer.writerow([attacker, *matchups[attacker].values()])
    safe_print('Exporting type_matchups.asm to type_matchups.csv...Done.')

def update_matchups() -> None: # overwrites type_matchups.asm using type_matchups.csv
    csv_path = ARGS.csv_dir.joinpath('type_matchups.csv')
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
                    attacker = format_type(attacker, as_code=True)+','
                    for d, effect in enumerate(defenders):
                        if not effect: continue
                        defender = format_type(types[d], as_code=True)+','
                        lines.append(f'\tdb {rpad(attacker, 13)} {rpad(defender, 13)} {effects[effect]}')
                lines.append('\tdb -1 ; end')
                lines.append('\n; autogenerated by easy_edit.py')
                outfile.writelines([line+'\n' for line in lines])
        safe_print('Updating type_matchups.asm using type_matchups.csv...Done.')

## Moves

def export_moves() -> None: # exports moves.asm to moves.csv
    safe_print('Exporting moves.asm to moves.csv...', end='\r')
    with ARGS.data_dir.joinpath('moves', 'moves.asm').open() as infile:
        with ARGS.csv_dir.joinpath('moves.csv').open('w') as outfile:
            writer = csv.writer(outfile, delimiter=',')
            writer.writerow(['Name', 'Effect', 'Power', 'Type', 'Accuracy', 'PP'])
            for line in infile.readlines():
                data = line.split(';')[0].split('\tmove')
                if len(data) > 1: 
                    data = [d.strip().upper() for d in data[-1].split(',')]
                    data[0] = format_move(data[0])
                    data[3] = format_type(data[3])
                    writer.writerow(data)
    safe_print('Exporting moves.asm to moves.csv...Done.')

def update_moves() -> None: # overwrites moves.asm using moves.csv
    csv_path = ARGS.csv_dir.joinpath('moves.csv')
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
                    name = format_move(name, as_code=True)
                    _type = format_type(_type, as_code=True)
                    name, effect, _type = [field.strip().upper()+',' for field in [name, effect, _type]]
                    power, accuracy, pp = [lpad(field, 3)+',' for field in [power, accuracy, pp]]
                    lines.append(f'\tmove {rpad(name, 13)} {rpad(effect, 27)} {rpad(power, 4)} {rpad(_type, 13)} {rpad(accuracy, 4)}{pp[:-1]}')
                lines.append('\tassert_table_length NUM_ATTACKS')
                lines.append('\n; autogenerated by easy_edit.py')
                outfile.writelines([line+'\n' for line in lines])
        safe_print('Updating moves.asm using moves.csv...Done.')

## Mon

# Mon data is strictly ordered, so we can use a static list of csv headers and reference by index.
mon_data_labels = [
    'pokedex id pointer -- see data/pokemon/dex_order.asm',
    'base stats (0-255)',
    'type(s) -- enter twice for monotype (ex: BUG BUG)',
    'catch rate (X/255)',
    'base exp (0-255)', 
    'dex sprite -- not advised to chnage here',
    'battle sprite pointers -- see gfx/pics.asm',
    'level 1 learnset -- for empty slot(s) add NO_MOVE',
    'growth rate -- see constants/pokemon_data_constants.asm',
]

# Special cases where mons EvosMoves pointers are formatted with internal camel case.
mon_name_exceptions = {'nidoranm':'NidoranM', 'nidoranf':'NidoranF', 'mrmime':'MrMime'} 

def export_mon() -> None: # exports <ARGS.mon>.asm and evos_moves.asm (partial) to <ARGS.mon>.csv
    safe_print(f'Exporting {ARGS.mon}.asm and evos_moves.asm to {ARGS.mon}.csv...', end='\r')
    indir = ARGS.data_dir.joinpath('pokemon')
    mon_data = [] # see mon_data_labels
    label_index = 0 # see mon_data_labels
    tm_hm_moves = [] # multi-row edge case, excluded from mon_data_labels since they're always at the end
    with indir.joinpath('base_stats', f'{ARGS.mon}.asm').open() as infile:
        for line in infile.readlines():
            data = line.split(';')[0].strip()
            if not data: continue
            if label_index < len(mon_data_labels):
                mon_data.append(data.split(' ', maxsplit=1)[-1].strip().split(','))
                label_index += 1
            elif 'db 0' not in data: tm_hm_moves.extend([move.strip() for move in data.split('tmhm')[-1].strip().split(',') if '\\' not in move])
    evo_data = [] # excluded in code for mons that don't evolve, but included here for consistent formatting
    level_moves = [] # level up learnset and evolution are pulled from a single file (evos_moves.asm) for all mons
    with indir.joinpath('evos_moves.asm').open() as infile:
        mon_header = (mon_name_exceptions[ARGS.mon] if ARGS.mon in mon_name_exceptions else ARGS.mon[0].upper() + ARGS.mon[1:].lower()) + 'EvosMoves:'
        mon_found = False
        in_evos = True
        for line in infile.readlines():
            data = line.split(';')[0].strip()
            if 'EvosMoves:' in data and mon_found: mon_found = False
            if data == mon_header: 
                mon_found = True
                continue # skip header
            if not data or not mon_found: continue
            if 'db 0' in data:
                if in_evos: in_evos = False
                continue
            data = [d.strip() for d in data.split('db', maxsplit=1)[-1].split(',')]
            if in_evos: evo_data.append(data) # evolution, if present, is either 3 or 4 items
            else: level_moves.append(data) # note this is specifically a nested list to include learn level
    with ARGS.csv_dir.joinpath(f'{ARGS.mon}.csv').open('w') as outfile:
        writer = csv.writer(outfile, delimiter=',')
        for i, label in enumerate(mon_data_labels):
            data = [d.strip() for d in mon_data[i]]
            if i in [1, 2, 5, 6, 7]:
                match i:
                    case 1: writer.writerow(['','Hit Points','Attack','Defense','Speed','Special'])
                    case 2: 
                        writer.writerow(['','Type 1','Type 2'])
                        data = [format_type(d) for d in data]
                    case 5: writer.writerow(['','File','(0)','(1)']) # if someone knows how these work please advise
                    case 6: writer.writerow(['','Front','Back'])
                    case 7: 
                        writer.writerow(['','Slot 1','Slot 2','Slot 3','Slot 4'])
                        data = [format_move(d) for d in data]
            writer.writerow([label, *data])
            writer.writerow([]) # readability
        writer.writerow(['evolution(s) -- see data/pokemon/evos_moves.asm'])
        writer.writerow(['if by level...', '(EVOLVE_LEVEL)', 'At Level', 'Evolves To'])
        writer.writerow(['if by stone...', '(EVOLVE_ITEM)', 'With Item', 'Min Level', 'Evolves To'])
        writer.writerow(['if by trade...', '(EVOLVE_TRADE)', 'Min Level', 'Evolves To'])
        writer.writerow(['if fully evolved...', '*Leave blank*'])
        for evo in evo_data: writer.writerow(['', *evo]) # gotta support eevee
        writer.writerow([]) # readability
        writer.writerow(['moves -- must match constants/move_constants.asm (case insensitive)']) # must start with "moves" -- see update_mon()
        writer.writerow(['...by level up -- max 8 !!ORDER MATTERS!!', 'Move Name', 'Learned At'])
        for level, move in level_moves: writer.writerow(['', format_move(move), level])
        writer.writerow([]) # readability
        writer.writerow(['...by TM/HM', 'Move Name']) # first column must end with "TM/HM" -- see update_mon()
        for move in tm_hm_moves: writer.writerow(['', format_move(move)])
    safe_print(f'Exporting {ARGS.mon}.asm and evos_moves.asm to {ARGS.mon}.csv...Done.')

def update_mon() -> None: # imports <ARGS.mon>.csv to <ARGS.mon>.asm and does in-place update of evos_moves.asm
    csv_path = ARGS.csv_dir.joinpath(f'{ARGS.mon}.csv')
    out_path = ARGS.data_dir.joinpath('pokemon')
    if not csv_path.exists(): safe_print(f'{ARGS.mon}.csv not found. Skipping update.')
    elif not out_path.exists(): safe_print(f'{ARGS.mon}.asm not found. Skipping update.')
    else:
        safe_print(f'Updating {ARGS.mon}.asm using {ARGS.mon}.csv...', end='\r')
        data_index = 0 # traverses mon_data_labels, then evos, level up moves, and tm/hm's
        mon_data = [] # see mon_data_labels
        evo_data = [] # nested list for eevee
        level_moves = [] # [[move, level], [move, level], ..., etc.]
        tm_hm_moves = [] # [move1, move2, ..., moveN]
        with csv_path.open() as infile:
            reader = csv.reader(infile, delimiter=',')
            for row in reader:
                if not row: continue
                n_labels = len(mon_data_labels)
                if len(mon_data) < n_labels: # base stats, sprites, etc.
                    if row[0] == mon_data_labels[data_index]:
                        mon_data.append(row[1:])
                        data_index += 1
                elif data_index == n_labels: # evolution(s)
                    if row[0] == '': evo_data.append(row[1:])
                    elif row[0][:5] == 'moves': data_index += 1 # must match section header -- see export_mon()
                elif data_index == n_labels + 1: # level up moves
                    if row[0] == '': level_moves.append(row[1:])
                    elif row[0][-5:] == 'TM/HM': data_index += 1 # must match section header -- see export_mon()
                elif data_index == n_labels + 2: # tm/hm moves    
                    if row[0] == '': tm_hm_moves.append([move for move in row[1:]]) # imports as nested list
        # print('\n')
        # for data in [*evo_data, *level_moves, *tm_hm_moves]:
        #     print(data)
        with out_path.joinpath('base_stats',f'{ARGS.mon}.asm').open('w') as outfile:
            lines = []
            for i, data in enumerate(mon_data):
                data = [d for d in data if d != ''] # sometimes libre fills empty columns
                match i:
                    case 0: line = f'db {data[0]} ; pokedex id'
                    case 1: line = f'db {", ".join([lpad(d, 3) for d in data])}\n\t;   hp  atk  def  spd  spc'
                    case 2: line = f'db {", ".join([format_type(d, as_code=True) for d in data])} ; type'
                    case 3: line = f'db {data[0]} ; catch rate'
                    case 4: line = f'db {data[0]} ; base exp'
                    case 5: line = f'INCBIN {", ".join(data)} ; sprite dimensions'
                    case 6: line = f'dw {", ".join(data)}'
                    case 7: line = f'db {", ".join([format_move(d, as_code=True) for d in data])} ; level 1 learnset'
                    case 8: line = f'db {data[0]} ; growth rate'
                    case _: break
                if i in [0, 1, 4, 6, 8]: line = line + '\n' # clean code
                lines.append(line)
            lines.append('; tm/hm learnset')
            move_index = 0 # rows of 5
            while move_index < len(tm_hm_moves):
                line = ('tmhm ' if move_index == 0 else ' '*5) + ''.join([rpad(format_move(move[0], as_code=True)+',', 14) for move in tm_hm_moves[move_index:move_index+5]]) + '\\'
                move_index += 5
                if move_index >= len(tm_hm_moves): line = line.rsplit(',', maxsplit=1)[0] # clean code
                lines.append(line)
            lines.append('; end\n')
            lines.append('db 0 ; padding')
            lines.append('\n; autogenerated by easy_edit.py')
            outfile.writelines(['\t'+line+'\n' for line in lines])
            # with out_path.open('a') as outfile:
            #     reader_in = csv.reader(infile, delimiter=',')
            #     reader_out = csv.reader(outfile, delimiter=',')
            #     for line in reader_out.readlines:
            #         print(line)
        safe_print(f'Updating {ARGS.mon}.asm using {ARGS.mon}.csv...Done.')
        

# Showtime

if __name__ == '__main__':
    error = None
    if ARGS.update and not ARGS.csv_dir.exists(): error = "CSV data either dosen't exist or wasn't found. Update --csv-dir and try again."
    if not ARGS.data_dir.exists(): error = "Game data either doesn't exist or wasn't found. Update --data-dir and try again."
    if not ARGS.export and not ARGS.update: error = "No operation selected. Set --export or --update and try again."
    if not any([ARGS.all, ARGS.matchups, ARGS.moves, ARGS.mon]): error = "No data category selected. Set --macthups, --moves, or --mon and try again."
    if error:
        safe_print(f'easyedit.py: {error} (Use -h to see options)')
        exit(1)
    os.makedirs(ARGS.csv_dir, exist_ok=True)
    if ARGS.all or ARGS.matchups:
       if ARGS.export: export_matchups()
       if ARGS.update: update_matchups()
    if ARGS.all or ARGS.moves:
        if ARGS.export: export_moves()
        if ARGS.update: update_moves()
    if ARGS.mon:
        ARGS.mon = ARGS.mon.lower() # filenames are all lowercase
        for punct in ['.', '_', "'"]: ARGS.mon = ARGS.mon.replace(punct, '') # Mr.Mime, Farfetch'd, plus "_" to be nice
        if ARGS.export: export_mon()
        if ARGS.update: update_mon()
    elif ARGS.all:
        operation = ('Exporting' if ARGS.export else 'Updating')
        safe_print(f'{operation} data for all pokemon...', end='\r')
        ARGS.quiet = True
        for file in os.listdir(ARGS.data_dir.joinpath('pokemon', 'base_stats')):
            ARGS.mon = file.rsplit('.',maxsplit=1)[0]
            if ARGS.export: export_mon()
            if ARGS.update: update_mon()
        ARGS.quiet = False
        safe_print(f'{operation} data for all pokemon...Done.')