from io import BytesIO
import base64
import matplotlib.pyplot as plt

#Change default styling
plt.style.use("ggplot")

#Chance font to Consolas
plt.rcParams['font.sans-serif'] = "Consolas"

#Remove borders.
plt.rcParams["axes.spines.left"] = False
plt.rcParams["axes.spines.right"] = False
plt.rcParams["axes.spines.top"] = False
plt.rcParams["axes.spines.bottom"] = False

#Remove background
plt.rcParams["savefig.transparent"] = True


def getGraph():
    buffer = BytesIO()
    plt.xticks(rotation=15, ha='right') #Rotate the tags on the x-axis
    plt.tight_layout()  #Solution for the tag cropping.
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    plt.plot(x,y)
    graph = getGraph()
    return graph