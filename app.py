import flask
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = flask.Flask(__name__, template_folder='templates')

df = pd.read_csv('model/Weighted_Average.csv')
df2 = pd.read_csv('model/FinalData.csv')
df4 = pd.read_csv('model/FinalComputer.csv')

count = CountVectorizer(stop_words='english')
count_matrix = count.fit_transform(df2['Name'])
cosine_sim = cosine_similarity(count_matrix, count_matrix)
df2 = df2.reset_index()
indices = pd.Series(df2.index, index=df2['Name'])
all_titles = [df2['Name'][i] for i in range(len(df2['Name']))]

count2 = CountVectorizer(stop_words='english')
count_matrix2 = count2.fit_transform(df4['name'].apply(lambda x: np.str_(x)))
cosine_sim2 = cosine_similarity(count_matrix2, count_matrix2)
df4 = df4.reset_index()
indices2 = pd.Series(df4.index, index=df4['name'])
all_titles2 = [df4['name'][i] for i in range(len(df4['name']))]



def get_recommendations(title):
    cosine_sim = cosine_similarity(count_matrix, count_matrix)
    idx = indices[title]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    game_indices = [i[0] for i in sim_scores]
    tit = df2['Name'].iloc[game_indices]
    dat = df2['Genres'].iloc[game_indices]
    pic = df2['PicURL'].iloc[game_indices]
    decs = df2['Description'].iloc[game_indices]
    return_df = pd.DataFrame(columns=['Name','Genres','PicURL','Description'])
    return_df['Name'] = tit
    return_df['Genres'] = dat
    return_df['PicURL'] = pic
    return_df['Description'] = decs
    
    return return_df

def get_recommendations2(title):
    cosine_sim2 = cosine_similarity(count_matrix2, count_matrix2)
    idx2 = indices2[title]
    sim_scores2 = list(enumerate(cosine_sim2[idx2]))
    sim_scores2 = sorted(sim_scores2, key=lambda x: x[1], reverse=True)
    sim_scores2 = sim_scores2[1:11]
    movie_indices2 = [i[0] for i in sim_scores2]
    tit2 = df4['name'].iloc[movie_indices2]
    dat2 = df4['genres'].iloc[movie_indices2]
    dev2 = df4['developer'].iloc[movie_indices2]
    pic2 = df4['header_image'].iloc[movie_indices2]
    return_df2 = pd.DataFrame(columns=['name','genres','developer','header_image'])
    return_df2['name'] = tit2
    return_df2['genres'] = dat2
    return_df2['developer'] = dev2
    return_df2['header_image'] = pic2
    return return_df2


# Setup the main route
@app.route('/mobile', methods=['GET', 'POST'])
def recommend():
    if flask.request.method == 'GET':
        return(flask.render_template('searchmobile.html')) 
    if flask.request.method == 'POST':
        g_name = flask.request.form['game_name']
        g_name = g_name.title()
        if g_name not in all_titles:
            return(flask.render_template('failed.html',name=g_name))
        else:
            result_final = get_recommendations(g_name) 
            names = []
            genre = []
            picurl = []
            decs = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                genre.append(result_final.iloc[i][1])
                picurl.append(result_final.iloc[i][2])
                decs.append(result_final.iloc[i][3])
            #return recommendation
            return flask.render_template('mobilegame.html',game_names=names,game_genre=genre,game_decs=decs,game_pic=picurl,search_name=g_name)



@app.route('/')
def indexpage():
       
            return flask.render_template("index.html")

@app.route('/video', methods=['GET', 'POST'])
def recommend2():
    if flask.request.method == 'GET':
        return(flask.render_template('searchvideo.html')) 
    if flask.request.method == 'POST':
        g_name = flask.request.form['game_name']
        g_name = g_name.title()
        if g_name not in all_titles2:
            return(flask.render_template('failed.html',name=g_name))
        else:
            result_final = get_recommendations2(g_name) 
            names = []
            genre = []
            developer = []
            picurl = []
            for i in range(len(result_final)):
                names.append(result_final.iloc[i][0])
                genre.append(result_final.iloc[i][1])
                developer.append(result_final.iloc[i][2])
                picurl.append(result_final.iloc[i][3])
            #return recommendation
            return flask.render_template('videogame.html',game_names=names,game_genre=genre,game_dev=developer,game_pic=picurl,search_name=g_name)


@app.route('/simple')
def simple():
       
            Name = df.Name 
            Genres = df.Genres
            PicURL = df.PicURL 
            Average_User_Rating = df.Average_User_Rating
            User_Rating_Count = df.User_Rating_Count
            weighted_average = df.weighted_average
            return flask.render_template("top10mobile.html", game_names=Name,game_genre=Genres,game_pic=PicURL,average=Average_User_Rating, count=User_Rating_Count, weight=weighted_average)


@app.route('/simple2')
def simple2():
       
            name = df4.name
            genre = df4.genres
            developer = df4.developer
            positive_ratings = df4.positive_ratings
            header_image = df4.header_image
            price = df4.price
            return flask.render_template("top10video.html", game_names=name,game_genre=genre,game_dev=developer,game_rate=positive_ratings,game_pic=header_image,game_price=price)



@app.route('/contact')
def contactform():
       
            return flask.render_template("contact.html")

@app.route('/dataplan')
def dataplan():
       
            return flask.render_template("dataplan.html")



if __name__ == '__main__':
    app.debug = True
    app.run()