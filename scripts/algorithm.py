from db_connection import create_conn, query_execute, close_conn
from scipy import spatial
import numpy as np
import pandas as pd
import pprint as pp

# ===== SUGGESTION ALGORITHM =====
def user_suggestion(user_id, criteria):
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
    
    greatest = 0
    greatest_index = ''

    second_greatest = 0 
    second_greatest_index = ''

    # ===== COSINE SIMILARITY =====
    for index, row in df_pivot.iterrows():
        # parameters
        user_id_iter = index
        numpy_array = row.to_numpy()
        
        # normalize
        numpy_array_normalized = normalize(numpy_array)

        # similarity weight
        similarity_weight = 1 - spatial.distance.cosine(numpy_array_user_id_normalized[0], numpy_array_normalized)

        if similarity_weight != 1:
            if similarity_weight > greatest:
                # transfer current greatest => second greatest
                second_greatest = greatest
                second_greatest_index = greatest_index
                # update current greatest
                greatest = similarity_weight
                greatest_index = user_id_iter
            elif similarity_weight > second_greatest:
                # update second greatest
                second_greatest = similarity_weight
                second_greatest_index = user_id_iter

    # TESTING
    print('\n')
    print('==== COSINE SIMILARITY =====')
    print('Greatest Similarity to: ' + greatest_index)
    print('Second greatest Similarity to: ' + second_greatest_index)

    # ===== ESTIMATING MISSING RESTAURANTS =====
    current_user = df_pivot[df_pivot.index == user_id]

    column_tracked = current_user == 0
    column_tracked.reset_index(inplace=True)

    column_tracked_melt = column_tracked.melt(
        id_vars = 'user_id',
        var_name = 'columns',
        value_name = 'values'
    )

    parsed_columns_df = column_tracked_melt.loc[column_tracked_melt['values'] == True, ['columns']]
    parsed_columns_array = parsed_columns_df.squeeze().tolist()

    estimated_array = []

    # TESTING
    print('Estimated Ratings:')

    for column in parsed_columns_array:
        greatest_rating = df_pivot.loc[greatest_index, column]
        second_greatest_rating = df_pivot.loc[second_greatest_index, column]
        
        rating = ((second_greatest_rating * second_greatest) + (greatest_rating * greatest)) / (second_greatest + greatest)
        
        item = {
            'restaurant': column,
            'estimated_rating': rating
        }

        estimated_array.append(item)

        # TESTING
        print(f'Ratings for {column}: ' + str(rating))

    print('\n')
    # ===== POLL FILTERING =====
    print("===== POLL FILTERING =====")

    df = query_execute(cur, f'''SELECT * 
                                FROM restaurants
                                WHERE 
                                delivery = {criteria['delivery']} AND
                                dine_in = {criteria['dine_in']} AND
                                reservable = {criteria['reservable']};''')
    
    valid_restaurants = df[['restaurant_id']].to_numpy().squeeze().tolist()

    print('Valid restraunts to criteria:' + str(valid_restaurants))

    final_set_restaurants = []

    for estimated_rating in estimated_array:
        if estimated_rating['restaurant'] in valid_restaurants:
            final_set_restaurants.append(estimated_rating)

    print('Final Valid Restaurants' + str(final_set_restaurants))

    

# ===== HELPER FUNCTIONS =====
def normalize(numpy_array):        
    array_sum = np.sum(numpy_array)
    array_size = np.count_nonzero(numpy_array)
    row_mean = array_sum / array_size
    normalized_numpy_array = np.where(numpy_array != 0, numpy_array - row_mean, 0)
    return normalized_numpy_array
