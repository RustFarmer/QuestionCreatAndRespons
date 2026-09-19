import webbrowser
from Settings.UpdateProgram.GetFileUrl.getFileUrlForDownload import getFileUrlForDownload


def download():
    url = getFileUrlForDownload().get_url
    print(url)
    webbrowser.open(url)

