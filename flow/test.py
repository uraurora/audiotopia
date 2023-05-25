from pyannote.audio import Pipeline
from pyannote.database.util import load_rttm

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

    REFERENCE = f"./audio.rttm"
    reference = load_rttm(REFERENCE)["afjiv"]
    print(reference)
