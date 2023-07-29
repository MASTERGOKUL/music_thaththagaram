import streamlit as st
import pandas as pd

# ===========================================      required characters   ==============================
kuril_eluthu = ['அ', 'இ', 'உ', 'எ', 'ஒ', 'க', 'ங', 'ச', 'ஞ', 'ட', 'ண', 'த', 'ந', 'ப', 'ம', 'ய', 'ர', 'ல', 'வ', 'ழ', 'ள',
                'ற', 'ன']
uyir_mei_eluthu = ['ி', 'ு', 'ெ', 'ொ']
alagu = {'1': "நேர்", "0": "நேர்", "10": "நேர் ", "11": "நிரை ", "110": "நிரை"}
mei_eluthu = ['க்', 'ங்', 'ச்', 'ஞ்', 'ட்', 'ண்', 'த்', 'ந்', 'ப்', 'ம்', 'ய்', 'ர்', 'ல்', 'வ்', 'ழ்', 'ள்', 'ற்',
              'ன்']
thaalam = {"தேமா": "தாதீம்", "புளிமா": "தகதீம்", "கூவிளம்": "தாதிமி", "கருவிளம்": "தகதிமி",
           "கூவிளங்காய்": "தாதிமிதா", "கருவிளங்காய்": "தகதிமிதா", "கூவிளங்கனி": "தாதிமிதக", "கருவிளங்கனி": "தகதிமிதக",
           "தேமாங்காய்": "தாதீம்தா", "புளிமாங்காய்": "தகதீம்தீம்", "தேமாங்கனி": "தாதீம்தக", "புளிமாங்கனி": "தகதீம்தக"}


# ===============================================  functions  of alagidutha   ==========================================


# split the words where it has 'மெய்யெழுத்துக்கள்'
def split_mei(word):
    seer, start = [], 0
    # iterates the word using index
    for index in range(len(word)):
        if word[index] == "்":
            seer.append(word[start:index - 1])
            start = index + 1
        #  to add last 'சீர்'  if it does not end with 'மெய்யெழுத்துக்கள்'
        if index == len(word) - 1:
            for i in word[start:]:
                if i not in mei_eluthu:
                    seer.append(word[start:])
                    break
    return seer


# to identify letters as kuril or nedil
def is_kuril(letter):
    return letter in kuril_eluthu


def is_uyir_mei(letter):
    return letter in uyir_mei_eluthu


# this function simplifies kuril as '1' and nedil as '0'
def simplify(asai):
    index = 0
    for seer in asai:
        seer_index = 0
        for letter in seer:
            n = ""
            letter_index = 0
            for char in letter:
                if is_kuril(char) and (len(letter) < 1 or not is_uyir_mei(asai[index][seer_index][letter_index])):
                    n += "1"
                elif is_uyir_mei(char):
                    pass
                else:
                    n += "0"
                letter_index += 1
            asai[index][seer_index] = n
            seer_index += 1
        index += 1
    return asai


def print_alagu(seer):
    table = []
    if len(seer) > 1 and seer[0] != "1":
        table.append(alagu[seer[0]])
        table.append(print_alagu(seer[1:]))
    elif (len(seer) > 2) and seer[2] != "0":
        table.append(alagu[seer[:2]])
        table.append(print_alagu(seer[2:]))
    elif (len(seer) > 2) and seer[2] == "1":
        table.append(alagu[seer[:2]])
        table.append(print_alagu(seer[2:]))
    else:
        table.append(alagu[seer])
    return table


def seer_asai(seer):
    result = []
    for index in seer:
        value = []
        for sr in index:
            if sr!='':
                value.append(print_alagu(sr))
        result.append(value)
    return result

def res_vaipadu(i):
    s = ""
    if isinstance(i, list):
        for j in i:
            if s == "":
                s += res_vaipadu(j)
            else:
                s += " " + res_vaipadu(j)
    else:
        if s == "":
            s = "".join(i).rstrip()
        else:
            s = s + " " + ("".join(i).rstrip())
    return s


def paa_vagai(Lines, linenum):
    # eetrasai=Lines[-1].split(" ")[-1][-1 : -3]
    # bool = eetrasai =='ய்' or eetrasai not in kuril_eluthu and eetrasai not in uyir_mei_eluthu
    if linenum > 2:
        s, ind = [], 0
        for i in Lines:
            s.append(len(Lines[ind].split(" ")))
            ind += 1
        if s[0] + s[-1] == 8 and s[-2] < 4:
            if s == [4] * linenum:
                return "நிலைமண்டில ஆசிரியப்பா"
            elif s[-3] < 4:
                return "இணைக்குறள் ஆசிரியப்பா"
            else:
                return "நேரிசை ஆசிரியப்பா"
    else:
        return "குறள் வெண்பா"


lineNum = 0
lines = []


def lineExtraction(string):
    paatuLines = string.split("\n")
    for sol in paatuLines:
        if sol.strip() != "":
            lines.append(sol.strip())
    return lines


# ===========================================      execution code      ===========================================
# to change the title and icon

st.set_page_config(page_title="தமிழ் Music", page_icon=":notes", layout="wide", initial_sidebar_state="collapsed")
st.title("🪘தத்தகாரம்")  # like h1 tag
# to add background image

st.markdown(
    """
    <style>
    table{
    margin-top:20px;
    }
      th{
      text-align:center !important;
      color:#fff !important;
            background-color: #f99;
        }
    *::selection{
    color:#fff;
    background-color:rgb(49, 51, 63);
    }
     .stApp {
     background-image: url('assets/mummy_background_image.png') ;
     background-size: cover;
     background-position:center;
 }
    a[href="//streamlit.io"]{
    display:none;
    }
    footer::after {
    content: " ❤ by GOKUL " !important;
    }
    footer{
    user-select:none;
    }
    header{
    display:none !important;
    }
    .block-container{
    width:80%;
    }
    .css-10trblm{
    text-align:center !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
col1, col2 = st.columns([0.5, 0.5])

# with col1:
sentence = st.text_area('Enter Your Text', '''''')
btn = st.button('Enter')
# split the sentence into a list of words

alagiduvaipadu = {}
table_show = {"சொல்": [], "சீர்": [], "அசை": [], "தாளசொற்கட்டு": []}
# with col2:
flag = False
for line in (sentence.split("\n")):
    words = line.split(" ")
    seers = list(map(split_mei, words))
    simplify(seers)
    #  to list 'சீர்' without 'மெய்யெழுத்துக்கள்'
    vaipadu = seer_asai(seers)
    ans = []
    for i in vaipadu:
        s = res_vaipadu(i)
        ans.append(s)
    seer_vaipadu = {"நேர்": "நாள்",
                    "நிரை": "மலர்",
                    "நேர் நேர்": "தேமா",
                    "நிரை நேர்": "புளிமா",
                    "நிரை நிரை": "கருவிளம்",
                    "நேர் நிரை": "கூவிளம்",
                    "நேர் நேர் நேர்": "தேமாங்காய்",
                    "நிரை நேர் நேர்": "புளிமாங்காய்",
                    "நிரை நிரை நேர்": "கருவிளங்காய்",
                    "நேர் நிரை நேர்": "கூவிளங்காய்"}
    temp = {}
    temp_table = []
    a = 0
    for i in ans:
        if i != "":
            flag = True
            temp[words[a]] = {i: seer_vaipadu[i]}
            table_show["சொல்"].append(words[a])
            table_show["சீர்"].append(i)
            table_show["அசை"].append(seer_vaipadu[i])
            table_show["தாளசொற்கட்டு"].append(thaalam[seer_vaipadu[i]])
            a = a + 1
    alagiduvaipadu[line] = temp
df = pd.DataFrame(table_show)
df.index = range(1, len(df) + 1)

if flag and btn:
    lineExtraction(sentence)
    paa = paa_vagai(lines, len(lines))
    st.subheader(" பா வகை : "+paa)
    st.table(df)
