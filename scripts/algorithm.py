from db_connection import create_conn, query_execute, close_conn
from scipy import spatial
import numpy as np
import pandas as pd

# ===== SUGGESTION ALGORITHM =====
def user_suggestion(user_id, restaurant_id):
    cur = create_conn()
    df = query_execute(cur, "SELECT * FROM ratings")
    
    df_pivot = df.pivot_table(
        index='user_id', 
        columns='restaurant_id', 
        values='rating'
    ).fillna(0)
    
    # NOT REQUIRED -- REMOVE FOR FINAL PRODUCT
    df_pivot = df_pivot[['R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7', 'R8', 'R9', 'R10', 'R11', 'R12']]

    highest_index = 1

    # normalize selected user_id
    numpy_array_user_id = df_pivot[df_pivot.index == user_id].to_numpy()
    numpy_array_user_id_normalized = normalize(numpy_array_user_id)

    similarity_weight_array = []
    greatest = 0
    greatest_index = ''

    second_greatest = 0 
    second_greatest_index = ''

    # === CENTERED COSINE ===
    for index, row in df_pivot.iterrows():
        # parameters
        user_id = index
        numpy_array = row.to_numpy()
        
        # normalize
        numpy_array_normalized = normalize(numpy_array)

        # similarity weight
        similarity_weight = 1 - spatial.distance.cosine(numpy_array_user_id_normalized[0], numpy_array_normalized)

        if similarity_weight != 1:
            if similarity_weight > greatest:
                second_greatest = greatest
                second_greatest_index = greatest_index
                greatest = similarity_weight
                greatest_index = user_id
            elif similarity_weight > second_greatest:
                second_greatest = similarity_weight
                second_greatest_index = user_id

    greatest_rating = df_pivot.loc[greatest_index, restaurant_id]
    second_greatest_rating = df_pivot.loc[second_greatest_index, restaurant_id]

    rating = ((second_greatest_rating * second_greatest) + (greatest_rating * greatest)) / (second_greatest + greatest)

    print(rating)

# ===== HELPER FUNCTIONS =====
def normalize(numpy_array):        
    array_sum = np.sum(numpy_array)
    array_size = np.count_nonzero(numpy_array)
    row_mean = array_sum / array_size
    normalized_numpy_array = np.where(numpy_array != 0, numpy_array - row_mean, 0)
    return normalized_numpy_array
