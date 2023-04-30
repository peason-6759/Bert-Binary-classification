import os
import re
import pandas as pd
import sqlalchemy
from sqlalchemy.orm  import declarative_base
from sqlalchemy.orm import sessionmaker

engine = sqlalchemy.create_engine("mariadb+mariadbconnector://root:@127.0.0.1:3306/cofacts_testdata")

class Base(object):
    __table_args__ = {'mysql_charset': 'utf8'}
Base = declarative_base()

class Articles(Base):
    __tablename__ = "articles"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key = True, autoincrement=True,nullable = False)
    origin_id = sqlalchemy.Column(sqlalchemy.String(64), primary_key = True, nullable = False)
    article = sqlalchemy.Column(sqlalchemy.Text(), nullable = True)
    rumor_status = sqlalchemy.Column(sqlalchemy.Boolean, nullable = False)

def addArticle(origin_id, article, rumor_status):
    # except_pattern = re.compile("["
    #         u"\U0001F600-\U0001F64F"  # emoticons
    #         u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    #         u"\U0001F680-\U0001F6FF"  # transport & map symbols
    #         u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
    #         "]+", flags=re.UNICODE)
    # article = except_pattern.sub(r'', article)
    article = re.sub(r'http\S+', '', article)
    if article.isspace() or len(article) == 0:
        raise ValueError
    
    article = article.encode('utf-8')
    newArticle = Articles(origin_id = origin_id,
                          article = article,
                          rumor_status = rumor_status)
    try:
        session.add(newArticle)
        session.commit()
    except:
        ValueError("some problem while handling article")
        print("problem: ",article)

    

if __name__ == "__main__":
    
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)  # write after class bulit, because it need to build article

    Session = sessionmaker()
    Session.configure(bind=engine)
    session = Session()
    try:
        os.chdir("data/cofacts_datasets")
        replies_file = 'article_replies.csv'
        article_file = 'articles.csv'
        df_replies = pd.read_csv(replies_file, index_col=None, header=0, engine='python', encoding='utf-8')
        df_articles = pd.read_csv(article_file, index_col=None, header=0, engine='python', encoding='utf-8')
        # df_articles = df_articles.dropna(subset=['text'])
        # df_articles = df_articles[~df_articles['text'].str.contains('http')]
        # print(df_replies.columns.tolist())
        # print(df_articles.columns.tolist())

        for _,row in df_replies.iterrows():
            if row.replyType == "OPINIONATED":
                # print('OPINIONATED')
                continue
            elif session.query(Articles).filter(Articles.origin_id == row["articleId"]).first() is not None:
                continue

            matched_article = df_articles['id'] == row["articleId"]
            article = df_articles[matched_article].head(1).iloc[0]['text']
            if len(article)>512:
                continue

            status = 1 if (row["replyType"] == "RUMOR" ) else 0

            try:    
                addArticle(origin_id = row["articleId"],
                            article = article,
                            rumor_status = status)
            except:
                session.rollback()  
                # print("rollback")       
    except:
        #os path error
        ValueError("Problem when open csv file, or wrong path lead to fail")