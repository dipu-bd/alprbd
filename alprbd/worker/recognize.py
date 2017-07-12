from ..helper import recognize_digit, recognize_letter, recognize_city


def recognize(frame):
    """
    recognize segments inside frame
    :param frame: frame to process
    :return: frame after processing
    """

    for plate in frame.plates:
        g = ""
        p = 1.0
        for seg in plate.segments:
            seg = process_segment(seg)
            if len(seg.guess) > 0:
                g = seg.guess[0][0] + g
                p *= seg.guess[0][1]
        # end for
        if len(g) > 0 and p > 0.75:
            plate.guess = [(g, p)]
    # end for

    return frame
# end function


def process_segment(segment):
    """
    process the segment and find the predictions
    :param segment: Segment to process
    :return: processed segment
    """
    g = []
    if segment.serial >= 2:
        g.extend(recognize_digit(segment.image))
    elif segment.serial == 1:
        g.extend(recognize_letter(segment.image))
    else:
        g.extend(recognize_city(segment.image))
    sorted(g, key=lambda x: -x[1])
    segment.guess = g
    return segment
# end function

