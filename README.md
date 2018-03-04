# vocabModel

Exploratory Data Collection and Analysis: Predicting Rapper Vocabulary Size from Sample Vocabulary, Region, and Age

Question: Can you predict a rapper's vocabulary size from their age and regional location?

[lyrics.py](https://github.com/bogedy/vocabModel/blob/master/lyrics.py): scarping code

[model.R](https://github.com/bogedy/vocabModel/blob/master/model.R): R script for analysis of the data csv

[RapSheet.csv](https://github.com/bogedy/vocabModel/blob/master/RapSheet.csv): collected data in a csv

[corpus.py](https://github.com/bogedy/vocabModel/blob/master/corpus.py): (very long) strings of song titles used by region. at the end of each region is the code used in [lyrics.py](https://github.com/bogedy/vocabModel/blob/master/lyrics.py)

A while ago I saw this cool experiment exploring who has the largest vocabulary in hip hop. After taking statistics this semester, I wanted to see if rappers from one coast had a statistically larger vocabulary than the other coast. I manually wrote the vocabulary values into a spreadsheet, loaded it into R, and found no statistical difference (without p-hacking and data dredging, that is). The sample size was pretty small, so I went about seeing how I could collect more data. These are the results.

The first issue is using an API to collect lyrics. Genius.com pays royalties on their lyrics and does not make them accessible through their API. This method uses the API to find the URL for a given song, and then uses BeautifulSoup to scrape the page for the lyrics. My code came from this blog post, where you can see the code in its original form.

The code works by searching genius.com for a song title, and then seeing if any of the results match the input artist name. Originally, if nothing matched, an error was returned. I edited the code to look for matches without case sensitivity, or for either of the strings including the other one. For example, rapper Freddie Gibbs works with producer Madlib on the album Piñata. Freddie does all of the rapping, while Madlib makes the beat. This is good material for Gibbs' lyric analysis, but the songs on Piñata are listed under "Freddie Gibbs and Madlib". Originally, scraping Gibb's lyrics returned an error, but after my edit for inclusion it worked fine.

Below the main body of code are two functions I define: list(s) and vocab(d). The best website I found for copying down song titles was azlyrics.com. The list format on that website made it simple to copy and paste a string list of song titles. The song list document shows the result of this, and there is an example included for Kendrick Lamar in the code. list(s) takes the string and converts it into a python list. vocab(d) then takes that list and plugs the song titles and artist names into the lyrics scraper function.

I originally wanted to randomly select rappers but ran into several issues. The API calls rely on the genius.com search function, which won't be very useful for small obscure artists who are too deep in the search results. Additionally, even among artists I am familiar with, issues surrounding authorship, featuring artists, and naming were already hard enough to figure out. I ended up trying to keep it simple with material familiar to me.

The original experiment that I was inspired by was answering a different question: How big is everyone's vocabulary? My question was can we predict vocabulary size. As such, the original experiment caps each sample size at 35,000 words. My experiment fits a linear regression model for predicting vocabulary size, and takes sample size as a parameter, therefore allowing for variability in the sample size. Each sample is whatever I deemed to be some of the rapper's most acclaimed works, excluding anything I knew to be heavy in features from other artists or otherwise unfit. I generally thought: The more the merrier, as long as I'm not doing too much copy and paste busy work.

I used R to fit a model for predicting vocabulary size from region, age, and sample size (as a blocker against bias). Here are the results:
```
  Coefficients:
                    Estimate Std. Error t value Pr(>|t|)    
  (Intercept)      2.353e+03  2.878e+02   8.177 1.03e-10 ***
  locationMidwest -4.202e+02  2.468e+02  -1.703   0.0949 .  
  locationSouth   -4.741e+02  2.482e+02  -1.910   0.0620 .  
  locationWest    -5.494e+02  2.340e+02  -2.348   0.0230 *  
  decade2         -1.066e+02  2.734e+02  -0.390   0.6982    
  decade3         -1.822e+02  2.961e+02  -0.615   0.5412    
  decade4         -3.467e+02  3.627e+02  -0.956   0.3439    
  samplesize       7.741e-02  6.614e-03  11.703 8.45e-16 ***
  ---
  Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```
There is little evidence in my dataset that decade of birth is an indicator of vocabulary size. Regional location, however seems promising. I refit a model to exclude decade of birth as a predictor:


```
Coefficients:
                  Estimate Std. Error t value Pr(>|t|)    
(Intercept)      2.249e+03  2.397e+02   9.380 9.05e-13 ***
locationMidwest -4.691e+02  2.311e+02  -2.030   0.0475 *  
locationSouth   -5.018e+02  2.299e+02  -2.182   0.0336 *  
locationWest    -5.986e+02  2.240e+02  -2.673   0.0100 *  
samplesize       7.746e-02  6.364e-03  12.173  < 2e-16 ***
---
Signif. codes:  0 '***' 0.001 '**' 0.01 '*' 0.05 '.' 0.1 ' ' 1
```

Now in this model region is an even stronger predictor of vocabulary size. These p-values are smaller.

The R2 value shows the percentage of variability in the data that is explained by the model. My reduced model has an adjusted R2 value of 0.7281. This is up from 0.7176 in the first model.

When performing an F test for the reduced model v.s. full one, I got a p-value of 0.7889, showing that I cannot reject the null, that the reduced model account for a higher percentage of the variability explained by the model. 

So what does this data say? The left columns are coefficients for the categorical variables of region, which take values 1 or 0. So the model predicts vocab size by multiplying the sample size by its coefficient (the last one in the table), and then adding the region coefficient (the east region coefficient is just the lack of other coefficients). While the coefficients are pretty small (only about 469-598 out of vocab sizes of several thousand), there is pretty clear evidence of the East Coast having the largest vocabulary, then the Midwest, then the South, then the West Coast.

The assumptions for linear regression are that the residuals (difference between the model and the data) for the model are normally distributed around mean 0. Graphs of these show that the assumptiosn were met.


Areas for improvement:

I ended up doing a lot of busy work for this project. I repeatedly searched google for lyrics by artists and then manually copied and pasted lists of songs into a document. With a little more know how, I could write a program to scrape the lyrics website for the song titles. This would also enable me to collect more data on more songs from more artists.
There are all kinds of errors that get lumped into the results. Some of the songs are simple words like "Intro", which are among many results. For some songs there were empty string returns. If a song had the same title as the album, maybe instead of returning the song lyrics it returned the tracklisting for a an album (which I suppose is alright, a list of song titles is still writing from the artist).
I originally wanted to control for type of album. In rap, there are mixtapes and albums. Mixtapes are sometimes released for free and allow artists for greater creative freedom. Albums are mass marketed and sometimes have label restrictions put on them. This can influence the lyrical content. I found it too hard to control for this, as some artists only have mixtapes or a mix of both. I wanted to have a variable for percentage of releases that are mixtapes, I know of no resource that have a reliable report of this information.

As noted: The scraping code is based on this blog post https://bigishdata.com/2016/09/27/getting-song-lyrics-from-geniuss-api-scraping/. I edited it.
