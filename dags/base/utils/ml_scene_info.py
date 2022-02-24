def extract_info_from_question_heading(heading):
    if 'ambiente Embonor' in heading:
        return {'scene': 2, 'sub_scene': 1}
    elif 'ambiente de la competencia' in heading:
        return {'scene': 2, 'sub_scene': 2}
    elif 'equipos de frío Embonor' in heading:
        return {'scene': 1, 'sub_scene': 1}
    elif 'equipos de frío de la competencia' in heading:
        return {'scene': 1, 'sub_scene': 2}
    else:
        raise ValueError(f'Unrecognized scene and sub_scene from question heading: {heading}')
