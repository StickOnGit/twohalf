def simple_pt(cam, xyz, zoom):
    result = xyz[:-1]
    if xyz[2] > cam[2]:
        d = xyz[2] - cam[2]
        for i in range(2):
            result[i] = ((result[i] - cam[i]) / d * zoom) + cam[i]
    return result
