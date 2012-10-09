#!/usr/bin/env python
# Record a movie of your computer use, to see how productive your day was!
#   Based on a script by jamak (gist 3068171); I'm just too lazy/inept to
#   install zsh. Also something about an OS X screenshot utility. Yes.
#
# P.S. It takes a lot of granola to turn a 22 line shell script into a
#   50+ line Python program

import subprocess, random, string, time

utils = {
    'screenshot': '/usr/bin/scrot -q 50 -m -z {output}',
    'movie': 'avconv -f image2 -qscale 2 -same_quant -i {inputs} {output}'
}

def observe_user(output_dir):
    period = 16 #seconds

    cur = 0
    done = False
    while not done:
        if subprocess.call(
            utils['screenshot'].format(
                output='{}/{:07}.png'.format(output_dir, cur)),
                shell=True) != 0:
            return -1
        cur += 1
        try:
            time.sleep(period)
        except KeyboardInterrupt:
            done = True
    return 0

def movie_from_images(input_dir):
    return subprocess.call(utils['movie'].format(
            inputs='{}/%07d.png'.format(input_dir),
            output='{}/output.mpeg'.format(input_dir)), shell=True)

def main(output_dir):
    if subprocess.call(['mkdir', output_dir]) != 0:
        return -1
    if observe_user(output_dir) != 0:
        return -1
    if movie_from_images(output_dir) != 0:
        return -1
    return 0


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('USAGE: {} output_directory'.format(sys.argv[0]))
    elif main(sys.argv[1]) != 0:
        print('There was a problem, aborting...')
