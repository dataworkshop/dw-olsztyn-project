import imutils


def montage_frames(frames):

    montage = imutils.build_montages(
        image_list=frames,
        image_shape=(frames[0].shape[1], frames[0].shape[0]),
        montage_shape=(len(frames), 1),
    )[0]

    return montage
