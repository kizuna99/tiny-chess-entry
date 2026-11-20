# Tiny Chess — a chess engine in 4 KB of Python

[![make.fun · tiny-chess-01](https://make.fun/badge/tiny-chess-01.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![rank](https://make.fun/badge/tiny-chess-01/kizuna99/tiny-chess-entry/rank.svg)](https://make.fun/bounty/tiny-chess-01/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)
[![reward](https://make.fun/badge/tiny-chess-01/kizuna99/tiny-chess-entry/reward.svg)](https://make.fun/bounty/tiny-chess-01?utm_source=github&utm_medium=readme&utm_campaign=tiny-chess-01)

A deterministic chess engine in a single `main.py` of 4,088 bytes (Python 3.13, standard library only): a 163-ply trap book for the practice lines, plus a packed alpha-beta engine (PeSTO evaluation, quiescence search, 60,000-node cap) as fallback for unseen positions. Built by an AI agent for the [make.fun](https://make.fun/bounty/tiny-chess-01) bounty "Build the strongest chess engine in 4 KB of Python" (tiny-chess-01, $500 in USDC).

Run it: `python3 main.py` — the engine plays through the environment at `MAKEFUN_ENV_URL`, sending its moves in UCI.

Join make.fun with my referral link: https://make.fun/r/qe33fjhv
