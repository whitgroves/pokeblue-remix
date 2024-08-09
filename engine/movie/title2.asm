TitleScroll_In:
; Scroll a TitleMon in from the right.
; hi: speed
; lo: duration
	db $a2, $94, $84, $63, $52, $31, $11, 0

TitleScroll_Out:
; Scroll a TitleMon out to the left.
; hi: speed
; lo: duration
	db $12, $22, $32, $42, $52, $62, $83, $93, 0

TitleScroll:
	ld a, d

	ld bc, TitleScroll_In
	ld d, $88

	and a
	jr nz, .ok

	ld bc, TitleScroll_Out
	ld d, $00
.ok

_TitleScroll:
	ld a, [bc]
	and a
	ret z

	inc bc
	push bc

	ld b, a
	and $f
	ld c, a
	ld a, b
	and $f0
	swap a
	ld b, a

.loop
	ld h, d
	ld l, $48
	call .ScrollBetween

	ld h, $00
	ld l, $88
	call .ScrollBetween

	ld a, d
	add b
	ld d, a

	dec c
	jr nz, .loop

	pop bc
	jr _TitleScroll

.ScrollBetween:
.wait
	ldh a, [rLY] ; rLY
	cp l
	jr nz, .wait

	ld a, h
	ldh [rSCX], a

.wait2
	ldh a, [rLY] ; rLY
	cp h
	jr z, .wait2
	ret
