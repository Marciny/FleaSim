def jump_length(counter, fps):  # 250 jednostek / sekunde
        jlength = counter/fps*250
        return jlength

def opposite_sex(sex):
    if sex == 'male':
        opsex = 'female'
    else:
        opsex = 'male'
    return opsex
