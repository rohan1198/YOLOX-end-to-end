resize_parameters = {"dir": "./asl_dataset/",
                     "size": 416}

augmentation_parameters = {
                           "Vertical Flip"        :            [0.5],
                           "Horizontal Flip"      :            [0.5],
                           "Rotate"               :            [0.5, 40],
                           "Resize"               :            [416],
                           "Gaussian Blur"        :            [0.5, 3],
                           "Gaussian Noise"       :            [0.5, 0.3],
                           "RGB Shift"            :            [0.5, 25, 25, 25],
                           "Random Crop"          :            [0.5, 416]
                           }

augmentation_images = {"n": 4}
