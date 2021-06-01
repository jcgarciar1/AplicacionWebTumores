from keras import models
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
def load_models():
    clasificador = models.load_model('/Users/juancgarcia/Downloads/PaginaTesis/PaginaTesis/Modelos/tesisInception2.h5')
    boxes = models.load_model('/Users/juancgarcia/Downloads/PaginaTesis/PaginaTesis/Modelos/tesisNasNet2.h5')
    return clasificador,boxes


# This function will preprocess images.
def preprocess(img, image_size=250):
    image = cv2.resize(img, (image_size, image_size))
    image = image.astype("float") / 255.0

    # Expand dimensions as predict expect image in batches
    image = np.expand_dims(image, axis=0)
    return image


def postprocess(image, class_probs, bounding_box):
    # Split the results into class probabilities and box coordinates
    # First let's get the class label
    label_names = (['meningioma_tumor', 'glioma_tumor', 'no_tumor', 'pituitary_tumor'])
    # The index of class with the highest confidence is our target class
    class_index = np.argmax(class_probs)

    # Use this index to get the class name.
    class_label = label_names[class_index]

    # Now you can extract the bounding box too.

    # Get the height and width of the actual image
    h, w = image.shape[:2]

    # Extract the Coordinates
    x1, y1, x2, y2 = bounding_box[0]

    # Convert the coordinates from relative (i.e. 0-1) to actual values
    x1 = int(w * x1)
    x2 = int(w * x2)
    y1 = int(h * y1)
    y2 = int(h * y2)

    # return the lable and coordinates
    return class_label, (x1, y1, x2, y2), class_probs


def predict_final(image, returnimage=False, scale=0.9):
    # Before we can make a prediction we need to preprocess the image.
    matplotlib.use('Agg')
    processed_image = preprocess(image)
    model,model_boxes = load_models()
    # Now we can use our model for prediction
    class_probs = model.predict(processed_image)
    bounding_box = model_boxes.predict(processed_image)
    # Now we need to postprocess these results.
    # After postprocessing, we can easily use our results
    label, (x1, y1, x2, y2), confidence = postprocess(image, class_probs, bounding_box)

    # Now annotate the image
    if label != "no_tumor":
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 100), 2)
    # cv2.putText(
    #    image,
    #   '{}'.format(label, confidence),
    #    (x1, y2 + int(35 * scale)),
    #    cv2.FONT_HERSHEY_COMPLEX, scale,
    #    (200, 55, 100),
    #    2
    #    )

    # Show the Image with matplotlib

    fig = plt.figure(figsize=(10, 10))
    plt.title(label + " " + str(confidence.max()*100) + "%")
    plt.imshow(image[:, :, ::-1])
    return fig