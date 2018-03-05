from numpy import random
import cv2

def read_words_dict(filename="dict"):
    with open(filename, encoding="utf8") as d:
        words = d.readlines()
    words = [w.strip() for w in words]
    return words

def randwords(words=None):
    if words is None:
        words = read_words_dict()
    
    b = words[random.randint(len(words)-1)] + " " + words[random.randint(len(words)-1)] + " " +words[random.randint(len(words)-1)]
    return b, words

def generate_meme(image, top_text=None, bottom_text=None, words=None, thickness=3,
                  fontScale=2, color=(255,255,255), top_offset=0.15, bottom_offset=0.9):
    if top_text is None:
        top_text, words = randwords(words)
    if bottom_text is None:
        bottom_text, words = randwords(words)
    texted_image = np.copy(image)
    fontFace = 3
    baselineTop=0;
    baselineBottom = 0;
    textSizeTop, baselineTop = cv2.getTextSize(top_text, fontFace,
                            fontScale, thickness)
    textSizeBottom, baselineBottom = cv2.getTextSize(bottom_text, fontFace,
                            fontScale, thickness)

    baselineTop += thickness
    baselineBottom += thickness

    x_top = int((texted_image.shape[1] - textSizeTop[0]) / 2)
    y_top = int(texted_image.shape[0] *0.15)
    x_bottom = int((texted_image.shape[1] - textSizeBottom[0]) / 2)
    y_bottom = int(texted_image.shape[0] *0.9)
    texted_image =cv2.putText(img=texted_image, text=top_text, 
                          org=(x_top,y_top),fontFace=fontFace, fontScale=fontScale, color=color, thickness=thickness)

    texted_image =cv2.putText(img=texted_image, text=bottom_text, 
                          org=(x_bottom,y_bottom),fontFace=fontFace, fontScale=fontScale, color=color, thickness=thickness)

    return texted_image

def generate_memes(directory, words=None):
    for folder in glob.glob(directory):
        if len(glob.glob(folder+"/*")) <10:
            for filename in glob.glob(folder+"/*"):
                for i in range(10):
                    meme = cv2.imread(filename)
                    meme = generate_meme(meme, words=words)
                    saveas = filename.split("/")[-1]
                    path = "/".join(filename.split('/')[:-1])
                    saveas = path+ "/{}_generated_{}".format( i, saveas)
                    cv2.imwrite(saveas, meme)
                    