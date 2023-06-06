from typing import Dict, List, Tuple

from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment
from pyannote.pipeline import Pipeline
from pyannote.database.util import load_rttm
from pydub import AudioSegment

from flow.tasks.speaker_diarization_tasks import *

if __name__ == '__main__':
    # pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization@2.1",
    #                                     use_auth_token="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")
    #
    # # apply the pipeline to an audio file
    # diarization = pipeline("/Users/gaoxiaodong/Downloads/audio/afjiv.wav")
    #
    # # dump the diarization output to disk using RTTM format
    # with open("audio.rttm", "w") as rttm:
    #     diarization.write_rttm(rttm)

    wav = '/Users/gaoxiaodong/Downloads/audio/afjiv.wav'
    # REFERENCE = f"./audio.rttm"
    # rttm: Rttm = load_rttm(REFERENCE)
    # annotation: Annotation = rttm["afjiv"]
    # print(annotation)
    # audio_file: AudioSegment = AudioSegment.from_file(wav, format='wav')
    # files = [audio_file]
    # speakers = split_merge_files.fn(files, annotation)
    # export_audio_files.fn(speakers, './')


