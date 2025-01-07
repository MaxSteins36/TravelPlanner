import places_API

def recommend_places(location="33.9720577784,-117.325408698", radius=16000, place_type = "restaurant", number_of_recommend = 3):
	places = places_API.get_places_nearby(location, radius, place_type)

#Filter out places based on min_rating
	recommended_places = []
	for place in places:
		rating = place.get('rating', 0)
		total_reviews = place.get('user_ratings_total', 0)
		if rating >= 3:
			place_info = {
				'name': place.get('name'),
                'rating': rating,
				'total_reviews': total_reviews,
                'address': place.get('vicinity'),
				'place_id': place.get('place_id'),
			}
			
			recommended_places.append(place_info)

	top_places_ratings = sorted(recommended_places, key = lambda k: k['rating'], reverse = True)
	top_places = top_places_ratings[:number_of_recommend]

	for place in top_places:
		if 'place_id' in place:
			detail_data = places_API.get_places_details(place['place_id'])
			if 'photos' in detail_data:
				photo = detail_data.get('photos', [])
				photo_reference = places_API.get_photo(photo[0]['photo_reference'],400)
				place['photo_reference'] = photo_reference
				
			if 'opening_hours' in detail_data: 
				open_hour = detail_data.get('opening_hours', {})
				if open_hour:
					place['open_now'] = open_hour.get('open_now', 'N/A')
					place['weekday_text'] = open_hour.get('weekday_text', [])

			if 'reviews' in detail_data:
				reviews = detail_data.get('reviews', [])
				review_informations = []
				for review in reviews:
					review_rating = review.get('rating')
					if review_rating >= 4:
						review_informations.append({
							'author_name': review.get('author_name'),
							'rating': review_rating,
							'text': review.get('text'),
							'relative_time': review.get('relative_time_description'),
						})
				review_informations = sorted(review_informations, key = lambda k: k['rating'], reverse = True)
				place['review_infomation'] = review_informations
	return top_places

##Testing base
if __name__ == '__main__':
	recommendations = recommend_places()

	for place in recommendations:
		print(f"   {place['name']} \n- Rating: {place['rating']} : {place['total_reviews']} reviews \n- Address: {place['address']} \n- ID: {place['place_id']} \n- Photo_ref: {place['photo_reference']} \n")

		if 'open_now' in place and place['open_now']:
			print("Open now")
		else:
			print("Closed now")

		if 'weekday_text' in place and place['weekday_text']:
			for hour in place['weekday_text']: print(f"  {hour}")
		else:
			print("  No opening hours available")

		if 'review_infomation' in place and place['review_infomation']:
			for review in place['review_infomation']:
				print(f"- {review['author_name']} \n- Rating: {review['rating']} \n- Comment: {review['text']} \n- Time: {review['relative_time']} \n")
		else:
			print("  No reviews available \n")
