#!/usr/bin/env python
# Record a movie of your computer use, to see how productive your day was!
#   Based on a script by jamak (gist 3068171); I'm just too lazy/inept to
#   install zsh. Also something about an OS X screenshot utility. Yes.

import subprocess, random, string, time

utils = {
    'screenshot': '/usr/bin/scrot -q 50 -m -z {path}/{num:07}.png',
    'movie': 'avconv -f image2 -qscale 2 -same_quant -i {path}/%07d.png {path}/output.mpeg'
}

def outside_call(name, call):
    err = subprocess.call(call, shell=True)
    if err != 0: raise EnvironmentError(err, '{} call failed'.format(name))

def observe_user(output_dir):
    period = 16 #seconds

    cur = 0
    done = False
    while not done:
        outside_call('screenshot',
                     utils['screenshot'].format(path=output_dir, num=cur))
        cur += 1
        try:
            time.sleep(period)
        except KeyboardInterrupt:
            done = True

def main(output_dir):
    outside_call('output directory creation', 'mkdir {}'.format(output_dir))
    observe_user(output_dir)
    outside_call('movie compile', utils['movie'].format(path=output_dir))

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('USAGE: {} output_directory'.format(sys.argv[0]))
    main(sys.argv[1])
