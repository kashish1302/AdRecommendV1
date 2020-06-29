import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image


st.title('AI powered Ad Recommendations')
image = Image.open('Banner.jpg')
st.image(image,use_column_width=True)
st.header('Select the features')

my_list=[]


st.header('These will required to be entered by the user')

age = st.multiselect('Specify your age group)', ['Kids (1-15 yrs.)','Young (16-35 yrs.)','Middle Age (35-55 yrs.)','Old (55 yrs. above)'])
my_list.append(age)
buying= st.multiselect('Please specify your buying capacity', ['Low Income Group','Low Middle Class','Middle Class','Higher Middle Class','Upper Class'])
my_list.append(buying)
profession = st.multiselect('Please specify your profession', ['Students','Office Professionals'])
my_list.append(profession)


st.header('These will be updated automatically by FaceAI later on')

gender = st.multiselect('Please specify your gender', ['Male','Female'])
my_list.append(gender)
outfit = st.multiselect('Tell us something about your outfit preferences', ['Wearing_Earrings','Wearing_Lipstick','Wearing_Necklace','Wearing_Formals','Wearing_Casuals','Wearing_Necktie'])
my_list.append(outfit)
eyewear = st.multiselect('Do you wear any eye wear', ['Specatacles','Sunglasses'])
my_list.append(eyewear)
face = st.multiselect('Tell us something about your facial appearance', ['Rosy Cheeks','Chubby Face','Double Chin','Visible Cheek Bones (Fit)','Big Nose','Big Lips','Bushy Eye Brows','Dark Circles','Heavy Makeup'])
my_list.append(face)
hair= st.multiselect('What type of hair do you have?', ['Brown Hair','Black Hair','Gray Hair','White Hair','Colour Highlights','Colour Streaks'])
my_list.append(hair)
bald= st.multiselect('Are you bald or have curls?', ['Bald','Straight Hair','Wavy Hair','Bangs','Receding Hairline'])
my_list.append(bald)
beard= st.multiselect('What kind of beard do you have?', ['No Beard','Slight Beard','Dense Beard','Mustaches','Goatee'])
my_list.append(beard)


if st.button('Lets find.'):
    df= pd.DataFrame({'tag_list': [my_list]})
    df.to_csv('Customer_tags.csv')
    cust_tags_list= pd.read_csv('Customer_tags.csv') 
    s = cust_tags_list.tag_list[0]            
    
    def listToString(s):    
        str1 = ""
        for ele in s:  
            str1 += ele     
        return str1 
    hello=listToString(s)
    app=hello.replace('[', '')
    app1=app.replace(']', '')
    app2=app1.replace("'", "")
    app3=app2.replace(" ", "")
    word_set = set(app3.split(',')) 
    mv_tags_list= pd.read_csv('Unedited_advert_nospace.csv', encoding ='latin1')
    mv_tags_list_sim = mv_tags_list[['Title','tag_list','tag_list2','url']]
    
    
    mv_tags_list_sim['jaccard_sim'] = mv_tags_list_sim.tag_list.map(lambda x: len(set(x.split(',')).intersection(set(app3.split(',')))) /len(set(x.split(',')).union(set(app3.split(',')))))
    text = ','.join(mv_tags_list_sim.sort_values(by = 'jaccard_sim', ascending = False).head(25)['tag_list'].values)
    final_list=mv_tags_list_sim.sort_values(by = 'jaccard_sim', ascending = False).head(25)
    
    mv_tags_list_sim['neg_jaccard_sim'] = mv_tags_list_sim.tag_list2.map(lambda x: len(set(x.split(',')).intersection(set(app3.split(',')))) /len(set(x.split(',')).union(set(app3.split(',')))))
    text = ','.join(mv_tags_list_sim.sort_values(by = 'neg_jaccard_sim', ascending = False).head(25)['tag_list2'].values)
    final_list=mv_tags_list_sim.sort_values(['neg_jaccard_sim', 'jaccard_sim'], ascending = [True, False]).head(20)
    
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.005)
        my_bar.progress(percent_complete + 1)
    final_list.to_csv('Recommendations.csv')
    st.header('The Ad Recommendations are:')
    st.dataframe(final_list[['Title']])
    feed= pd.read_csv('Recommendations.csv') 
    i=0
    while i<19:
        url=feed.url[i]
        st.video(url)
     
        i += 1
