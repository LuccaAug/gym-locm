# gym-locm

A collection of [OpenAI Gym](https://github.com/openai/gym) environments for the collectible card game [Legends of Code and Magic (LOCM)](https://jakubkowalski.tech/Projects/LOCM/).

## Installation

Python 3.6+ is required.
```
git clone https://github.com/ronaldosvieira/gym-locm.git
cd gym-locm
pip install -e .
```

## Usage

```python
import gym
import gym_locm

env = gym.make('LOCM-XXX-vX')

done = False
while not done:
    action = ...  # Your agent code here
    obs, reward, done, _ = env.step(action)
    env.render()
```

## Environments

A match of LOCM has two phases: the **draft**, where the players build their decks, and the **battle**, where the playing actually occurs.

A reward of *1* is given if the controlled player wins the battle phase, and *-1* otherwise. There are no draws. 

### Draft phase only
 ```python
env = gym.make("LOCM-draft-v0")
```

The draft phase is played. A default (configurable) policy is used in the battle phase.

**State**: a 3 x 16 matrix (16 features from each of the 3 cards). 

**Actions**: 0-2 (chooses first, second or third card).

### Battle phase only
 ```python
env = gym.make("LOCM-battle-v0")
```

The battle phase is played. A default (configurable) policy is used in the draft phase.

**State**: a vector with 3 x 20 + 8 values (16 features from each of the 20 possible cards plus 4 features from each player).

**Actions**: 0-144 (pass, summon, use and attack with all possible origins and targets).
<details>
  <summary>Click to see all actions</summary>
    
      0: PASS
      1: SUMMON (card at index 0 of player's hand) 0
      2: SUMMON (card at index 0 of player's hand) 1
      3: SUMMON (card at index 1 of player's hand) 0
      4: SUMMON (card at index 1 of player's hand) 1
      5: SUMMON (card at index 2 of player's hand) 0
                          ⋮
     16: SUMMON (card at index 7 of player's hand) 1
     17: USE (card at index 0 of player's hand) -1
     18: USE (card at index 0 of player's hand) (1st creature at player's lane 0)
     19: USE (card at index 0 of player's hand) (2nd creature at player's lane 0)
     20: USE (card at index 0 of player's hand) (3rd creature at player's lane 0)
     21: USE (card at index 0 of player's hand) (1st creature at player's lane 1)
     22: USE (card at index 0 of player's hand) (2nd creature at player's lane 1)
     23: USE (card at index 0 of player's hand) (3rd creature at player's lane 1)
     24: USE (card at index 0 of player's hand) (1st creature at opponent's lane 0)
     25: USE (card at index 0 of player's hand) (2nd creature at opponent's lane 0)
     26: USE (card at index 0 of player's hand) (3rd creature at opponent's lane 0)
     27: USE (card at index 0 of player's hand) (1st creature at opponent's lane 1)
     28: USE (card at index 0 of player's hand) (2nd creature at opponent's lane 1)
     29: USE (card at index 0 of player's hand) (3rd creature at opponent's lane 1)
     30: USE (card at index 1 of player's hand) -1
     31: USE (card at index 1 of player's hand) (1st creature at player's lane 0)
                          ⋮
    120: USE (card at index 7 of player's hand) (3rd creature at opponent's lane 1)
    121: ATTACK (1st creature at player's lane 0) -1
    122: ATTACK (1st creature at player's lane 0) (1st creature at opponent's lane 0)
    123: ATTACK (1st creature at player's lane 0) (2nd creature at opponent's lane 0)
    124: ATTACK (1st creature at player's lane 0) (3rd creature at opponent's lane 0)
    125: ATTACK (2nd creature at player's lane 0) -1
    126: ATTACK (2nd creature at player's lane 0) (1st creature at opponent's lane 0)
                          ⋮
    133: ATTACK (1st creature at player's lane 1) -1
                          ⋮
    144: ATTACK (3rd creature at player's lane 1) (3rd creature at opponent's lane 0)
    
</details>

### Full match
```python
env = gym.make("LOCM-v0")
```

A full match is played. The draft phase happens in the first 30 turns, with the battle phase taking place on the subsequent turns.

States and actions are the same as listed above, changing according to the current phase.

### Two-player variations
 ```python
env = gym.make("LOCM-draft-2p-v0")
env = gym.make("LOCM-battle-2p-v0")
env = gym.make("LOCM-2p-v0")
```

Both players are controlled alternately. A reward of *1* is given if the first player wins, and *-1* otherwise. 

### Additional options

Some additional options can be configured at env creation time. These are:

#### Set random seed

This option determines the random seed to be used by the environment. In a match, 
the random seed will be used to generate card choices for each draft turn and to 
shuffle both players' deck at the beginning of the battle. To increase reproducibility,
every time the env is reset, its random state is reset, and `seed + 1` is used as seed.

Usage: `env = gym.make('LOCM-XXX-vX', seed=42)`, default: `None`.

#### Set agents for the roles you don't control

By default, random draft and battle agents are used in the roles not controlled by the 
user (e.g. if it's a single-player draft env, a random agent drafts for the opponent 
player, and random agents battles for both players). To specify different agents for 
these roles, use, for instance:

```python
env = gym.make('LOCM-draft-XXX-vX', draft_agent=RandomDraftAgent(),
                battle_agents=(RandomBattleAgents(), RandomBattleAgents()))
env = gym.make('LOCM-battle-XXX-vX', battle_agent=RandomBattleAgent(),
                draft_agents=(RandomDraftAgents(), RandomDraftAgents()))
```

Trying to specify agents for roles you control will result in an error.

<details>
  <summary>Click to see all available agents</summary>
    
Draft agents:
    
- `PassDraftAgent`: always passes the turn (this is equivalent to always choosing the 
first card).
- `RandomDraftAgent`: drafts at random. 
- `RuleBasedDraftAgent`: drafts like Baseline1 from the Strategy Card Game AI competition.
- `MaxAttackDraftAgent`: drafts like Baseline2 from the Strategy Card Game AI competition.
- `IceboxDraftAgent`: drafts using the card ranking created by CodinGame's user Icebox.
- `ClosetAIDraftAgent`: drafts using the card ranking created by CodinGame's user ClosetAI.
- `UJI1DraftAgent`: drafts like UJIAgent1 from the Strategy Card Game AI competition.
- `UJI2DraftAgent`: drafts like UJIAgent2 from the Strategy Card Game AI competition.
- `CoacDraftAgent`: drafts like Coac from the Strategy Card Game AI competitions pre-2020.
- `NativeDraftAgent`: drafts like an AI player developed for the original LOCM engine, 
whose execution command is passed in the constructor (e.g. `NativeDraftAgent('python3 player.py')`).

Battle agents:
- `PassBattleAgent`: always passes the turn. 
- `RandomBattleAgent`: chooses any valid action at random (including passing the turn).
- `RuleBasedBattleAgent`: battles like Baseline1 from the Strategy Card Game AI competition.
- `MaxAttackBattleAgent`: battles like Baseline2 from the Strategy Card Game AI competition.
- `GreedyBattleAgent`: battles like Greedy from Kowalski and Miernik's paper <a href="#kowalski2020">[1]</a>.
- `MCTSBattleAgent`: battles using a MCTS algorithm (experimental). Takes a `time` 
parameter that determines the amount of time, in milliseconds, that the agent is allowed
to "think".
- `NativeDraftAgent`: battles like an AI player developed for the original LOCM engine, 
whose execution command is passed in the constructor (e.g. `NativeBattleAgent('python3 player.py')`).

If NativeDraftAgent and NativeBattleAgent are going to be used to represent the same player,
consider using a single NativeAgent object instead, and passing it as draft and battle agent.
</details>

#### Use item cards

This option determines whether consider green, red and blue item cards in the game. If set to 
false, item cards will not be available to draft, and USE actions will not be 
present on battle envs' action space (ATTACK action codes will start at 17).

Usage: `env = gym.make('LOCM-XXX-vX', items=False)`, default: `True`.

#### Include previously drafted cards to state (draft envs only)

This option determines whether the state of draft envs includes the previously drafted
cards alongside the current card alternatives. If set to true, the state shape of a 
draft env changes from a 3 x 16 matrix to a 33 x 16 matrix, where the 30 first rows 
hold the up to 30 cards drafted in the past turns. The card slots of current and future
picks are filled with zeros.

Usage: `env = gym.make('LOCM-draft-XXX-vX', use_draft_history=True)`, default: `False`.

#### Sort cards in state by mana cost (draft envs only)

This option determines whether the cards in the draft's state matrix will be sorted by 
mana cost in ascending order. This virtually reduces the state space, as every 
possible permutation of three specific cards will result in a single state matrix.

Usage: `env = gym.make('LOCM-draft-XXX-vX', sort_cards=True)`, default: `False`.

#### Change draft length

This option determines the amount of draft turns that will happen, and, therefore, the size 
of the decks built in the draft phase. If `use_draft_history` is `True`, the state representation
in the draft phase will change to accommodate the longer or shorter history of past picks.

Usage: `env = gym.make('LOCM-XXX-vX', n=20)`, default: `30`

#### Change amount of cards alternatives per draft turn

This option determines the amount of random cards that will be presented to the players on 
every draft turn. The state representation and the set of actions in the draft phase will 
change to accommodate the amount of cards options per turn.

Usage: `env = gym.make('LOCM-XXX-vX', k=5)`, default: `3`

## Other resources

### Runner

We provide a command-line interface (CLI) to run LOCM matches. It is available as soon as the
repository is installed. Some basic use cases are listed below.

1. Run 1000 matches in parallel with 4 processes of the Icebox draft agent versus the Coac
draft agent, using random actions in the battle:
    ```bash
    locm-runner --p1-draft icebox --p1-battle random \
                --p2-draft coac --p2-battle random \
                --games 1000 --processes 4
    ```

2. Run 1000 matches of a fully random player against a player developed for the original 
engine, and with a specific random seed:
    ```bash
    locm-runner --p1-draft random --p1-battle random \
                --p2-path "python /path/to/agent.py" \
                --games 1000 --seed 42
    ```

### Train draft agents with deep reinforcement learning

We provide scripts to train deep reinforcement learning draft agents as described in our 
thesis <a href="#vieira2020a">[2]</a> and SBGames 2020 paper <a href="#vieira2020b">[3]</a>. 
Further instructions are available in the README.md file in 
the [experiments](gym_locm/experiments) 
package.

To install the dependencies necessary to run the scripts, install 
the repository with 
```python
pip install -e .['experiments']
```

We also provide a collection of draft agents trained with deep 
reinforcement learning, and a script to use them in the LOCM's original engine.
Further details on these agents and instructions for the script are available in the
README.md in the 
[trained_models](gym_locm/trained_models) 
package. The use of these draft agents with the Runner script is not implemented yet.

### Train battle agents with deep reinforcement learning

We provide scripts to train deep reinforcement learning battle agents as described in our
SBGames 2022 paper <a href="#vieira2022a">[4]</a>. Further instructions are available
in the README.md file in the [experiments/papers/sbgames-2022](gym_locm/experiments/papers/sbgames-2022)
package.

To install the dependencies necessary to run the scripts, install
the repository with
```python
pip install -e .['experiments']
```

## References
1. <span id="kowalski2020">Kowalski, J., Miernik, R. (2020). Evolutionary 
Approach to Collectible Card Game Arena Deckbuilding using Active Genes. arXiv preprint arXiv:2001.01326.</span>

2. <span id="vieira2020a">Vieira, R., Chaimowicz, L., Tavares, A. R. (2020). Drafting in Collectible Card Games via 
Reinforcement Learning. Master's thesis, Department of Computer Science, Federal University 
of Minas Gerais, Belo Horizonte, Brazil.</span>

3. <span id="vieira2020b">Vieira, R., Tavares, A. R., Chaimowicz, L. (2020). Drafting in 
Collectible Card Games via Reinforcement Learning. 19th Brazilian Symposium of Computer Games
and Digital Entertainment (SBGames).</span>

4. <span id="vieira2022a">Vieira, R., Tavares, A. R., Chaimowicz, L. (2022). Exploring Deep 
   Reinforcement Learning for Battling in Collectible Card Games. 19th Brazilian Symposium 
   of Computer Games and Digital Entertainment (SBGames).</span>

## License
[MIT](https://choosealicense.com/licenses/mit/)
