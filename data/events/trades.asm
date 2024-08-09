TradeMons:
; entries correspond to TRADE_FOR_* constants
	table_width 3 + NAME_LENGTH, TradeMons
	; give mon, get mon, dialog id, nickname
	; The two instances of TRADE_DIALOGSET_EVOLUTION are a leftover
	; from the Japanese Blue trades, which used species that evolve.
	; Japanese Red and Green used TRADE_DIALOGSET_CASUAL, and had
	; the same species as English Red and Blue.
	db MANKEY,     HITMONLEE,  TRADE_DIALOGSET_CASUAL, "TERRY@@@@@@"
	db ABRA,       MR_MIME,    TRADE_DIALOGSET_CASUAL, "MARCEL@@@@@"
	db BUTTERFREE, BEEDRILL,   TRADE_DIALOGSET_HAPPY,  "CHIKUCHIKU@" ; unused
	db EXEGGCUTE,  SQUIRTLE,   TRADE_DIALOGSET_HAPPY,  "SAILOR@@@@@"
	db SPEAROW,    FARFETCHD,  TRADE_DIALOGSET_CASUAL, "DUX@@@@@@@@"
	db SLOWBRO,    GOLDUCK,    TRADE_DIALOGSET_CASUAL, "MARC@@@@@@@"
	db POLIWHIRL,  JYNX,       TRADE_DIALOGSET_CASUAL, "LOLA@@@@@@@"
	db STARYU,     CHARMANDER, TRADE_DIALOGSET_HAPPY,  "LIZ@@@@@@@@" ; formerly "DORIS"
	db VULPIX,     BULBASAUR,  TRADE_DIALOGSET_HAPPY,  "CRINKLES@@@"
	db MACHOP,     HITMONCHAN, TRADE_DIALOGSET_CASUAL, "MIKE@@@@@@@" ; formerly "SPOT"
	assert_table_length NUM_NPC_TRADES
