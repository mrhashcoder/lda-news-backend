""" Module for reading in, saving and analyzing NYTimes article data.

"""

# System dependencies
import datetime
import json
import os
import requests

# Standard
import pandas as pd
import numpy as np

from lda.libraries import configs
from lda.libraries import text_processing

MIN_OCCURANCES = 5
MIN_PERCENT = .4
NUM_WDS_PER_CAT = 15


def get_nytimes_topic_words(get_new_data=False):
    """
        Main function to get the NYTimes topic seed words.
        Args:
            get_new_data: boolean flag for whether to pull new NYTimes data.
        Returns:
            topic_seeds: A list of lists with topic seed words.
            The first item of each list is the topic name.
    """
    if get_new_data:
        data = get_nytimes_data('all')
        data = aggregate_data()
        topic_seeds = get_section_words(data)
        with open('news_analyzer/resources/nytimes_data/' +
                  'aggregated_seed_words.txt',
                  'w') as open_file:
            open_file.write(json.dumps(topic_seeds))
    else:
        with open('news_analyzer/resources/nytimes_data/' +
                  'aggregated_seed_words.txt',
                  'r') as open_file:
            topic_seeds = json.loads(open_file.read())
    return topic_seeds


def aggregate_data():
    """
        Helper function that aggregates the daily data into one list of lists
        by concatenating contents of all equivalent categories together.

        Args:
            None
        Returns:
            Data: a list of lists. The contents of all queries aggregated
            by category
    """
    directory = 'news_analyzer/resources/nytimes_data/'
    data = pd.DataFrame(np.asarray(['business', '']).reshape(-1, 2))
    for file in os.listdir(directory):
        if file.startswith('NYtimes_'):
            datai = pd.read_csv(directory+file).iloc[:, 1:]
            for i in range(len(datai)):
                if datai.iloc[i, 0] in configs.GUIDED_LDA_TOPICS:
                    if datai.iloc[i, 0] in list(data.iloc[:, 0]):
                        loc = list(data.iloc[:, 0]).index(datai.iloc[i, 0])
                        old_string = str(data.iloc[loc, 1])
                        new_string = str(datai.iloc[i, 1])
                        data.iloc[loc, 1] = old_string + new_string
                    else:
                        data = data.append(
                            pd.DataFrame(
                                np.asarray([datai.iloc[i, 0],
                                            datai.iloc[i, 1]]).reshape(-1, 2)))
    return data


def get_nytimes_data(sections='all'):
    """
        Helper function for retrieving articles from the NYTimes by section.
        Args:
        sections: An array of sections from NYTimes to pull.

        Returns:
        NYTimesData: A pandas dataframe with section names and all the section
        content as a string.
    """
    if sections == 'all':
        sections = configs.GUIDED_LDA_TOPICS

    nytimes_data = []
    for section in sections:
        url = ('http://api.nytimes.com/svc/topstories/v2/' + section +
               '.json?api-key=65daae448b694b07a1dca7feb0322778')
        # 65daae448b694b07a1dca7feb0322778
        # 2f87e82d4d404f3888ba7b17aff3bd94
        url_content = requests.get(url).content
        try:
            temp_data = pd.read_json(url_content)
        except ValueError:
            # Failed to import new data.
            empty_df = pd.DataFrame(np.asarray([]).reshape(-1, 2))
            return empty_df
        except:
            # Failed to import new data.
            empty_df = pd.DataFrame(np.asarray([]).reshape(-1, 2))
            return empty_df
        temp_data = pd.read_json(url_content)
        article_content = ""
        # merge articles together
        for i in range(len(np.asarray(temp_data.results))):
            new_content = str(np.asarray(temp_data.results)[i])
            article_content = article_content + new_content

        nytimes_data.append([section, article_content])

    nytimes_data = pd.DataFrame(np.asarray(nytimes_data))
    # save the dataframe so it can be used to create aggregated seed words
    nytimes_data.to_csv("news_analyzer/resources/nytimes_data/NYtimes_data_" +
                        datetime.datetime.now().strftime("%Y%m%d") +
                        ".csv")
    return nytimes_data


def get_section_words(data):
    """
        Helper function for identifying top topic words for each category.
        Args:
        data: A pandas dataframe with section names and all the section
            content as a string.

        Returns:
        topic_seeds: A list of lists with top topics for each of the inputted
            sections.
    """
    data = pd.DataFrame(np.asarray(data))
    if data.shape[0] <= 2:
        return list()

    processor = text_processing.ArticlePreprocessor(min_df=0)
    article_dtm = processor.get_dtm(series_of_articles=data.iloc[:, 1])

    topic_seeds = []
    dtm_normalized = article_dtm**2 / np.sum(article_dtm, axis=0)

    for i in range(len(dtm_normalized)):
        min_apps = (dtm_normalized.loc[i, :] >= MIN_OCCURANCES)
        min_probability = ((dtm_normalized.loc[i, :] /
                            np.sum(dtm_normalized, axis=0)) > MIN_PERCENT)
        words = dtm_normalized.loc[i, min_apps & min_probability]
        words = words.sort_values(ascending=False)
        category_name = list([data.loc[i, 0]])
        top_words = list(words.reset_index().iloc[:, 0])[0:NUM_WDS_PER_CAT]
        if category_name[0] in top_words:
            top_words.remove(category_name[0])
        topic_seeds.append((category_name + top_words))
    return topic_seeds
