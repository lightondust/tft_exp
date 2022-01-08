import streamlit as st
from text.text_data import load_data, search_set_path
from text.text_module import search_multi_text
import urllib

from utils.file import save_json


@st.cache(allow_output_mutation=True)
def _load_data():
    return load_data()


text_data, search_set = _load_data()

params = st.experimental_get_query_params()
page = st.sidebar.selectbox('page', ['', 'search', 'view'])

page_in_query = params.get('page')
if page_in_query:
    page_in_query = page_in_query[0]


def search():
    text_to_search = st.sidebar.multiselect('text', list(text_data.keys()), list(text_data.keys()))
    text_cont = {k:text_data[k] for k in text_to_search}

    keyword = st.text_input('words')
    keywords = keyword.split()

    search_save = st.sidebar.button('save search')
    for w in search_set:
        st.sidebar.write(' '.join(w))
    if search_save:
        if keywords not in search_set:
            search_set.append(keywords)
        save_json(search_set_path, search_set)

    res_df = search_multi_text(text_cont, keywords)
    res_df = res_df.sort_values(by='score', ascending=False)

    itm_per_page = st.number_input('item per page', 0, 100, 10, 1)
    itm_per_page = int(itm_per_page)
    if res_df.shape[0] > itm_per_page:
        page_no = st.slider('page_no', 0, res_df.shape[0] // itm_per_page, 0, 1)
    else:
        page_no = 0

    pre_page = st.button('pre page')
    next_page = st.button('next page')
    if next_page:
        page_no += 1
    if pre_page:
        page_no -= 1

    for item_idx in range(page_no * itm_per_page, page_no * itm_per_page + itm_per_page):
        if item_idx < res_df.shape[0]:
            rec = res_df.iloc[item_idx]
            cont_idx = rec.cont_idx
            score = rec.score
            text_file = rec.text_file

            query = {
                'page': 'view',
                'text_file': text_file,
                'cont_idx': cont_idx
            }
            url = urllib.parse.urlencode(query)
            st.markdown('[{} {} {}](?{})'.format(score, cont_idx, text_file, url))
            st.markdown(text_cont[text_file][cont_idx])

    st.write(keywords)
    print(keywords)


def view():
    text_file_in_query = params.get('text_file')
    text_file_selected = st.sidebar.selectbox('text', [''] + list(text_data.keys()))
    text_file = ''
    if text_file_selected:
        text_file = text_file_selected
    else:
        if text_file_in_query:
            text_file = text_file_in_query[0]

    if text_file:
        st.title(text_file)
        cont = text_data[text_file]

        cont_query = params.get('cont_idx')
        cont_idx_select = st.selectbox('pos', [None] + list(range(len(cont))))
        cont_idx = 0
        if cont_idx_select:
            cont_idx = int(cont_idx_select)
        else:
            if cont_query:
                cont_idx = cont_query[0]

        cont_idx = int(cont_idx)

        itm_no = st.slider('item no', 0, 100, 10, 1)
        itm_no = int(itm_no)

        pre_page = st.button('pre page')
        next_page = st.button('next page')
        if next_page:
            cont_idx += itm_no
        if pre_page:
            cont_idx -= itm_no
        st.write(cont_idx)
        params['cont_idx'] = [cont_idx]
        st.experimental_set_query_params(**params)

        for i in range(cont_idx-itm_no//2, cont_idx+itm_no//2):
            st.write(cont[i])


if page:
    params['page'] = page
    st.experimental_set_query_params(**params)
else:
    if page_in_query:
        page = page_in_query
    if not page_in_query:
        page_in_query = 'search'

st.title(page)


if page == 'search':
    search()
elif page == 'view':
    view()

st.write(params)
