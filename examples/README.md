# Examples
Welcome to the example files! These serve as a tangible complement to the [Documentation Portal](https://pulsefire.iann838.com). They cover fundaments of the library, as well as provide standalone scripts that can be ran and referenced for your own projects.

> [!Note]
> Examples for other Riot games are needed! PRs welcome

## Running Example Scripts
All example scripts require an environment variable set for `RIOT_API_KEY`. One can be acquired [here](https://developer.riotgames.com/apis).

### Running League of Legends Examples
Files with starting with **summoner** or **champion** require a name be passed be when running the script.
```
python path/to/example_script.py [summoner or champion name]

python ./examples/lol/summoner_ranks.py "Not a Whale"
python ./examples/lol/champion_abilities.py Jinx
```