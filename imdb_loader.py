soundtrack_dir = '/home/...'
movies_dir = '/home/...'
soundtrack_csv = '/home/...'
movies_csv = '/home/...'

def main():
  rating_ids = load_ratings()
  watchlist_ids = load_watchlist() 
  recommendation_ids = load_recommendations([rating_ids, watchlist_ids])   
  (ranks, top_250_ids) = load_top_250()
  
  ids = []
  ids.extend(rating_ids)
  ids.extend(watchlist_ids)
  ids.extend(recommendation_ids)
  ids.extend(top_250_ids)
  ids = list(set(ids)) # Make values distinct
  
  save_movies(ids)
  load_soundtrack(ids)
  load_lists(ids)
