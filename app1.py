# Define a function to visualize the bounding boxes on the images
def visualize(img, boxes):
    img = np.array(img)
    for box in boxes:
        x1, y1, x2, y2 = box
        img = cv2.rectangle(img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    img = Image.fromarray(img)
    return img
