#!/usr/bin/env python
# Record a movie of your computer use, to see how productive your day was!
#   Based on a script by jamak (gist 3068171); I'm just too lazy/inept to
#   install zsh. Also something about an OS X screenshot utility. Yes.
#
# P.S. It takes a lot of granola to turn a 22 line shell script into a
#   50+ line Python program

import subprocess, random, string, time

utils = {
    # Assumes utility that uses scrot syntax
    'screenshot': ['/usr/bin/scrot', '-q', '100', '-m', '-z'],

    # Assumes utility that uses ffmpeg/avconv movie compilation syntax
    'movie': ['avconv', '-f', 'image2', '-qscale', '2', '-same_quant']
}

def observe_user(output_dir):
    period = 16 #seconds

    cur = 0
    done = False
    while not done:
        if subprocess.call(
            utils['screenshot'] +
                ['/tmp/{}/{:07}.png'.format(output_dir, cur)]) != 0:
            return -1
        cur += 1
        try:
            time.sleep(period)
        except KeyboardInterrupt:
            done = True
    return 0

def movie_from_images(input_dir, output_file):
    return subprocess.call(utils['movie'] +
                           ['-i', '/tmp/{}/%07d.png'.format(input_dir),
                            output_file])

def main(outfile):
    output_dir = 'pt-' + ''.join(random.choice(string.printable[:62])
                                 for x in range(20))
    if subprocess.call(['mkdir', '/tmp/{}'.format(output_dir)]) != 0:
        return -1
    if observe_user(output_dir) != 0:
        return -1
    if movie_from_images(output_dir, outfile) != 0:
        return -1
    subprocess.call(['rm', '-r', '/tmp/{}'.format(output_dir)])
    return 0


if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('USAGE: {} output_filename'.format(sys.argv[0]))
    elif main(sys.argv[1]) != 0:
        print('There was a problem, aborting...')
