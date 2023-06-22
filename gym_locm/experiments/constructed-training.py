import argparse
from gym_locm.agents import InspiraiConstructedAgent
from gym_locm.envs.constructed import LOCMConstructedSingleEnv

from sb3_contrib import MaskablePPO
from sb3_contrib.common.maskable.utils import get_action_masks

import wandb
from wandb.integration.sb3 import WandbCallback


def get_arg_parser():
    p = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    p.add_argument("--learning_rate", help="path to draft model", default="draft.json")
    p.add_argument("--batch_size", help="path to draft model", default="draft.json")
    p.add_argument("--n_steps", help="path to draft model", default="draft.json")
    p.add_argument("--n_epochs", help="path to draft model", default="draft.json")
    return p

def run(args):
    agent = InspiraiConstructedAgent()
    env = LOCMConstructedSingleEnv(constructed_agent=agent)

    wandb.init(
        sync_tensorboard=True,
        config=vars(args),
    )

    model = MaskablePPO(
        "MlpPolicy", 
        env, 
        verbose=1, 
        tensorboard_log='.',
    )
    
    model_name = f"models/{args.learning_rate}_{args.batch_size}_{args.n_steps}_{args.n_epochs}"
    callbacks = [WandbCallback(gradient_save_freq=0, verbose=0, model_save_freq=10000, model_save_path=model_name)]
    model.learn(
        total_timesteps= 50000, 
        callback= callbacks
    )

    obs = env.reset()
    done = False
    while not done:
        # Retrieve current action mask
        action_masks = get_action_masks(env)
        action, _states = model.predict(obs, action_masks=action_masks)
        state, reward, done, info = env.step(action)

if __name__ == '__main__':
    # get arguments
    arg_parser = get_arg_parser()
    args = arg_parser.parse_args()
    run(args)