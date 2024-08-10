WildMonEncounterSlotChances:
; There are 10 slots for wild pokemon, and this is the table that defines how common each of
; those 10 slots is. A random number is generated and then the first byte of each pair in this
; table is compared against that random number. If the random number is less than or equal
; to the first byte, then that slot is chosen.  The second byte is double the slot number.
	db  48, $00 ; 49/256 = 19.1% chance of slot 0
	db  97, $02 ; 49/256 = 19.1% chance of slot 1
	db 146, $04 ; 49/256 = 19.1% chance of slot 2
	db 171, $06 ; 25/256 =  9.8% chance of slot 3
	db 196, $08 ; 25/256 =  9.8% chance of slot 4
	db 221, $0A ; 25/256 =  9.8% chance of slot 5
	db 231, $0C ; 10/256 =  3.9% chance of slot 6
	db 241, $0E ; 10/256 =  3.9% chance of slot 7
	db 251, $10 ; 10/256 =  3.9% chance of slot 8
	db 255, $12 ;  4/256 =  1.6% chance of slot 9
