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

def get_bar_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 6))
    plt.bar(x,y)
    graph = getGraph()
    return graph

def get_pie_plot(values, labels):
    print(values)
    print(labels)
    plt.switch_backend('AGG')
    plt.figure(figsize = (7, 4))
    plt.pie(values, labels = labels, shadow = True, autopct='%1.0f%%')
    graph = getGraph()
    return graph
