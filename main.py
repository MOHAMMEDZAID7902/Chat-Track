import streamlit as st
import preprocessor, helper
import matplotlib.pyplot as plt
import seaborn as sns

import helper

st.sidebar.title("Whatsapp Chat Analyzer")
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color:#18191A;
    }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    "## This is the sidebar"


def add_bg_from_url():
    st.sidebar.markdown(
        f"""
           <style>
           .stApp {{
               background-image: url("https://images.freecreatives.com/wp-content/uploads/2016/04/Solid-Black-Website-Background.jpg");
               background-attachment: fixed;
               background-size: cover
           }}
           </style>
           """,
        unsafe_allow_html=True
    )


add_bg_from_url()

uploaded_files = st.sidebar.file_uploader("Choose a CSV file", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    bytes_data = uploaded_file.read()
    data = bytes_data.decode("utf-8")
    df=preprocessor.preprocess(data)



    user_list= df['users'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"overall")

    selected_user = st.sidebar.selectbox("Show Analysis ",user_list)
    if st.sidebar.button("Show Analysis"):
        num_message , words , audio_msg, video_msg, image_msg, link_msg= helper.fetch_analyze(selected_user,df)


        st.title("Top Statistics")
        col1, col2, col3= st.columns(3)

        with col1:
               st.header("Total Messages")
               st.title(num_message)
        with col2:
                st.header("Total Words")
                st.title(words)
        with col3:
                st.header("Total URLs")
                st.title(link_msg)

        col1, col2, col3 = st.columns(3)

        with col1:
                st.header("Audio Messages")
                st.title(audio_msg)

        with col2:
                st.header("Video Messages")
                st.title(video_msg)

        with col3:
                st.header("Image Messages")
                st.title(image_msg)

        st.title("Monthly Timeline")
        timline_user = helper.group_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timline_user['time'], timline_user['message'],color = 'purple')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        st.title("Daily Timeline")
        timline_daily = helper.date_timeline(selected_user, df)
        fig, ax = plt.subplots()
        ax.plot(timline_daily['date_only'], timline_daily['message'], color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        st.title("Activity Map")
        col1, col2 = st.columns(2)

        with col1:
            timeline_day = helper.activity_day(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(timeline_day.index,timeline_day.values, color='yellow')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            timeline_month = helper.activity_month(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(timeline_month.index,timeline_month.values, color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)


        st.title("Weekly Activity Map")
        heat_map=helper.activity_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(heat_map)
        st.pyplot(fig)



        if selected_user == 'overall':
            st.title("Most Active User")
            x,new_df = helper.most_active_users(df)
            fig , ax = plt.subplots()
            col1,col2 = st.columns(2)
            with col1:
                ax.bar(x.index,x.values , color = 'red')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        word_cloud= helper.create_wordcloud(selected_user,df)
        st.title("Word Cloud")

        fig , ax =plt.subplots()
        ax.imshow(word_cloud)
        st.pyplot(fig)


        most_common = helper.most_common_words(selected_user,df)
        st.title("Common words")

        fig, ax = plt.subplots()
        ax.barh(most_common[0],most_common[1])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        most_emoji= helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1, col2 = st.columns(2)

        with col1:
            st.dataframe(most_emoji)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(most_emoji[1].head(10), labels = most_emoji[0].head(10),autopct="%0.2f")
            st.pyplot(fig)
