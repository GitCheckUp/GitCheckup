from io import BytesIO
import base64
import matplotlib.pyplot as plt



def getGraph():
    buffer = BytesIO()
    plt.savefig(buffer, format = 'png')
    buffer.seek(0)
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(10, 5))
    plt.plot(x,y)
    graph = getGraph()
    return graph