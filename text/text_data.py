import glob
import os

import streamlit as st
from utils.file import load_json

search_set_path = './data/text/search_set/search.json'


def read_text_contents(doc_path):

    with open(doc_path, 'r') as f:
        cont = f.readlines()

    return cont


def load_data():
    if os.path.exists(search_set_path):
        search_set = load_json(search_set_path)
    else:
        search_set = []

    files = glob.glob('./data/text/text_files/*.txt')
    files.sort()
    text_data = {}
    for f in files:
        k = f.split('/')[-1].replace('.txt', '')
        text_data[k] = read_text_contents(f)
    return text_data, search_set

