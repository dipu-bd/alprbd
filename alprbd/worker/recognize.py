

def recognize(frame):
    """
    recognize segments inside frame
    :param frame: frame to process
    :return: frame after processing
    """

    for plate in frame.plates:
        for seg in plate.segments:
            process_segment(seg)
        # end for
    # end for

# end function


def process_segment(segment):
    """
    process the segment and find the predictions
    :param segment: Segment to process
    :return: processed segment
    """
    g = []
    g.extend(recognize_letter(segment.image))
    g.extend(recognize_digit(segment.image))
    g.extend(recognize_city(segment.image))
    g = [(l, round(p * 100, 2)) for l, p in g]
    segment.guess = sorted(g, key=lambda x: -int(x[1] * 100))
    return segment
# end function


def recognize_digit(digit):
    """
    recognize the digit
    :param digit: digit to recognize
    :return: recognition with probabilities
    """

    return []
# end function


def recognize_letter(letter):
    """
    recognize the letter
    :param letter: letter to recognize
    :return: recognition with probabilities
    """

    return []
# end function


def recognize_city(image):
    """
    recognize the letter
    :param image: letter to recognize
    :return: recognition with probabilities
    """

    return []
# end function

