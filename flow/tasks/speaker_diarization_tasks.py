from functools import reduce
from os import PathLike
from pathlib import Path
from tempfile import TemporaryFile, NamedTemporaryFile
from typing import List, Iterator, Dict, Optional, Tuple, Union, Callable

from prefect import task
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment
from pyannote.database.util import load_rttm
from pydub import AudioSegment

Speaker = str

FileName = str

Rttm = Dict[FileName, Annotation]

DiarizationFormat = Union[Rttm, Annotation]

StrPath = Union[str, PathLike[str]]  # stable
BytesPath = Union[bytes, PathLike[bytes]]  # stable
StrOrBytesPath = Union[str, bytes, PathLike[str], PathLike[bytes]]  # stable


@task
def upload_audio_files(
        file_list: Union[List[str], List[Path], Path],
        audio_formats: List[str] = None
) -> Iterator[AudioSegment]:
    # file upload
    if audio_formats is None:
        audio_formats = ['.mp3', '.wav', '.flac', '.aac', '.ogg']
    if isinstance(file_list, Path):
        if not file_list.is_dir():
            raise FileNotFoundError(f'dir {file_list} not found')
        file_list = [x for _audio_format in audio_formats for x in file_list.glob(f'**/*{_audio_format}')]
    # todo: validate and signal
    print(file_list)
    for file in file_list:
        path = Path(file)
        if not path.is_file():
            raise FileNotFoundError(f'file {file} not found')
        file_ext: str = path.suffix
        audio: AudioSegment = AudioSegment.from_file(file, format=file_ext)
        yield audio


@task
def extract_audio(audio: AudioSegment) -> AudioSegment:
    # audio extract and filter
    return audio


@task
def speaker_diarization(
        audios: Iterator[AudioSegment],
        num_speakers: Optional[int] = None,
        min_speakers: Optional[int] = None,
        max_speakers: Optional[int] = None,
        hook: Optional[Callable] = None
) -> DiarizationFormat:
    """
    speaker diarization based on pyannote audio lib
    :param audios: audios to be handled, pydub format
    :param num_speakers: speaker numbers, if you are sure
    :param min_speakers: min number of speakers
    :param max_speakers: max number of speakers
    :param hook: callable hook
    :return: annotation
    """
    # Speaker diarization, output rttm format
    pipeline = Pipeline.from_pretrained('pyannote/speaker-diarization@2.1',
                                        use_auth_token='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')

    # apply the pipeline to an audio file
    with NamedTemporaryFile(suffix='.wav') as temp:
        path = Path(temp.name)
        reduce(lambda x, y: x + y, audios, AudioSegment.empty()).export(path, format='wav')
        annotation: Annotation = pipeline(
            path,
            num_speakers=num_speakers,
            min_speakers=min_speakers,
            max_speakers=max_speakers,
            hook=hook
        )

    # dump the diarization output using RTTM format
    return annotation


@task
def export_rttm(annotation: Annotation, export_dir: StrPath = './') -> Rttm:
    # export rttm files
    rttm_file = Path(export_dir) / f'audio-{annotation.uri}.rttm'
    with open('audio.rttm', 'w') as rttm:
        annotation.write_rttm(rttm)
    return load_rttm(rttm_file)


@task
def split_merge_files(audios: Iterator[AudioSegment], format: DiarizationFormat) -> Dict[Speaker, AudioSegment]:
    # split files into slices based on rttm
    if isinstance(format, dict):
        speakers: Dict[Speaker, Tuple[AudioSegment, List[Segment]]] = {
            speaker: (seg, segments)
            for seg in audios
            for speaker, segments in convert_rttm(format).items()
        }
    elif isinstance(format, Annotation):
        speakers: Dict[Speaker, Tuple[AudioSegment, List[Segment]]] = {
            speaker: (seg, segments)
            for seg in audios
            for speaker, segments in convert_annotation(format).items()
        }
    else:
        raise ValueError(f'Invalid format: {format}')

    # merge audio segments
    return {
        speaker: reduce(
            lambda x, y: x + y,
            [file[seg.start * 1000:seg.end * 1000] for seg in segments],
            AudioSegment.empty()
        )
        for speaker, (file, segments) in speakers.items()
    }


@task
def export_audio_files(audios: Dict[Speaker, AudioSegment], export_dir: str) -> List[str]:
    # export audio files
    res = []
    for speaker, audio in audios.items():
        name = f'{export_dir}/{speaker}.wav'
        audio.export(name, format='wav')
        res.append(name)
    return res


def convert_annotation(annotation: Annotation) -> Dict[Speaker, List[Segment]]:
    return {
        key:
            [seg for seg, track_name, label in annotation.itertracks(yield_label=True) if label == key]
        for key in annotation.labels()
    }


def convert_rttm(rttm: Rttm) -> Dict[Speaker, List[Segment]]:
    return reduce(lambda d1, d2: {**d1, **d2}, map(convert_annotation, rttm.values()), dict())
