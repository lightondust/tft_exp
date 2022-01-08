import pandas as pd


def search_multi_text(text_cont, keywords):
    res_all = []
    for k,v in text_cont.items():
        res = search_text(v, keywords)
        for r in res:
            r.append(k)
        res_all += res
    res_df = pd.DataFrame(res_all, columns=['text', 'cont_idx', 'score', 'text_file'])
    return res_df


def search_text(cont, keywords):
    # res_txt = []
    # res_idx = []
    # res_score = []
    res = []
    for idx, c in enumerate(cont):
        flag = False
        score = 0.
        for k in keywords:
            if k in c:
                flag = True
                score += 1
        if flag:
            res.append([c, idx, score])
            # res_txt.append(c)
            # res_idx.append(idx)
            # res_score.append(score)

    return res
    # return [res_txt, res_idx, res_score]
    # res_df = pd.DataFrame([res_txt, res_idx, res_score])
    # res_df = res_df.T
    # res_df.columns = ['text', 'cont_idx', 'score']
    # return res_df