# author: gaoxiaodong
# datetime:2023/6/4 18:46
# poject: PyCharm

"""
description：

"""

from prefect import flow
from prefect.runtime import flow_run, task_run

from flow.tasks.speaker_diarization_tasks import *


def generate_task_name() -> str:
    flow_name = flow_run.flow_name
    task_name = task_run.task_name

    parameters = task_run.parameters
    name = parameters["name"]
    limit = parameters["limit"]

    return f"{flow_name}-{task_name}-with-{name}-and-{limit}"


@flow(
    name='Speaker Diarization Flow',
    description='Speaker Diarization Flow, to extract the speaker from the audio',
)
def speaker_diarization_flow(file_list: Union[List[str], List[Path], Path], export_dir: str):
    audio_iter = upload_audio_files(file_list)
    filtered_audio_iter = extract_audio.map(audio_iter)
    annotation: Annotation = speaker_diarization(filtered_audio_iter)
    rttm: Rttm = export_rttm(annotation, export_dir=export_dir)
    pieces_info: Dict[Speaker, AudioSegment] = split_merge_files(filtered_audio_iter, annotation)
    output = export_audio_files(pieces_info, export_dir=export_dir)



if __name__ == '__main__':
    # f.visualize()
    path = Path('/Users/gaoxiaodong/Downloads/test_audio')
    speaker_diarization_flow(file_list=path, export_dir='./')

    # flow.run(parameters=dict(x=1))  # prints 2
    # flow.run(parameters=dict(x=100))  # prints 101
    # flow.run()  # prints 3
