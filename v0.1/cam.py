from parameters import *

class MyCamera(object):
    def __init__(self, camera_func):
        self.camera_func = camera_func
        self.offset = [0, 0]
        
    def posupd (self, pos):
        posx = pos[0] + self.offset[0]
        posy = pos[1] + self.offset[1]
        return posx, posy

    def update(self, offpos):
        self.offset =  self.camera_func(self.offset, offpos)

    def center(self, offset):           # późniejsze camera.update(mousepos) kontroluje, czy ekran nie będzie pokazywał obszaru poza mapą
        l, t =  round(half_width - offset[0]), round(half_height - offset[1])
        self.offset = [l,t]


def complex_camera(current_offset, offpos):
# l1, t1 to jest ostatnie położenie myszki przekształcone w wektor dodany do
# obecnego offsetu; ustawienia : ruch zaczyna się, gdy myszka jest na krańcach
# (ćwierć ekranu)
#na końcu warunki graniczne
    l1, t1,  = offpos
    l1, t1 = half_width - l1, half_height - t1 
    
    if l1 > half_width/2:
        l1 = l1 - half_width/2
    elif l1 < - half_width/2:
        l1 = l1 + half_width/2
    else:
        l1 = 0

    if t1 > half_width/2:
        t1 = t1 - half_width/2
    elif t1 < - half_width/2:
        t1 = t1 + half_width/2
    else:
        t1 = 0

    l1, t1 = round(l1/4), round(t1/4)
        
    l2, t2 = current_offset
    l3, t3 = l1 + l2, t1 + t2
    
    l3 = min(0, l3)                            # stop scrolling at the left edge
    l3 = max(-(map_width - screen_width), l3)   # stop scrolling at the right edge
    t3 = max(-(map_height - screen_height), t3) # stop scrolling at the bottom / t3 = max(-(map_height - screen_height + bar_height), t3)
    t3 = min(0, t3)                           # stop scrolling at the top

    return l3, t3

#### tu instancję tworzę - nie wiem, czy to dobra praktyka
camera = MyCamera(complex_camera)

