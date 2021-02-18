import sys
import argparse
import subprocess
from pathlib import Path
from tempfile import NamedTemporaryFile


def run_with_live_output(command):
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        text=True
    )

    for line in iter(proc.stdout.readline, ''):
        sys.stdout.write(line, end='')

    return proc.returncode


def concat_videos(videos, dst):
    # Create config
    # Example:
    # file 'file1.mkv'
    # file 'file2.mkv'
    config = ''.join([f"file '{path.resolve()}'\n" for path in videos])

    with NamedTemporaryFile(mode='w') as config_file:
        config_file.write(config)
        config_file.flush()

        command = [
            'ffmpeg',
            '-safe', '0',
            '-f', 'concat',
            '-i', config_file.name,
            '-codec', 'copy',
            str(dst)
        ]
        print('Running:', ' '.join(command))

        run_with_live_output(command)


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('videos', nargs='+', type=Path)
    parser.add_argument('destination', type=Path)

    return parser.parse_args()


def main():
    args = parse_args()

    concat_videos(args.videos, args.destination)


if __name__ == '__main__':
    main()
