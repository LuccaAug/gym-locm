from abc import ABC, abstractmethod

from gym_locm.engine import *
from gym_locm.helpers import *


class Agent(ABC):
    @abstractmethod
    def act(self, state):
        pass


class PassBattleAgent(Agent):
    def act(self, state):
        return Action(ActionType.PASS)


class RandomBattleAgent(Agent):
    def act(self, state):
        return np.random.choice(state.available_actions)


class RuleBasedBattleAgent(Agent):
    def __init__(self):
        self.last_action = None

    def act(self, state):
        castable = list(filter(has_enough_mana(state.current_player.mana),
                               state.current_player.hand))
        summonable = list(filter(is_it(Creature), castable))

        creatures = [c for lane in state.current_player.lanes for c in lane]
        opp_creatures = [c for lane in state.opposing_player.lanes for c in lane]
        can_attack = list(filter(Creature.able_to_attack, creatures))

        green_items = list(filter(is_it(GreenItem), castable))
        red_items = list(filter(is_it(RedItem), castable))
        blue_items = list(filter(is_it(BlueItem), castable))

        if summonable:
            creature = np.random.choice(summonable)
            lane = Lane.LEFT if np.random.choice([0, 1]) == 0 else Lane.RIGHT

            action = Action(ActionType.SUMMON,
                            creature,
                            lane)

            if self.last_action != action:
                self.last_action = action
                return action

        if can_attack:
            creature = np.random.choice(can_attack)
            lane = Lane.LEFT if creature in state.current_player.lanes[0] else Lane.RIGHT

            opp_creatures = state.opposing_player.lanes[lane]
            guards = list(filter(lambda c: c.has_ability('G'), opp_creatures))

            action = Action(ActionType.ATTACK,
                            creature,
                            np.random.choice(guards) if guards else None)

            if self.last_action != action:
                self.last_action = action
                return action

        if creatures and green_items:
            action = Action(ActionType.USE,
                            np.random.choice(green_items),
                            np.random.choice(creatures))

            if self.last_action != action:
                self.last_action = action
                return action

        if opp_creatures and red_items:
            action = Action(ActionType.USE,
                            np.random.choice(red_items),
                            np.random.choice(opp_creatures))

            if self.last_action != action:
                self.last_action = action
                return action

        if blue_items:
            action = Action(ActionType.USE,
                            np.random.choice(blue_items))

            if self.last_action != action:
                self.last_action = action
                return action

        action = Action(ActionType.PASS)

        self.last_action = action

        return action


PassDraftAgent = PassBattleAgent
RandomDraftAgent = RandomBattleAgent


class RuleBasedDraftAgent(Agent):
    def act(self, state):
        for i, card in enumerate(state.current_player.hand):
            if isinstance(card, Creature) and card.has_ability('G'):
                return Action(ActionType.PICK, i)

        return Action(ActionType.PICK, 0)


class IceboxDraftAgent(Agent):
    @staticmethod
    def _icebox_eval(card):
        value = card.attack + card.defense

        value -= 6.392651 * 0.001 * (card.cost ** 2)
        value -= 1.463006 * card.cost
        value -= 1.435985

        value += 5.985350469 * 0.01 * ((card.player_hp - card.enemy_hp) ** 2)
        value += 3.880957 * 0.1 * (card.player_hp - card.enemy_hp)
        value += 5.219

        value -= 5.516179907 * (card.card_draw ** 2)
        value += 0.239521 * card.card_draw
        value -= 1.63766 * 0.1

        value -= 7.751401869 * 0.01

        if 'B' in card.keywords:
            value += 0.0
        if 'C' in card.keywords:
            value += 0.26015517
        if 'D' in card.keywords:
            value += 0.15241379
        if 'G' in card.keywords:
            value += 0.04418965
        if 'L' in card.keywords:
            value += 0.15313793
        if 'W' in card.keywords:
            value += 0.16238793

        return value

    def act(self, state):
        return np.argmax(list(map(self._icebox_eval, state.current_player.hand)))


class ClosetAIDraftAgent(Agent):
    scores = [
        -666,   65,   50,   80,   50,   70,   71,  115,   71,   73,
        43,   77,   62,   63,   50,   66,   60,   66,   90,   75,
        50,   68,   67,  100,   42,   63,   67,   52,   69,   90,
        60,   47,   87,   81,   67,   62,   75,   94,   56,   62,
        51,   61,   43,   54,   97,   64,   67,   49,  109,  111,
        89,  114,   93,   92,   89,    2,   54,   25,   63,   76,
        58,   99,   79,   19,   82,  115,  106,  104,  146,   98,
        70,   56,   65,   52,   54,   65,   55,   77,   48,   84,
        115,   75,   89,   68,   80,   71,   46,   73,   69,   47,
        63,   70,   11,   71,   54,   85,   77,   77,   64,   82,
        62,   49,   43,   78,   67,   72,   67,   36,   48,   75,
        -8,   82,   69,   32,   87,   98,  124,   35,   60,   59,
        49,   72,   54,   35,   22,   50,   54,   51,   54,   59,
        38,   31,   43,   62,   55,   57,   41,   70,   38,   76,
        1, -100, -100, -100, -100, -100, -100, -100, -100, -100,
        -100, -100, -100, -100, -100, -100, -100, -100, -100, -100
    ]

    def _closet_ai_eval(self, card):
        return self.scores[card.id - 1]

    def act(self, state):
        return np.argmax(list(map(self._closet_ai_eval, state.current_player.hand)))
