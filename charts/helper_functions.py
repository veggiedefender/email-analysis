import gzip
import pickle
from matplotlib import pyplot as plt

plt.style.use('fivethirtyeight')

def load_emails():
    try:
        with gzip.open("../emails.pickle.gz", "rb") as file:
            return pickle.load(file)
    except FileNotFoundError as err:
        raise Exception("Try running downloader.py first to download an archive of your emails.") from err
