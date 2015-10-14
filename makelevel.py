"""
AsteroidImpact Level Generator

This is used to make the standard levels (see makestandardlevels.py) and from the
command-line to make your own custom levels.
"""

import random
from virtualdisplay import GAME_PLAY_AREA
import argparse
import json

SMALL_SIZES = [60, 100, 90, 70, 110, 80]
MEDIUM_SIZES = [110, 120, 150, 120, 140, 130]
LARGE_SIZES = [200, 160, 170, 220, 210, 220]
VARIED_SIZES = SMALL_SIZES + MEDIUM_SIZES + LARGE_SIZES

SLOW_SPEEDS = [2, 3, 3, 4]
MEDIUM_SPEEDS = [4, 6, 6, 7]
FAST_SPEEDS = [10, 12, 12, 14]
EXTREME_SPEEDS = [16, 20, 20, 22]

TARGET_SIZE = 32

def make_dir(speed, rnd):
    """
    Find random dx,dy in range [-speed,speed] that avoid pure horizontal and pure vertical
    movements.
    """
    dx = rnd.randint(1, speed)
    dy = rnd.randint(1, speed)
    if rnd.randint(0, 1) == 1:
        dx = -dx
    if rnd.randint(0, 1) == 1:
        dy = -dy
    return (dx, dy)

def make_level(seed=None,
               target_count=5,
               asteroid_count=3,
               asteroid_sizes='large',
               asteroid_speeds='slow',
               powerup_count=10,
               powerup_initial_delay=0.0,
               powerup_delay=1.0,
               powerup_types='all'):
    """Create the level's details"""

    # convert string args to lists:
    if asteroid_sizes == 'small':
        asteroid_sizes = SMALL_SIZES
    elif asteroid_sizes == 'medium':
        asteroid_sizes = MEDIUM_SIZES
    elif asteroid_sizes == 'large':
        asteroid_sizes = LARGE_SIZES
    elif asteroid_sizes == 'varied':
        asteroid_sizes = VARIED_SIZES

    if isinstance(asteroid_sizes, str):
        raise ValueError('asteroid_sizes of unknown string value: "%s"'%asteroid_sizes)

    if asteroid_speeds == 'slow':
        asteroid_speeds = SLOW_SPEEDS
    elif asteroid_speeds == 'medium':
        asteroid_speeds = MEDIUM_SPEEDS
    elif asteroid_speeds == 'fast':
        asteroid_speeds = FAST_SPEEDS
    elif asteroid_speeds == 'extreme':
        asteroid_speeds = EXTREME_SPEEDS

    if isinstance(asteroid_speeds, str):
        raise ValueError('asteroid_speeds of unknown string value: "%s"'%asteroid_speeds)

    if powerup_types == 'shield':
        powerup_types = ['shield']
    if powerup_types == 'slow':
        powerup_types = ['slow']
    if powerup_types == 'all':
        powerup_types = ['shield', 'slow']
    if powerup_types == 'none':
        powerup_types = ['none']

    if isinstance(powerup_types, str):
        raise ValueError('powerup_types of unknown string value: "%s"'%powerup_types)

    rnd = random.Random(seed)
    level = {}
    target_positions = []
    for i in xrange(target_count):
        target_positions.append(
            (rnd.randint(0, GAME_PLAY_AREA.width - TARGET_SIZE),
             rnd.randint(0, GAME_PLAY_AREA.height - TARGET_SIZE)))
    level['target_positions'] = target_positions

    asteroids = []
    for i in xrange(asteroid_count):
        diameter = rnd.choice(asteroid_sizes)
        speed = rnd.choice(asteroid_speeds)
        dx, dy = make_dir(speed, rnd)
        asteroids.append(dict(
            diameter=diameter, dx=dx, dy=dy,
            top=(rnd.randint(0, GAME_PLAY_AREA.height - diameter)),
            left=(rnd.randint(0, GAME_PLAY_AREA.width - diameter))))
    level['asteroids'] = asteroids

    powerups = []
    if powerup_count > 0 and len(powerup_types) > 0:
        if powerup_initial_delay > 0:
            powerups.append(dict(type='none', duration=powerup_initial_delay))
        for i in xrange(powerup_count):
            powerup_left, powerup_top = \
                (rnd.randint(0, GAME_PLAY_AREA.width - TARGET_SIZE),
                 rnd.randint(0, GAME_PLAY_AREA.height - TARGET_SIZE))
            powerup_type = rnd.choice(powerup_types)
            powerups.append(
                dict(type=powerup_type,
                     diameter=TARGET_SIZE,
                     left=powerup_left,
                     top=powerup_top))
            if powerup_delay > 0.0:
                powerups.append(
                    dict(type='none',
                         duration=powerup_delay))
    else:
        powerups = [dict(type='none', duration=1.0)]

    level['powerup_list'] = powerups

    return level

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create Asteroid Impact level.')
    parser.add_argument('--file', type=str, default=None,
                        help='File to save level json to.')
    parser.add_argument('--seed', type=int, default=None,
                        help='Random number seed. If none supplied will use current time.')
    parser.add_argument('--target-count', type=int, default=5,
                        help='Number of crystals to pick up.')
    parser.add_argument('--asteroid-count', type=int, default=5,
                        help='Number of asteroids to avoid.')
    parser.add_argument('--asteroid-sizes', choices=['small', 'medium', 'large', 'varied'], default='large',
                        help='Approximate size of asteroids.')
    parser.add_argument('--asteroid-speeds', choices=['slow', 'medium', 'fast', 'extreme'], default='slow',
                        help='Approximate speed of asteroids.')
    parser.add_argument('--powerup-count', type=int, default=5,
                        help='Number of asteroids to avoid.')
    parser.add_argument('--powerup-initial-delay', type=float, default=0.0,
                        help='Delay in seconds before first powerup is available.')
    parser.add_argument('--powerup-delay', type=float, default=1.0,
                        help='Delay in seconds after powerup is used before next one becomes available.')
    parser.add_argument('--powerup-types', choices=['shield', 'slow', 'all', 'none'], default='all',
                        help='Types of powerups that are in level.')

    args = parser.parse_args()

    new_level = make_level(
        seed=args.seed,
        target_count=args.target_count,
        asteroid_count=args.asteroid_count,
        asteroid_sizes=args.asteroid_sizes,
        asteroid_speeds=args.asteroid_speeds,
        powerup_count=args.powerup_count,
        powerup_initial_delay=args.powerup_initial_delay,
        powerup_delay=args.powerup_delay,
        powerup_types=args.powerup_types)

    if args.file:
        with open(args.file, 'w') as f:
            json.dump(new_level, f)
        print 'saved level to file "%s"' % args.file
    else:
        print json.dumps(new_level)

        # pretty printing:
        #print json.dumps(new_level, sort_keys=True, indent=4, separators=(',',': '))
