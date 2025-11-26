Commands:
help                                             - List commands
new --w W --h H --mines M [--seed S]             - Start a new game
show [--reveal]                                  - Print board; --reveal shows mines
(debug/after loss)
open X Y                                         - Reveal cell at (X,Y)
flag X Y                                         - Toggle flag at (X, Y)
chord X Y                                        - On a revealed number: if flags match,
reveal remaining neighbors
hint                                             - Print one certain safe/mine move with
explanatio
step                                             - Apply one deterministic solver step; or
exact small-component ste
auto [--guess] [--limit N]                       - Run solver up to N steps; --guess
allows lowest-risk guesse
prob                                             - Print coarse ASCII probability heatmap
for unknown cell
frontier                                         - Summary: #components, sizes, unknowns
per componen
save path.json                                   - Snapshot game state to JSON
load path.json                                   - Restore snapshot from JSON 
quit | exit                                      - Exit program