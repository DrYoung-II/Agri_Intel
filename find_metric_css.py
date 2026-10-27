import streamlit, os, re

st_path = os.path.dirname(streamlit.__file__)
for r, d, fs in os.walk(st_path):
    for f in fs:
        if f.endswith('.js') and 'Metric.CmkuJai4.js' in f:
            fp = os.path.join(r, f)
            with open(fp, 'r', encoding='utf-8', errors='ignore') as jf:
                txt = jf.read()
            m = re.findall(r'L=.*?;', txt)
            for match in m[:10]:
                print(match[:200])
