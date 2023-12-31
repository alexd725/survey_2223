import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import altair as alt
from cryptography.fernet import Fernet
import io
import streamlit_authenticator as stauth


def check_authentication():
    users = list(st.secrets['passwords'].keys())
    passwords = list(st.secrets['passwords'].values())
    usernames = {}
    for i in range(len(users)):
        usernames[users[i]] = {"name": users[i], "password": passwords[i]}

    result = {"usernames": usernames}

    authenticator = stauth.Authenticate(
        result,
        st.secrets['cookie']['name'],
        st.secrets['cookie']['key'],
        st.secrets['cookie']['expiry_days'],
    )

    name, authentication_status, username = authenticator.login(
        'Log in', 'main')
    return authentication_status, authenticator, username


def altair_class_barchart(df, aggregate):
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(
            'value',
            axis=alt.Axis(gridOpacity=0.3,
                          values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                          title='{} score'.format(aggregate)),
            scale=alt.Scale(domain=(0, 10)),
        ),
        y=alt.Y('variable',
                axis=alt.Axis(title=''),
                sort=alt.EncodingSortField(field='value',
                                           order='descending',
                                           op='sum')),
        tooltip=alt.value(None)).transform_aggregate(
            value='{}(value)'.format(aggregate),
            groupby=['variable'],
            #disable tooltip
        )

    chart_text = chart.mark_text(
        align='left',
        baseline='middle',
        dx=3,
    ).encode(text=alt.Text('value:Q', format='.1f'))

    return (chart + chart_text).configure_view(strokeWidth=0).configure_axis(
        grid=False, labelLimit=1000)


def decrypt_data(filepath):
    key = st.secrets['key']

    fernet = Fernet(key)
    with open(filepath, 'rb') as enc_file:
        encrypted = enc_file.read()

    decrypted = fernet.decrypt(encrypted)
    df = pd.read_csv(io.StringIO(decrypted.decode('utf-8')))
    return df


def seaborn_violin_plot(df, question):
    fig = plt.figure(figsize=(10, 3))
    chart = sns.violinplot(data=df,
                           x=question,
                           cut=0,
                           scale='count',
                           linewidth=3,
                           split=True)
    chart.set_xlim(0, 10)
    chart.set_xticks([0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    chart.xaxis.grid(
        True,
        linestyle='dashed',
        which='major',
        color='lightgrey',
    )
    return fig


def plot_bar_chart_classes(df, aggfunction, color_input):

    cols_to_rename = {
        df.columns[1]: 'Standard deviation',
        df.columns[2]: 'Mean',
        df.columns[3]: 'Median'
    }

    df.rename(columns=cols_to_rename, inplace=True)

    df['Standard deviation'] = df['Standard deviation'].round(decimals=1)
    df['Mean'] = df['Mean'].round(decimals=1)
    df['Median'] = df['Median'].round(decimals=1)

    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(aggfunction,
                axis=alt.Axis(gridOpacity=0.3,
                              values=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]),
                scale=alt.Scale(domain=(0, 10))),
        y=alt.Y('Class',
                axis=alt.Axis(title=None, gridOpacity=0.3),
                sort=alt.EncodingSortField(field=aggfunction,
                                           op='sum',
                                           order='descending')),
        tooltip=[
            'Class', 'Standard deviation', 'Response rate (%)', 'Class size',
            'Respondents'
        ],
        color=alt.Color(
            color_input,
            scale=alt.Scale(scheme='goldgreen'),
            legend=alt.Legend(
                direction='vertical',
                titleAnchor='middle',
                orient='right',
                padding=25,
                # legendY=-70,
                # legendX=400,
                gradientThickness=20,
                gradientLength=250,
                tickCount=8)))

    chart_text = chart.mark_text(
        color='white',
        align='left',
        baseline='middle',
        dx=10,
        fontWeight=400,
        dy=0).encode(text=alt.Text('{}'.format(aggfunction)))

    return (chart +
            chart_text).configure_view(strokeWidth=0).configure_axis(grid=True)


global_stats = {
    'The class presents a good challenge for me.': {
        'Standard deviation': 1.8,
        'Mean': 7.1,
    }
}

CLASS_LIST = {
    'AP 2-D Art': 'AP Humanities',
    'AP Art History': 'AP Humanities',
    'AP BIO': 'AP STEM',
    'AP CALC': 'AP STEM',
    'AP CGP': 'AP Humanities',
    'AP CS A': 'AP STEM',
    'AP CSP': 'AP STEM',
    'AP ECON A': 'AP Humanities',
    'AP ECON B': 'AP Humanities',
    'AP ENG Language A': 'AP Humanities',
    'AP ENG Language B': 'AP Humanities',
    'AP ENG Literature': 'AP Humanities',
    'AP EuroHis': 'AP Humanities',
    'AP FRE': 'AP Humanities',
    'AP GER': 'AP Humanities',
    'AP HG': 'AP Humanities',
    'AP PHYS': 'AP STEM',
    'AP PSYCH': 'AP Humanities',
    'AP RESEARCH': 'AP Humanities',
    'AP SEM 3': 'AP Humanities',
    'AP STATS A': 'AP STEM',
    'AP STATS B': 'AP STEM',
    'CES-HSS 1': 'CES',
    'CES-HSS 2A': 'CES',
    'CES-HSS 2B': 'CES',
    'CES-WR 1': 'CES',
    'CES-WR 2': 'CES',
    'CES-WR 3A': 'CES',
    'CES-WR 3B': 'CES',
    'CSem 1': 'CSem',
    'CSem 2A': 'CSem',
    'CSem 2B': 'CSem',
    'CSem 3A': 'CSem',
    'CSem 3B': 'CSem',
    'CSem 3C': 'CSem',
    'CSem 4A': 'CSem',
    'CSem 4B': 'CSem',
    'CSem 4C': 'CSem',
    'EL 1': 'EL',
    'EL 2': 'EL',
    'EL 3N': 'EL',
    'EL 3R': 'EL',
    'EL 4': 'EL',
    'ELL 1': 'ELL',
    'ELL 3': 'ELL',
    'French': 'Language',
    'GER Adv': 'Language',
    'GER Beg': 'Language',
    'LEAF Core: CES-Civics & Law': 'LEAF Core',
    'LEAF Core: CES-Contemporary Threats to Democracy': 'LEAF Core',
    'LEAF Core: Forecasting': 'LEAF Core',
    'LEAF Core: MMS': 'LEAF Core',
    'MATH 1': 'MATH',
    'MATH 2A': 'MATH',
    'MATH 2B': 'MATH',
    'Math-CS 1A': 'MATH',
    'Math-CS 1B': 'MATH',
    'Math-CS 2A': 'MATH',
    'Math-CS 2B': 'MATH',
    'NL-CZ 3+4': 'Language',
    'NL-SK 1': 'Language',
    'NL-SK 2A': 'Language',
    'NL-SK 2B': 'Language',
    'NL-SK 3A': 'Language',
    'NL-SK 3B': 'Language',
    'NL-SK 4A': 'Language',
    'NL-SK 4B': 'Language',
    'Pre-CALC': 'MATH',
    'SCIE 1': 'SCIE',
    'SCIE 2A': 'SCIE',
    'SCIE 2B': 'SCIE',
    'SK as FL 1-3': 'Language',
    'SK as FL 4': 'Language',
}

TEACHERS = {
    'januska': ['AP PSYCH'],
    'crcha': ['CES-HSS 1'],
    'skovajsa': ['CES-WR 1', 'CES-WR 2', 'CES-WR B'],
    'mullerova': ['EL 1', 'ELL 3'],
    'sajbidor': ['ELL 1'],
    'pechova': ['French', 'NL-CZ 3+4'],
    'darina':
    ['GER Beg', 'SK as FL 1-3', 'SK as FL 4', 'GER Adv', 'AP GER', 'AP FRE'],
    'kubseova': ['MATH 1', 'MATH 2A', 'MATH 2B'],
    'kluvanec': ['Math-CS 1A', 'Math-CS 1B', 'Math-CS 2A', 'Math-CS 2B'],
    'zmajkovic': ['CSem 2B', 'CSem 3B', 'CSem 4B'],
    'wetzler': [
        'SCIE 1', 'SCIE 2A', 'AP BIO', 'AP CALC', 'AP CS A', 'AP CSP',
        'AP PHYS', 'AP STATS A', 'AP STATS B', 'MATH 1', 'MATH 2A', 'MATH 2B',
        'Math-CS 1A', 'Math-CS 1B', 'Math-CS 2A', 'Math-CS 2B', 'SCIE 2B',
        'LEAF Core: Forecasting', 'LEAF Core: MMS'
    ],
    'suchy':
    ['NL-SK 4A', 'NL-SK 4B', 'NL-SK 2B', 'NL-SK 1', 'NL-SK 2A', 'NL-SK 3B'],
    'povysilova': ['AP HG', 'SCIE 2B'],
    'podracka': ['CES-HSS 2B', 'CES-HSS 2A', 'AP EuroHis'],
    'piovarci': ['AP ECON A', 'AP ECON B'],
    'pellerova': ['AP STATS A', 'AP STATS B', 'LEAF Core: MMS'],
    'pavlovic': ['AP CALC'],
    'micuch': ['AP CS A', 'AP CSP'],
    'mccavigan': ['AP ENG Language A', 'AP ENG Language B'],
    'lutz': ['EL 3N', 'EL 1', 'EL 2', 'EL 3R', 'EL 4'],
    'kurian': ['LEAF Core: Forecasting', 'AP PHYS'],
    'kiselova': ['EL 2', 'NL-SK 3A'],
    'jelokova': [
        'LEAF Core: CES-Contemporary Threats to Democracy', 'AP CGP',
        'AP SEM 3', 'AP RESEARCH'
    ],
    'hustaty': ['AP Art History', 'AP 2-D Art'],
    'filkaszova': [
        'AP 2-D Art', 'AP Art History', 'AP CGP', 'AP ECON A', 'AP ECON B',
        'AP ENG Language A', 'AP ENG Language B', 'AP ENG Literature',
        'AP EuroHis', 'AP FRE', 'AP GER', 'AP HG', 'AP PSYCH', 'AP RESEARCH',
        'AP SEM 3', 'CES-HSS 1', 'CES-WR 1', 'CES-WR 2', 'CES-WR B', 'ELL 1',
        'French', 'NL-CZ 3+4', 'GER Beg', 'SK as FL 1-3', 'SK as FL 4',
        'GER Adv', 'NL-SK 4A', 'NL-SK 4B', 'NL-SK 2B', 'NL-SK 1', 'NL-SK 2A',
        'NL-SK 3B', 'CES-HSS 2B', 'CES-HSS 2A', 'NL-SK 3A',
        'LEAF Core: CES-Contemporary Threats to Democracy',
        'LEAF Core: CES-Civics & Law'
    ],
    'fiabanova': ['CSem 4A', 'CSem 3A', 'CSem 2A'],
    'beetlestone': [
        'CSem 3C', 'CSem 4C', 'CSEM 1', 'CSem 2C', 'CSem 2A', 'CSem 2B',
        'CSem 3A', 'CSem 3B', 'CSem 4A', 'CSem 4B'
    ],
    'jakabovic': [],
    'townsend': [],
    'pusey': []
}

ALL_ACCESS = ['sapak', 'klagova', 'zavodsky', 'potash', 'retkovsky', 'sedlar']
