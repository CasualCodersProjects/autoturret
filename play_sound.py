from threading import Thread
import os
import random


def get_sound(sound_name):
    base_dir = os.path.join(os.getenv("HOME"), 'sounds')
    # get a list of all sounds
    sounds = os.listdir(base_dir)
    # use the sound name as a search term and get all matching sounds
    matching_sounds = [s for s in sounds if sound_name in s]
    if len(matching_sounds) == 0:
        print(f'No sounds found for {sound_name}.')
        return ''
    # return a random sound from the list
    return os.path.join(base_dir, random.choice(matching_sounds))


def play_sound(sound_file):
    '''
    Plays a sound file.
    '''

    # check if the file exists
    if os.path.isfile(sound_file):
        # play the sound file
        Thread(target=os.system, args=(f'aplay {sound_file}',)).start()
    else:
        print(f'{sound_file} does not exist.')


if __name__ == '__main__':
    play_sound(get_sound('turret_deploy'))
