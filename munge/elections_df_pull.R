library(tidyverse)
library(lubridate)
library(rvest)
library(countrycode)

# get site links ---------------------------------------------------------------
page <- xml2::read_html("https://www.electionguide.org/sitemap-election.xml")

pages <- page %>% 
  html_nodes("loc") %>% 
  html_text()

# get data ---------------------------------------------------------------------
election_df <- tibble()
i <- 1

for (link in pages) {
  
  data <- xml2::read_html(link) 
  
  date <- data %>% 
    html_node("h3 span") %>% 
    html_text()
  
  country <- data %>% 
    html_node("h3 a") %>% 
    html_text()
  
  election <- data %>% 
    html_node("div h5") %>% 
    html_text() %>% 
    stringr::str_trim()
  
  status <- data %>% 
    html_node("h3 em") %>% 
    html_text() %>% 
    stringr::str_trim()
  
  df <- tibble(date, country, election, status)
  
  election_df <- election_df %>% bind_rows(df) 
  
  print(paste(country, ": completed", i, "of", length(pages)))
  
  i <- i + 1
  
}

LDI <- today()

# clean data -------------------------------------------------------------------
clean_df <- election_df %>% 
  mutate(iso_3c = countrycode(country, origin = "country.name", destination = "iso3c", 
                              custom_match = c("Italian Republic" = "ITA",
                                               "Lebanese Republic" = "LBN",
                                               "Northern Ireland" = "GBR",
                                               "Scotland" = "GBR",
                                               "Wales" = "GBR",
                                               "Portuguese Republic" = "PRT",
                                               "Republic of Bostwana" = "BWA",
                                               "Serbia and Montenegro" = "SRB")),
         date = str_remove_all(date, "\\."),
         date = str_replace_all(date, "Sept", "Sep"),
         date = as_date(date, format = "%b %d, %Y"))

# save data --------------------------------------------------------------------
election_df %>% write_csv("election_df.csv")
