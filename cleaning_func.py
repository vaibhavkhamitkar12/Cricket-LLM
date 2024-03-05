
def update_city_based_on_venue(df, venue_to_city):
  """
  This function replaces 'NA' values in the 'City' column of a DataFrame
  with corresponding city names based on the 'Venue' column using a dictionary.

  Args:
      df (pandas.DataFrame): The DataFrame to modify.
      venue_to_city (dict): A dictionary mapping venue names to city names.

  Returns:
      pandas.DataFrame: The modified DataFrame.
  """
  df['City'] = df['Venue'].apply(lambda x: venue_to_city.get(x, 'NA') if x != 'NA' else x)
  return df
# Define a dictionary mapping venue names to city names
venue_to_city = {
    "Dubai International Cricket Stadium": "Dubai",
    "Sharjah Cricket Stadium": "Sharjah"
}


#Vaibhav update 
def bat_over_type(x):
    if x <= 5:
        return "PowerPlay"
    elif x >= 16:
        return "DeathOver"
data["over_type"] = data['overs'].apply(bat_over_type)

#update
#Vaibhav update 
def chase_defend(x):
    if x == "Wickets":
        return "Chasing"
    elif x == "Runs":
        return "Defending"
data["chase_or_defend"] = data['WonBy'].apply(chase_defend)

#update
def no_match_results():
  if x == "NoResults":
    


