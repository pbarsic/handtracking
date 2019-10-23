def group_detections(detection_box, detection_score, detection_category):
    w=[]
    for det in zip(detection_box, detection_score, detection_category):
        m = [ a for a in det[0] ]
        m.append(det[1])
        m.append(det[2])
        w.append(m)
    return w

def group_detections_threshold(detection_box, detection_score, detection_category, threshold):
    w=[]
    for det in zip(detection_box, detection_score, detection_category):
        if det[1] > threshold:
            m = [ a for a in det[0] ]
            m.append(det[1])
            m.append(det[2])
            w.append(m)
    return w

