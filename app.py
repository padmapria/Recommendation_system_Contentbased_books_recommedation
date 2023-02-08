import pickle,os,requests
import streamlit as st
import pandas as pd
import bz2
import pickle
import _pickle as cPickle

st.header('Book Recommender System')


# Load any compressed pickle file
def decompress_pickle(file):
    data = bz2.BZ2File(file, 'rb')
    data = cPickle.load(data)
    return data


# Read our model file from compressed pickle
books_df = decompress_pickle('book_list.pbz2')
similarity = decompress_pickle('similarity.pbz2')


#books_df = pickle.load(open('models/book_list.pkl', "rb"))
#similarity = pickle.load(open('models/similarity.pkl', "rb"))



#Get the list of books
books_list = books_df['title'].values

# Select a book from dropdown
selected_book = st.selectbox(
    "select a book from the dropdown",
    books_list
)

#Recommend most similar book
def recommend(book):
    index = books_df[books_df['title'] == book].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recomm_book_names = []
    for i in distances[1:6]:
        recomm_book_names.append(books_df.iloc[i[0]].title)
   
    return recomm_book_names


#https://docs.streamlit.io/library/api-reference/data/st.dataframe
if st.button('Recommend books'):
    recomm_book_names = recommend(selected_book)
    
    def load_data():
        return pd.DataFrame(
            {
                "Recommended BookList": recomm_book_names
            }
        )

    # Boolean to resize the dataframe, stored as a session state variable
    #st.checkbox("Use container width", value=False, key="use_container_width")

    df = load_data()

    # Display the dataframe and allow the user to stretch the dataframe
    # across the full width of the container, based on the checkbox value
    st.dataframe(df)


#For testing purpose        
#st.text_area("Write some text")
#st.text_input("Write some text")
#st.number_input("Write some number")
        
# Add css to make text bigger
st.markdown(""" <style> .font {
font-size:25px;} 
</style> """, unsafe_allow_html=True)

st.markdown(
    """
    <style>
    .font {
        font-size:50px;
    } 
    textarea {
        font-size: 1rem !important;
    }
    input {
        font-size: 3rem !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

        