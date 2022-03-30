from lda.libraries import handler
from news_fetcher import fetch_india_news
from database_saver import save_one_news, insert_tags


def handle_one_article(news_article):
    # save one news
    news_id = save_one_news(news_article)

    news_str = news_article['description']
    if news_article['content'] != 'null' or news_article['content'] != None:
        news_str += " " + str(news_article['content'])
    
    # topic Generation
    news_topic_handler = handler.Handler()
    topic_list = news_topic_handler.get_topics(news_str)[0]
    topics = []
    for topic in topic_list:
        topics.append(topic[0])
    
    if articles['category'] != null or articles['category'] != None:
        for topic in articles['category']:
            topics.append(topic)
        
    insert_tags(news_id , topics)
    
    

def handle_cycle():
    # news fetching
    news_list = fetch_india_news()
    for news_article in news_list:
        handle_one_article(news_article)


handle_cycle()