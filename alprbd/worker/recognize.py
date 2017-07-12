

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

# end function