# Anime Data Analysis Report                                                                                     
                                                                                                                   
  ## Overview                                                                                                      
  This report provides an exploratory data analysis (EDA) of the anime dataset. The dataset contains information   
  about 24,905 anime entries with various attributes such as ID, name, score, type (e.g., TV, movie), number of    
  episodes, airing date, popularity, and more.                                                                     
                                                                                                                   
  ## Score Distribution                                                                                            
  The distribution of anime scores is shown in the following plot:                                                 
  ![Score Distribution](../outputs/score_distribution.png)                                                          
                                                                                                                   
  ## Number of Animes by Type                                                                                      
  The number of animes by type is visualized in the bar plot below:                                                
  ![Anime Type Counts](../outputs/anime_type_counts.png)                                                            
                                                                                                                   
  ## Average Score by Type                                                                                         
  The average score for each anime type is shown in the bar plot below:                                            
  ![Average Score by Type](../outputs/average_score_by_type.png)                                                    
                                                                                                                   
  ## Top 10 Most Popular Animes (Filtered)                                                                         
  | Name | Popularity | Score |                                                                                    
  |------|------------|-------|                                                                                    
  {top_popular_animes[['Name', 'Popularity', 'Score']].to_markdown(index=False)}                                   
                                                                                                                   
  ## Top 10 Highest Rated Animes (Filtered)                                                                        
  | Name | Score | Popularity |                                                                                    
  |------|-------|------------|                                                                                    
  {top_rated_animes[['Name', 'Score', 'Popularity']].to_markdown(index=False)}                                     
                                                                                                                   
  ## Number of Valid Animes Released per Year                                                                      
  The trend of the number of valid animes released per year is visualized in the line plot below:                  
  ![Valid Animes Released per Year](../outputs/valid_animes_per_year.png)