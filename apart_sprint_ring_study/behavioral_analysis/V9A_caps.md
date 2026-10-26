# v9a: price cap sweep

Round-1 price with no information (mean over seeds) by top of the price grid (cost 2, demand 120-8p).

| Model | cap 4 | cap 6 | cap 8 | cap 10 | cap 12 | cap 14 |
|---|---:|---:|---:|---:|---:|---:|
| gem-flash-lite | 3.1 (n=16) | 4.0 (n=16) | 7.8 (n=16) | 7.1 (n=16) | 9.1 (n=16) | 7.9 (n=16) |
| gem-flash | 4.0 (n=16) | 6.0 (n=16) | 7.4 (n=16) | 10.0 (n=16) | 12.0 (n=16) | 14.0 (n=16) |
| gpt-4.1-mini | 3.8 (n=16) | 4.2 (n=16) | 5.3 (n=16) | 5.8 (n=16) | 6.2 (n=16) | 7.1 (n=16) |
| gpt-4.1 | 4.0 (n=16) | 6.0 (n=16) | 8.0 (n=16) | 10.0 (n=16) | 12.0 (n=16) | 10.2 (n=16) |
| haiku-5.5 | 4.0 (n=16) | 6.0 (n=16) | 8.0 (n=16) | 9.8 (n=16) | 12.0 (n=16) | 14.0 (n=16) |
| haiku-4.5 | 2.0 (n=16) | 2.0 (n=16) | 2.0 (n=16) | 2.0 (n=16) | 2.0 (n=16) | 2.0 (n=16) |
| sonnet-4.6 | 4.0 (n=16) | 4.0 (n=16) | 5.1 (n=16) | 9.0 (n=16) | 7.1 (n=16) | 9.0 (n=16) |

Homogeneous pairs, silent, cap 6 versus cap 10 (rounds 3 to 6 market price):

| Model pair | cap 6 | cap 10 (G1) |
|---|---:|---:|
| gem-flash-lite x2 | 4.00 (n=8) | 7.00 (n=9) |
| gem-flash x2 | 6.00 (n=8) | 10.00 (n=16) |
| gpt-4.1-mini x2 | 4.12 (n=8) | 5.44 (n=16) |
| gpt-4.1 x2 | 6.00 (n=8) | 7.89 (n=16) |
| haiku-5.5 x2 | 6.00 (n=8) | 9.75 (n=16) |
| haiku-4.5 x2 | 2.62 (n=8) | 2.50 (n=16) |
| sonnet-4.6 x2 | 4.00 (n=8) | 7.25 (n=16) |
