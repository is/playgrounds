import math
import json

import cv2
import numpy as np

import star_common as sc

IN = 'star-cache/040__contours.json'
MAX_RANGE = 25
SRC = 'star-cache/x1/s_00.png'

class Matcher(object):
    def __init__(self, max_range):
        self.map = {}
        self.off = 0
        self.max_range = max_range
        self.cur = None


    def tag(self, tag):
        self.cur = tag

    def match(self, p):
        max_range = self.max_range * self.max_range
        min_pi = None
        min_dist = 10000000000000000

        for pi in self.map.values():
            if pi['lock']:
                continue
            dx = pi['cx'] - p['cx'] 
            dy = pi['cy'] - p['cy']
            dist = dx * dx + dy * dy
            if dist < min_dist:
                min_dist = dist
                min_pi = pi

        if min_pi == None:
            return None

        if min_dist < max_range:
            sign = '+'
        else:
            sign = '-'
        pi = min_pi

        dist = math.sqrt(min_dist)
        print(f"""{sign} / {pi['id']}/{pi['src']} / {p['img']}.{p['serial']}: ({pi['cx']:.2f},{pi['cy']:.2f}) / ({p['cx']:.2f},{p['cy']:.2f}) - dst:{dist:.2f}""")
        if min_dist < max_range:
            pi['ps'].append(p)
            pi['tag'] = self.cur
            pi['cx'] = p['cx']
            pi['cy'] = p['cy']
            return pi
        return None

    def add(self, p):
        key = self.off
        self.off += 1
        pi = {
            'id': key,
            'cx': p['cx'],
            'cy': p['cy'],
            'cx0': p['cx'],
            'cy0': p['cy'],
            'ps': [p],
            'src': f"{p['img']}.{p['serial']}",
            'tag': self.cur,
            'lock': False
        }
        self.map[key] = pi
        return pi
    
    def flush(self):
        for pi in self.map.values():
            if pi['tag'] != self.cur:
                pi['lock'] = True


def main():
    with open(IN, 'r') as fin:
        dss = json.load(fin)
    
    matcher = Matcher(MAX_RANGE)
    for ds in dss:
        id, contours = ds
        n = 0
        head = []
        matcher.tag(id)
        for contour in contours:
            contour['img'] = id
            contour['serial'] = n
            n += 1
            
            if matcher.match(contour) == None:
                head.append(contour)
        for contour in head:
            matcher.add(contour)
        matcher.flush()

    for i in range(matcher.off):
        pi = matcher.map[i]
        dx = pi['cx'] - pi['cx0']
        dy = pi['cy'] - pi['cy0']
        dist = math.sqrt(dx * dx + dy * dy)
        if len(pi['ps']) <= 3:
            del matcher.map[i]
            continue
        print(f"{i}: {pi['src']} - {len(pi['ps'])} - move:{dist:.2f}, step:{dist / len(pi['ps']):.2f}")
    print(f"{len(matcher.map)} traces")

    img = cv2.imread(SRC)
    for pi in matcher.map.values():
        ps = pi['ps']
        pts = np.array([[p['cx'], p['cy']] for p in ps]).astype(np.int32)
        pts = pts.reshape(-1, 1, 2)
        cv2.polylines(img, [pts], False, (0, 0, 255), thickness=2)
        for p in ps:
            cv2.drawMarker(img, (int(p['cx']), int(p['cy'])), (255, 255, 255), markerType=0, thickness=1)
        cv2.putText(img, str(pi['id']) + "." + pi['src'][2:],
            (int(pi['cx0']) - 15, int(pi['cy0'])- 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imwrite('star-cache/050__trace.png', img)

if __name__ == '__main__':
    main()