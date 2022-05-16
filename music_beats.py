import librosa


x, sr = librosa.load('electronic-rock-king-around-here.mp3')


tempo, beat_frames = librosa.beat.beat_track(
    x, sr=sr)

beat_times = librosa.frames_to_time(beat_frames, sr=sr)
beat_times = [round(elem, 2) for elem in beat_times]
# print(beat_times)
