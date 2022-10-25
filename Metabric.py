import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
import hiplot as hip
from pySankey import sankey
from matplotlib.patches import Patch


st.title("METABRIC patient data visualizations")
st.header('Created by Carson Broeker')


df = pd.read_csv("data_clinical_patient.txt", sep="\t", skiprows=[1,2,3,4])
df = df.dropna()

agree = st.checkbox('Show full METABRIC patient data table.')

if agree:
    st.dataframe(data=df)


options_all = st.multiselect(
    'Explore different associations between variables in the METABRIC dataset.',
    ['index',
 '#Patient Identifier',
 'Lymph nodes examined positive',
 'Nottingham prognostic index',
 'Cellularity',
 'Chemotherapy',
 'Cohort',
 'ER status measured by IHC',
 'HER2 status measured by SNP6',
 'Hormone Therapy',
 'Inferred Menopausal State',
 'Sex',
 'Integrative Cluster',
 'Age at Diagnosis',
 'Overall Survival (Months)',
 'Overall Survival Status',
 'Pam50 + Claudin-low subtype',
 '3-Gene classifier subtype',
 "Patient's Vital Status",
 'Primary Tumor Laterality',
 'Radio Therapy',
 'Tumor Other Histologic Subtype',
 'Type of Breast Surgery',
 'Relapse Free Status',
 'Relapse Free Status (Months)'],
    ['Age at Diagnosis', 'Relapse Free Status (Months)', 'Overall Survival (Months)'])


df_hiplot = df[options_all]
biggy = hip.Experiment.from_dataframe(df_hiplot)
biggy.to_streamlit().display()

option_category = st.selectbox(
    'Did you know that there are many different subtypes of breast cancer? Check different options to see how different \
        subtypes funnel to other categories.',
    ['Cellularity',
 'Chemotherapy',
 'ER status measured by IHC',
 'HER2 status measured by SNP6',
 'Hormone Therapy',
 'Inferred Menopausal State',
 'Sex',
 'Integrative Cluster',
 'Overall Survival Status',
 'Pam50 + Claudin-low subtype',
 '3-Gene classifier subtype',
 "Patient's Vital Status",
 'Primary Tumor Laterality',
 'Radio Therapy',
 'Tumor Other Histologic Subtype',
 'Type of Breast Surgery',
 'Relapse Free Status'])

st.set_option('deprecation.showPyplotGlobalUse', False)

sankey_fig = sankey.sankey(
    df["Pam50 + Claudin-low subtype"], df[option_category], 
    aspect=20, fontsize=12, #figureName="Breast_Cancer"
)
st.pyplot(fig=sankey_fig)

st.write("These subtypes are referred to as 'intrinsic' subtypes which are determined by examining gene expression\
    signatures of each breast tumor. Most often in the clinic, treatment decisions are based on the protein expression or lack thereof\
        of three different genes: the estrogen receptor, the progesterone receptor, and HER2. If you lack expression\
            of all of these genes, you are referred to as triple-negative. Watch the video below to learn more!")

st.video("https://www.youtube.com/watch?v=6gm494IIHxQ")

number = st.number_input("What percentage of women on average can expect to be diagnosed with \
    breast cancer at some point in their lifetime?", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

if number < 12.5:
    st.write("No, the number is higher!")
elif number > 12.5:
    st.write("No, the number is smaller!")
else:
    st.write("That's right! About 12.5\% of women or 1 out of 8 women will be diagnosed with breast \
        cancer at some point in their lifetime.")

number_death = st.number_input("What percentage of women on average can expect to die from \
    breast cancer at some point in their lifetime?", min_value=0.0, max_value=100.0, value=50.0, step=0.5)

if number_death < 3.0:
    st.write("No, the number is higher!")
elif number_death > 3.0:
    st.write("No, the number is smaller!")
else:
    st.write("Correct. About 3.125\% of women or 1 out of 32 women will ultimately die of breast cancer.")

violin_options = st.selectbox(
    'However, odds of survival have increased dramatically in recent history for breast cancer.\
    Odds of survival also depend on subtype of breast cancer diagnosed and other factors. Vary the parameters to \
        view the different rates of survival by different factors.',
    ['Cellularity',
 'Chemotherapy',
 'ER status measured by IHC',
 'HER2 status measured by SNP6',
 'Hormone Therapy',
 'Inferred Menopausal State',
 'Sex',
 'Integrative Cluster',
 'Overall Survival Status',
 'Pam50 + Claudin-low subtype',
 '3-Gene classifier subtype',
 "Patient's Vital Status",
 'Primary Tumor Laterality',
 'Radio Therapy',
 'Tumor Other Histologic Subtype',
 'Type of Breast Surgery',
 'Relapse Free Status'])


violin_plot = sns.violinplot(data=df, x=violin_options, y="Overall Survival (Months)")

#plt.xticks(rotation=15)
ax = plt.gca()
plt.draw()

for tick in ax.get_xticklabels():
    tick.set_rotation(20)

st.pyplot(ax.figure)
plt.close()

#numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
#newdf = df.select_dtypes(include=numerics)
#newdf = newdf.astype('float64')
#df_z = newdf.apply(zscore)
#df_x = df_z.T

options_numeric = st.multiselect(
    'Explore how the different numeric variables in the dataset cluster together. What interesting associations do you find? Do certain subtypes of breast cancer cluster with different variables? Please use at least two variables.',
    ['Lymph nodes examined positive',
 'Nottingham prognostic index',
 'Cohort',
 'Age at Diagnosis',
 'Overall Survival (Months)',
 'Relapse Free Status (Months)'],
    ['Age at Diagnosis', 'Relapse Free Status (Months)', 'Overall Survival (Months)', 'Lymph nodes examined positive'])

newdf = df[options_numeric]
species = df.pop("Pam50 + Claudin-low subtype")
lut = dict(zip(species.unique(), ["blue","pink", "yellow", "red", "#98F5FF", "green", "black"]))
row_colors = species.map(lut)
newdf = newdf.astype('float64')
#df_z = newdf.apply(zscore)
df_x = newdf.T

cluster_fig = sns.clustermap(df_x, vmin=-3, vmax=3, cmap='icefire', method='ward', z_score=0, col_colors=row_colors)

handles = [Patch(facecolor=lut[name]) for name in lut]
plt.legend(handles, lut, title="Intrinsic Subtype", fontsize='large', \
    bbox_to_anchor=(1,1), bbox_transform=plt.gcf().transFigure, loc='upper right')

st.pyplot(cluster_fig)
plt.close()
heatmap_fig = sns.heatmap(data=(df.corr()), vmin=-1, vmax=1, cmap="icefire")

st.write("If you are having trouble seeing these correlations, look at the heatmap below that shows \
    the correlation value between each numeric parameter.")

st.pyplot(heatmap_fig.figure)