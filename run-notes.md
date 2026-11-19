# Run notes — gta6-meme-x-01 (GTA 6 meme on X)

Built 2026-11-20 ~01:30–01:45 WIB (session started after the 2026-11-19T14:00:00Z
opening). DO NOT SUBMIT from here: POST.json is still a placeholder.

## Meme concept

A gamer slumped at his monitor in front of a neon Vice City / Leonida
sunset, loading bar stuck at 99% with an hourglass, empty cans piling up.
Top text: "WAITED 13 YEARS FOR GTA 6 / STILL STUCK AT 99%". Bottom left:
"MEANWHILE, MY AI AGENT ALREADY WON REAL MONEY ON make.fun" — and the
real make.fun ghost (press-kit mark, magenta disc, star coin) big on the
right, worked into the scene's empty lower third rather than pasted as a
sticker. Joke = the 13-year wait + launch-day download; pitch = agents
already earning real money on make.fun, in the meme's own voice.

## Assets used

- Base scene: original AI illustration generated in-session with
  media.generate_image (flat cartoon Vice City skyline, gamer at loading
  screen, no text, no logos, no copyrighted GTA art) —
  `assets/media-generation-gta6-vice-city-gamer-base-0-579fb561-19f5-4f9a-a14f-4d48822d036a.png`
- Ghost/logo: REAL make.fun press assets downloaded from
  https://make.fun/press/ — `assets/mark-1024.png` (used in the meme),
  `assets/mark.svg`, `assets/wordmark.svg`. AI generation was NOT used to
  draw the ghost/logo.
- `render.py` (Python + PIL, DejaVu Sans Bold) builds `meme.png`
  1024×1024 deterministically from base + ghost + big outlined text.

## Visual check (genuine revision)

- v1 defects found by reading meme.png: (1) top line "WAITED 13 YEARS FOR
  GTA 6" clipped at the right edge — the "6" was cut off; (2) bottom text
  ran wide across the gamer's head and body.
- v2 fix (real layout/logic change in render.py, not comments): added a
  `fit_font`/`text_center_fit` auto-shrink so the top line can never clip,
  and re-laid the pitch as five short lines in the empty left column only
  (x <= ~360), clear of the gamer at centre. Ghost bumped 300 -> 310px.
- v2 re-checked at full size and at 480×480 (judge size): top line fully
  visible, all text legible, ghost clearly recognisable at 480×480.
  Final meme.png sha256:
  ff17988c84b35166b636d19a0832765c8b3292ad85d22880ab30f210d902c81f

## Caption draft (for the user to post on X — keep it short)

> Waited 13 years for GTA 6 and I'm still stuck at 99% 😭 Meanwhile my AI
> agent already won real money on @makefunai — people and their agents
> build things and earn real cash in bounties there.
> https://make.fun/bounty/gta6-meme-x-01 makefun-desk-onion-skyline

Carries make.fun (link) + @makefunai tag, play code
`makefun-desk-onion-skyline` (code 0), and the earn-real-money pitch.
Post from the public X account with meme.png attached as the FIRST picture.
Keep the post up and the account public until results are out.

## Revision 1 — Drake Hotline Bling format (2026-11-20 ~02:00 WIB)

User's verbatim instruction: "Revisi gambarnya. Pake meme umum. Atau meme
lagi hype." Prompt file: ~/workspace/makefun/prompt-gta6-meme-x-01-rev1.txt
(OUTSIDE the repo). The 99%-loading gamer meme (commit 7acb922) is replaced
entirely; render.py + meme.png rewritten fresh in-session.

Concept: Drake Hotline Bling, redrawn as an ORIGINAL illustration (no
copyrighted Drake photo, no lifted meme image). Same cartoon character in
both panels (short dark hair, light beard, orange puffer jacket, plain
beige background): TOP panel hand up, looking away, rejecting; BOTTOM
panel smiling, pointing right — straight at the real make.fun ghost.
Top text: "WAITING / 13 YEARS / FOR GTA 6" + "STILL STUCK / AT 99%".
Bottom text: "MY AI AGENT / ALREADY WON / REAL MONEY / ON make.fun",
under the real press-kit ghost (magenta disc, 230px) in the approve half.

Assets (new): `assets/media-generation-drake-reject-panel-0-fdf72acd-...webp`
and `assets/media-generation-drake-approve-panel-0-1d31e28e-...webp` —
original illustrations generated in-session with media.generate_image
(no text, no logos in the generated art; all text added with PIL).
Ghost still the REAL press asset `assets/mark-1024.png`; AI was NOT used
to draw the ghost/logo. Old gamer-base asset stays in the repo (unused).

Layout: 1024x1024, top half text-left / reject-right, white 12px divider,
bottom half approve-left / ghost+text-right. Text blocks use the panel
background colour sampled from the art so they blend; text is DejaVu Sans
Bold, white with black outline, auto-fit so no line can clip.

Visual check (genuine revision):
- v1 defect found by pixel scan, not by eye: the bottom block was 518px
  tall in a 506px half — "ON make.fun" ran to the very last row (row 1023)
  and was clipped at the bottom edge.
- v2 fix (real layout change in render.py): ghost 250 -> 230px, bottom
  font 54 -> 50, plus an assert that the block fits inside the half with
  margin. Lowest dark row in the bottom-right is now 1004 (20px margin).
- v2 re-checked at full size and at 480x480 (judge size): no clipped text,
  all text legible, ghost clearly recognisable, pointing gesture reads as
  pointing at the ghost. Final meme.png sha256:
  cc6d2968a7bb5ecd0201456f42a91e1fa929adcb939e658e645279166321678c

## Revision 2 — GTA "WASTED" death screen (2026-11-20 ~02:00 WIB)

User's verbatim instruction: "Kurang menarik rubah lagi. Nuansa GTA nya
tidak ada dan kurang lucu." Prompt file:
~/workspace/makefun/prompt-gta6-meme-x-01-rev2.txt (OUTSIDE the repo).
The Drake format (commit 3f86874) is replaced entirely; render.py +
meme.png rewritten fresh in-session. DO NOT SUBMIT — no X post exists yet.

Concept: the iconic GTA "WASTED" death screen, drawn as GTA-STYLE text
(no copyrighted GTA art, no lifted screenshot, no trademark logo image).
Fresh original illustration: neon Vice City / Leonida sunset — pink-orange
sky, palm trees, art-deco skyline, neon waterfront — with a Hawaiian-shirt
gamer slumped face-down on the beach, empty cans around him. Across the
open sky, huge grey death-screen lettering "WASTED" (font 184, letter-
spaced, black outline); sub-line "CAUSE OF DEATH: THE 99% LOADING
SCREEN"; a pink loading bar HUD stuck at 99% over the sun/skyline; five
gold wanted stars top-right (GTA HUD detail). Bottom punchline bar with
the REAL press-kit ghost (magenta disc, 104px, clearly recognisable):
"MEANWHILE MY AI AGENT / ALREADY WON REAL MONEY / ON make.fun".

Assets (new): `assets/media-generation-gta6-wasted-vice-city-base-0-9b0b21d1-...png`
— original illustration generated in-session with media.generate_image
(no text, no logos in the generated art; all text added with PIL).
Ghost still the REAL press asset `assets/mark-1024.png`; AI was NOT used
to draw the ghost/logo. Old Drake panels stay in the repo (unused).

Visual check (genuine revision):
- v1 defect found by reading meme.png at full size: the two centred
  bottom lines ran across the gamer's face (head spans x ~700..900 down
  into the bar) — the punchline text talked over the character.
- v2 fix (real layout change in render.py): punchline re-laid as three
  short lines in the LEFT column only (x 130..650, font 32), clear of the
  face; an assert guards the 3-line block against the 116px bar height
  (caught a 1px overflow on the first run — line height tightened 1.18
  -> 1.12). Face now fully visible above the bar.
- v2 re-checked at full size and at 480x480 (judge size): WASTED huge
  and unclipped, sub-line + 99% bar legible, 5 stars readable, ghost
  clearly recognisable, all bottom text legible with no overlaps.
  Final meme.png sha256:
  0616a7e592550efef7832cf2a649b49d7215ca70049be0b6cc3250e69641649e

## POST.json — PLACEHOLDER, MUST BE REPLACED

`POST.json` currently holds `{"url": "https://x.com/<handle>/status/<id>"}`.
It MUST be replaced with the real post URL after the user posts from their
phone and sends the URL. Do NOT submit with the placeholder.

## Bundle notes (for the parent)

- --prompt-origin handed-off
- --prompt-via "subagent task from the main agent"
- Parents (round 1): coordinator session 356eb1fa-4000-4f0e-b0cc-6752af6f9699 +
  main session 710bc693-2de5-453e-a87f-8be6fb75c614
- Parents (revision 1): coordinator session 63eb32f6-46d8-497e-90dc-e026a6c617b7 +
  main session 710bc693-2de5-453e-a87f-8be6fb75c614
- Parents (revision 2): coordinator session 92c77703-9b0f-40d7-ab27-ae36f5394ff1 +
  main session 710bc693-2de5-453e-a87f-8be6fb75c614
- Prompt file (user's verbatim words): ~/workspace/makefun/prompt-gta6-meme-x-01.txt
  ("Gas, buatkan meme-nya")
- Revision 1 prompt file: ~/workspace/makefun/prompt-gta6-meme-x-01-rev1.txt
  ("Revisi gambarnya. Pake meme umum. Atau meme lagi hype.")
  --prompt-origin handed-off, --prompt-via "subagent task from the main agent"
  (same parents as above)
- Competition: gta6-meme-x-01, $500, top 50 share, deadline
  2026-11-23T14:00:00Z (23 Nov 21:00 WIB), FREE entry, quota entries_made 0
  (day cap 3 left 3). Reward locked in Solana escrow — parent's submit
  needs the Solana signature path.
- The parent bundles + submits ONLY after the user posts and sends the
  real X post URL, then replaces POST.json with it.
