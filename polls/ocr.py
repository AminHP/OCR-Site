__author__ = 'amin'

import models

from ANN.Net.ann import ANN
#from ANN.Trainer.ann_trainer import ANN_Trainer
from ANN.Trainer_RP.ann_trainer import ANN_Trainer as ANN_Trainer


def find_char_rect(raw_data):
    start_x = None
    end_x   = None
    start_y = None
    end_y   = None

    for y in range(len(raw_data)):
        if start_y == None and (sum(raw_data[y])) > 0:
            start_y = y
            break
    for y in range(len(raw_data) - 1, -1, -1):
        if end_y == None and sum(raw_data[y]) > 0:
            end_y = y
            break

    for x in range(len(raw_data[0])):
        _sum = 0
        for y in range(len(raw_data)):
            _sum += raw_data[y][x]

        if start_x == None and _sum > 0:
            start_x = x
            break
    for x in range(len(raw_data[0]) - 1, -1, -1):
        _sum = 0
        for y in range(len(raw_data)):
            _sum += raw_data[y][x]
        if end_x == None and _sum > 0:
            end_x = x
            break

    if start_x == None or end_x == None or start_y == None or end_y == None:
        return ()
    return (start_x, start_y, end_x - start_x, end_y - start_y)

def normalize_data(raw_data, rect, n=5, m=5):
    data = []
    x, y, w, h = rect

    if w < n or h < m:
        return None

    for gx in range(n):
        for gy in range(m):
            part_w = w / n
            part_h = h / m
            start_x = x + gx * part_w
            start_y = y + gy * part_h

            if gx == n - 1:
                part_w = w - (n - 1) * part_w
            if gy == m - 1:
                part_h = h - (m - 1) * part_h

            sum = .0
            for i in range(start_x, start_x + part_w):
                for j in range(start_y, start_y + part_h):
                   sum += float(raw_data[j][i])
            data.append(float(sum / (255. * float(part_w * part_h))))

    return data

def get_raw_data(image):
    width  = image.size[0]
    height = image.size[1]
    pixels = list(image.getdata())

    raw_data = [[0 for x in range(width)] for y in range(height)]
    for x in range(width):
        for y in range(height):
            pos = y * height + x
            if pixels[pos][0] != 0 or pixels[pos][1] != 0 or pixels[pos][2] != 0 or pixels[pos][3] != 0:
                raw_data[y][x] = 255
                #print y, x, data[y][x]
            #data[y][x] = (pixels[pos][0], pixels[pos][1], pixels[pos][2], pixels[pos][3])

    return raw_data


def check(uid, image):
    raw_data = get_raw_data(image)
    del image

    rect = find_char_rect(raw_data)
    if not rect:
        return 'error: blank pattern'

    data = normalize_data(raw_data, rect)
    if data == None:
        return 'error: pattern is too small'

    if not models.Ann_net_data.objects.filter(userid=uid):
        return 'error: no data'

    ann = ANN(uid)
    ann.loadData()

    ann.activate(data)
    char = chr(ann.outputs.index(max(ann.outputs)) + ord('A'))
    del ann

    del rect
    del data
    del raw_data

    return "character is <b>'%s'</b>" %(char)


def add(uid, image, char):
    char = char[0]
    allowed_chars = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    if not char in allowed_chars:
        return "error: character must be A-Z"

    raw_data = get_raw_data(image)
    del image

    rect = find_char_rect(raw_data)
    if not rect:
        return 'error: blank pattern'

    input = normalize_data(raw_data, rect)
    if input == None:
        return 'error: pattern is too small'
    output = [0. for i in range(26)]
    output[ord(char) - ord('A')] = 1.

    models.Ann_samples.objects.create(userid=uid, input=str(input), output=str(output))

    del rect
    del raw_data
    del input
    del output

    return "pattern for '%s' added to database" % (char)


def get_error(uid):
    #record = models.Ann_trainer_data.objects.filter(userid=uid)
    record = models.Ann_trainer_rp_data.objects.filter(userid=uid)
    error = 'infinity'
    if record:
        error = eval(record[0].data)[0][0]
    return str(error)

def train(uid, max_error):
    try:
        max_error = float(max_error)
    except:
        return 'error: max error is not float'

    ann = ANN_Trainer(uid)
    ann.train(max_error)

    return 'trained'


def reset(uid):
    models.Ann_net_data.objects.filter(userid=uid).delete()
    models.Ann_trainer_data.objects.filter(userid=uid).delete()
    models.Ann_trainer_rp_data.objects.filter(userid=uid).delete()
    models.Ann_samples.objects.filter(userid=uid).delete()

    return 'reset all data'
