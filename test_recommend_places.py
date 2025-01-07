import pytest
from unittest.mock import patch
from recommend_places import recommend_places

# Test Successful run default
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_recommend_places_default(mock_get_photo, mock_get_details, mock_get_nearby):

    # Mock return value for get_places_nearby
    mock_get_nearby.return_value = [
        {'name': 'Riverside Restaurant 1', 'rating': 4.5, 'user_ratings_total': 100, 'vicinity': '123 Riverside St', 'place_id': 'place1',},
        {'name': 'Riverside Restaurant 2', 'rating': 3.8, 'user_ratings_total': 50, 'vicinity': '456 Riverside St', 'place_id': 'place2',},
        {'name': 'Riverside Restaurant 3', 'rating': 4.0, 'user_ratings_total': 150, 'vicinity': '789 Riverside St', 'place_id': 'place3',}
    ]

    # Mock response for get_places_details
    mock_get_details.return_value = {
        'photos': [{'photo_reference': 'photo1'}],
        'opening_hours': {'open_now': True, 'weekday_text': ['Mon-Fri: 9:00 AM - 9:00 PM']},
        'reviews': [
            {'author_name': 'Alice', 'rating': 5, 'text': 'Great food!', 'relative_time_description': '1 day ago'},
            {'author_name': 'Bob', 'rating': 4, 'text': 'Good service', 'relative_time_description': '3 days ago'}
        ]
    }

    mock_get_photo.return_value = "https://example.com/photo1.jpg"

    recommended_places = recommend_places()

    print(recommended_places)
    # Assertions
    assert len(recommended_places) == 3
    assert recommended_places[0]['name'] == 'Riverside Restaurant 1'
    assert recommended_places[1]['name'] == 'Riverside Restaurant 3'
    assert recommended_places[2]['name'] == 'Riverside Restaurant 2'

    assert recommended_places[0]['rating'] == 4.5
    
    assert recommended_places[0]['place_id'] == 'place1'

    open_now = recommended_places[0].get('open_now', False)
    assert open_now is True
    assert recommended_places[0]['weekday_text'] == ['Mon-Fri: 9:00 AM - 9:00 PM']

    assert recommended_places[0]['photo_reference'] == 'https://example.com/photo1.jpg'
    assert 'review_infomation' in recommended_places[0]
    assert len(recommended_places[0]['review_infomation']) == 2


# Test Successful run input
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_recommend_places_input(mock_get_photo, mock_get_details, mock_get_nearby):

    mock_get_nearby.return_value = [
        {'name': 'Riverside Restaurant 1', 'rating': 4.5, 'user_ratings_total': 100, 'vicinity': '123 Riverside St', 'place_id': 'place1',},
        {'name': 'Riverside Restaurant 2', 'rating': 3.8, 'user_ratings_total': 50, 'vicinity': '456 Riverside St', 'place_id': 'place2',},
        {'name': 'Riverside Restaurant 3', 'rating': 4.0, 'user_ratings_total': 150, 'vicinity': '789 Riverside St', 'place_id': 'place3',},
        {'name': 'Riverside Restaurant 4', 'rating': 2.0, 'user_ratings_total': 250, 'vicinity': '111 Riverside St', 'place_id': 'place4',},
        {'name': 'Riverside Restaurant 5', 'rating': 1.7, 'user_ratings_total': 350, 'vicinity': '333 Riverside St', 'place_id': 'place5',},
        {'name': 'Riverside Restaurant 6', 'rating': 4.9, 'user_ratings_total': 350, 'vicinity': '555 Riverside St', 'place_id': 'place6',}
    ]

    mock_get_details.return_value = {
        'photos': [{'photo_reference': 'photo1'}],
        'opening_hours': {'open_now': True, 'weekday_text': ['Mon-Fri: 9:00 AM - 9:00 PM']},
        'reviews': [
            {'author_name': 'Alice', 'rating': 5, 'text': 'Great food!', 'relative_time_description': '1 day ago'},
            {'author_name': 'Bob', 'rating': 4, 'text': 'Good service', 'relative_time_description': '3 days ago'}
        ]
    }

    mock_get_photo.return_value = "https://example.com/photo1.jpg"

    recommended_places = recommend_places(number_of_recommend=4)

    assert len(recommended_places) == 4
    assert recommended_places[0]['name'] == 'Riverside Restaurant 6'
    assert recommended_places[1]['name'] == 'Riverside Restaurant 1'
    assert recommended_places[2]['name'] == 'Riverside Restaurant 3'
    assert recommended_places[3]['name'] == 'Riverside Restaurant 2'

    assert recommended_places[0]['rating'] == 4.9

    assert recommended_places[0]['place_id'] == 'place6'

    open_now = recommended_places[0].get('open_now', False)
    assert open_now is True
    assert recommended_places[0]['weekday_text'] == ['Mon-Fri: 9:00 AM - 9:00 PM']

    assert recommended_places[0]['photo_reference'] == 'https://example.com/photo1.jpg'
    assert 'review_infomation' in recommended_places[0]
    assert len(recommended_places[0]['review_infomation']) == 2

# Test low ratings < 3 eliminated
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_filter_low_rated_places(mock_get_photo, mock_get_details, mock_get_nearby):

    mock_get_nearby.return_value = [
        {'name': 'Restaurant 1', 'rating': 2.5, 'user_ratings_total': 100, 'vicinity': 'Street 1', 'place_id': 'place1'},
        {'name': 'Restaurant 2', 'rating': 4.0, 'user_ratings_total': 150, 'vicinity': 'Street 2', 'place_id': 'place2'},
        {'name': 'Restaurant 3', 'rating': 3.5, 'user_ratings_total': 80, 'vicinity': 'Street 3', 'place_id': 'place3'}
    ]

    mock_get_details.return_value = {
        'result': {
            'photos': [{'photo_reference': 'photo1'}],
            'opening_hours': {'open_now': True, 'weekday_text': ['Mon-Fri: 9:00 AM - 9:00 PM']},
            'reviews': [
                {'author_name': 'Alice', 'rating': 5, 'text': 'Great!', 'relative_time_description': '1 day ago'}
            ]
        }
    }

    mock_get_photo.return_value = "https://example.com/photo1.jpg"

    recommended_places = recommend_places(number_of_recommend=2)

    assert len(recommended_places) == 2
    assert 'Restaurant 1' not in [place['name'] for place in recommended_places]
    assert 'Restaurant 2' in [place['name'] for place in recommended_places]
    assert 'Restaurant 3' in [place['name'] for place in recommended_places]


# Test no valid places
@patch('places_API.get_places_nearby')
def test_no_valid_places(mock_get_nearby):

    mock_get_nearby.return_value = [
        {'name': 'Restaurant 1', 'rating': 2.0, 'user_ratings_total': 50, 'vicinity': 'Street 1', 'place_id': 'place1'},
        {'name': 'Restaurant 2', 'rating': 2.5, 'user_ratings_total': 30, 'vicinity': 'Street 2', 'place_id': 'place2'}
    ]

    recommended_places = recommend_places()

    assert len(recommended_places) == 0

# Test missing fields handling
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_missing_fields(mock_get_photo, mock_get_details, mock_get_nearby):
    # Mock places response with missing fields
    mock_get_nearby.return_value = [
        {'name': 'Restaurant 1', 'rating': 4.0, 'user_ratings_total': 100, 'vicinity': 'Street 1', 'place_id': 'place1'}
    ]

    # Mock details response with missing reviews and photos
    mock_get_details.return_value = {
        'opening_hours': {'open_now': False, 'weekday_text': ['Mon-Fri: 8:00 AM - 6:00 PM']},
        'reviews': []  # No reviews
    }

    mock_get_photo.return_value = None

    recommended_places = recommend_places()

    assert 'photo_reference' not in recommended_places[0]
    assert 'reviews' not in recommended_places[0]

    assert recommended_places[0]['open_now'] is False
    assert recommended_places[0]['weekday_text'] == ['Mon-Fri: 8:00 AM - 6:00 PM']

#Test no rating place
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_recommend_places_no_rating(mock_get_photo, mock_get_details, mock_get_nearby):
    mock_get_nearby.return_value = [
        {'name': 'Restaurant A', 'rating': 4.5, 'user_ratings_total': 100, 'vicinity': '123 Street', 'place_id': 'place1'},
        {'name': 'Restaurant B', 'rating': 0, 'user_ratings_total': 50, 'vicinity': '456 Street', 'place_id': 'place2'},
        {'name': 'Restaurant C', 'rating': 3.8, 'user_ratings_total': 150, 'vicinity': '789 Street', 'place_id': 'place3'}
    ]

    mock_get_details.return_value = {
        'photos': [{'photo_reference': 'photo1'}],
        'opening_hours': {'open_now': True, 'weekday_text': ['Mon-Fri: 9:00 AM - 9:00 PM']},
        'reviews': []
    }

    mock_get_photo.return_value = "https://example.com/photo1.jpg"

    recommended_places = recommend_places()

    # Assertions
    assert len(recommended_places) == 2
    assert recommended_places[0]['name'] == 'Restaurant A'
    assert recommended_places[1]['name'] == 'Restaurant C'

    assert recommended_places[1]['open_now'] == True
    assert recommended_places[0]['weekday_text'] == ['Mon-Fri: 9:00 AM - 9:00 PM']

# test number_of_recommend > or < possible places
@patch('places_API.get_places_nearby')
@patch('places_API.get_places_details')
@patch('places_API.get_photo')
def test_recommend_places_number_of_recommend(mock_get_photo, mock_get_details, mock_get_nearby):
    # Mock data for places_nearby
    mock_get_nearby.return_value = [
        {'name': 'Restaurant A', 'rating': 4.5, 'user_ratings_total': 100, 'vicinity': '123 Street', 'place_id': 'place1'},
        {'name': 'Restaurant B', 'rating': 3.8, 'user_ratings_total': 50, 'vicinity': '456 Street', 'place_id': 'place2'},
        {'name': 'Restaurant C', 'rating': 4.0, 'user_ratings_total': 150, 'vicinity': '789 Street', 'place_id': 'place3'}
    ]

    recommended_places = recommend_places(number_of_recommend=0)
    assert len(recommended_places) == 0

    recommended_places = recommend_places(number_of_recommend=5)
    assert len(recommended_places) == 3

if __name__ == "__main__":
    pytest.main()