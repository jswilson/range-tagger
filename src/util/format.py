def format_frames_to_hms(frames):
    fps = 29.97 # should be read, i know, thank you.
    total_seconds = frames / fps
    hours = str(int(total_seconds / 3600))
    minutes = str(int(total_seconds / 60 % 60))
    seconds = str(int(total_seconds % 60))

    s = ''
    if hours != '0':
        s += hours.zfill(2) + ':'

    return s + minutes.zfill(2) + ':' + seconds.zfill(2)
