import  streamlit as st
import  preprocessor
import help
import matplotlib.pyplot as plt
import seaborn as sns
import time

col1,col2 = st.columns(2);
with col1:
    st.title("Whatsapp Chat Analyzer")
    st.image("whatsapp.png")

with col2:
    st.header("How to use ?")
    st.text("1. Open a chat in whatsapp.")
    st.text("2. Go to Options -> More -> Export chat.")
    st.text("3. Select Export chat WITHOUT MEDIA.")
    st.text("4. Upload this file here.")
    st.text("5. Analyze !!!")
    st.header("Note ->")
    st.text("Before Exporting chat, make sure that\nyour phone follows 24 hour clock format\notherwise change it to 24 hour in phone\nsettings and then upload.")
    st.text("Also make sure that date is in DD/MM/YY \nformat in your phone, NOT in DD/MM/YYYY")
st.sidebar.header("By- Sumit Kumar\nAKA\nKamui-Shurikens")
st.sidebar.write("[Github Repository](https://github.com/Kamui-Shurikens/Whatsapp_chat_analyzer)")
st.sidebar.text("")
st.sidebar.text("")
st.sidebar.text("")
uploaded_file = st.sidebar.file_uploader("Enter your secret chats here...")


if uploaded_file is not None:
    st.snow()
    bytes_data = uploaded_file.getvalue()
    #here bytes data will contain bytes, we need to convert it into utf-8 string
    data = bytes_data.decode('utf-8')
    # st.text(data)  # to print string

    # now we will give this string to preprocessor to get dataframe

    df = preprocessor.preprocess(data);
    st.dataframe(df)

    userList = df['user'].unique().tolist()
    userList.remove('group_notification')
    userList.sort()
    userList.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Who you want to analyze ?",userList)
    if (st.sidebar.button("ANALYZE !!")):
        col1,col2,col3,col4 = st.columns(4)
        total_msg,words,media,links = help.get_stats(selected_user,df)
        with col1:
            st.header("Total Messages")
            st.title(total_msg)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Total Media shared")
            st.title(media)
        with col4:
            st.header("Total Links Shared")
            st.title(links)

        # monthly timeline
        st.title('Monthly-timeline')
        timeline = help.get_monthly_stats(selected_user,df)
        fig,ax = plt.subplots()

        ax.plot(timeline['time'],timeline['message'],color = 'green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #daily timeline
        st.title('Daily-Timeline')
        timeline = help.get_daily_stats(selected_user,df)
        fig,ax = plt.subplots()

        ax.plot(timeline['just_date'],timeline['message'],color = 'cyan')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # Activity
        st.title('ACTIVITY')
        col1,col2 = st.columns(2)

        with col1:
            st.header("Overall Week Activity")
            busy_day = help.get_weekly_activity(selected_user,df)
            fig,ax = plt.subplots()
            ax.bar(busy_day.index,busy_day.values,color='purple')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header("Overall Month Activity")
            busy_month = help.get_monthly_activity(selected_user,df)
            fig, ax = plt.subplots()
            ax.bar(busy_month.index, busy_month.values,color='orange')
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        #Heatmap
        st.title("Average Weekly Heat Map")
        user_heatmap = help.get_heatmap(selected_user,df)
        fig,ax = plt.subplots()
        ax = sns.heatmap(user_heatmap)
        st.pyplot(fig)



        if(selected_user == 'Overall'):

            st.title('Most Active Users')

            col1,col2 = st.columns(2)

            activity = help.most_active(df)
            topmost = activity.head();

            fig, axs = plt.subplots()
            axs.bar(topmost.index,topmost.values,color = 'red')

            with col1:
                plt.xticks(rotation = 'vertical')
                st.pyplot(fig)

            with col2:
                percent_data = round((activity/df.shape[0])*100,2).reset_index().rename(columns={'index':'user','user':'percentage'})
                st.dataframe(percent_data)


        # creating wordcloud whether for single user or for a group

        st.title('WORD CLOUD')
        wc_image = help.get_wordcloud(selected_user,df)
        fig,ax = plt.subplots()
        ax.imshow(wc_image)

        st.pyplot(fig)

        # Most common 20 words analysis

        st.title('Most Common Words')
        most_common = help.get_most20(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(most_common[0],most_common[1])
        plt.xticks(rotation = 'vertical')
        st.pyplot(fig)

        # emoji analysis

        st.title('EMOJI ANALYSIS')
        emoji_df = help.get_emoji_df(selected_user,df)


        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            fig,ax = plt.subplots()
            ax.pie(emoji_df[1],labels = emoji_df[0],autopct = '%0.2f')
            st.pyplot(fig)
        st.balloons()

