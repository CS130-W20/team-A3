"""
interests.py
====================
Provide interest list for frontend
"""
import numpy as np
import pandas as pd
import pickle

interests_list = [["Topic", "Machine Learning", "Data Mining & Analysis",
                    "Deep Learning", "Big Data", "Databases"]]

def get_interests_options():
    return interests_list

def get_ohe_concepts(interests, concepts):
    # get list of concepts
    with open('database/course_contains_concepts/course_concepts_df.pkl', 'rb') as f:
        cols = np.array(pickle.load(f).columns)

    interests_ohe = [0]*len(cols)
    concepts_ohe  = [0]*len(cols)

    interest_concepts = []
    for interest in interests:
        if interest == "Machine Learning":
            interest_concepts += ["machine learning", "regression model",
            "artificial intelligence", "logistic regression","decision tree"]
        elif interest == "Deep Learning":
            interest_concepts += ["deep learning", "deep neural network",
            "reinforcement learning", "natural language processing",
            "computer vision"]
        elif interest == "Data Mining & Analysis":
            interest_concepts += ["data analysis", "data visualization",
            "statistical model", "regression analysis", "linear regression model",
            "data mining", "statistical inference"]
        elif interest == "Big Data":
            interest_concepts += ["big data", "hadoop", "cloud computing"]
        elif interest == "Databases":
            interest_concepts += ["database", "mysql", "datalog", "data management"]
        elif interest == "Other":
            interest_concepts += ["programming", "algorithm", "system programming",
            "graphics", "biostatistics"]

    for interest in interest_concepts:
        concept_idx = np.where(cols == interest.lower())[0][0]
        interests_ohe[concept_idx] = 1

    for concept in concepts:
        concept_idx = np.where(cols == concept.lower())[0][0]
        concepts_ohe[concept_idx] = 1

    return [interests_ohe, concepts_ohe]
