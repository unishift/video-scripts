import sys
import json


def get_gop_structure(video_path):
    from subprocess import run
    p = run(['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_frames', str(video_path)], capture_output=True, text=True)
    frames_info = json.loads(p.stdout)
    return ''.join([(v['pict_type'] if 'pict_type' in v else 'E') for v in frames_info['frames'] if v['media_type'] == 'video'])


if __name__ == '__main__':
    video_path = sys.argv[1]

    for i, frame_type in enumerate(get_gop_structure(video_path)):
        if frame_type in 'IE':
            print(frame_type, i)
