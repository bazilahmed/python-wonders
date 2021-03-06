# program to do web scraping and store the output as a csv file

from datetime import datetime
from time import sleep
from bs4 import BeautifulSoup
# import logging
import requests
import pandas as pd
import random

# create a log file
# add the log file code here later
today = datetime.now().date()

# define the iteration count in terms of page results based on the sample url
results_numbers = list(range(10, 1001, 10))

# add 0 as the first element in the list to go through the search results of the first page
results_numbers.insert(0, 0)

# create a list to save the number of records retrieved in each iteration
job_results_counts = []

# create empty dataframe
columns = ['Title', 'Summary', 'Company', 'Location', 'Salary']
job_results_df = pd.DataFrame(columns=columns)

# create a session and get the response for the url
s = requests.Session()
s.headers = {'User Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15'}
# sample url for 2nd page results "https://www.indeed.com/jobs?q=data+analyst&start=10"
# first_page = "https://www.indeed.com/jobs?q=data+scientist&start=0"
base_url = "https://www.indeed.com/jobs?q=statistician&start="

# print some messages on the screen
print("\n---------------------------------------------------------------------------------")
print("Welcome to the future of web scraping! Let's get started!\n")
print("---------------------------------------------------------------------------------")

# iterate through pages to get the response, parse it, create a dataframe and save the output
for result_no in results_numbers:
    # building the url to navigate through the pages
    url = f"{base_url}{result_no}"
    iteration = int(result_no / 10) + 1
    print(f"Iteration {iteration} started..")

    # get the response
    try:
        r = s.get(url)
        print(f"Connection Successful! Status code: {r.status_code}")
    except ConnectionError:
        print(f"Connection failed in getting page {iteration} results. Please try again later")

    # retrieve the content and save to a text file
    soup = BeautifulSoup(r.content, "html.parser")

    # commenting the text file section temporarily
    # text_file = f"page_results_{iteration}_{today}.txt"
    # with open(text_file, 'w') as file_object:
    #     file_object.write(f"{soup.prettify()}")
    # print("Page downloaded and saved as html text\n")

    # number of records retrieved
    job_results = soup.find_all('div', class_='jobsearch-SerpJobCard row result')
    job_results_counts.append(len(job_results))
    print(f"Iteration {iteration} retrieved {len(job_results)} records")

    # retrieve the job title
    titles = []
    for row in job_results:
        try:
            job_title = row.find('a', class_="jobtitle turnstileLink").text.strip()
            titles.append(job_title)
        except AttributeError:
            try:
                job_title = row.find('a', class_="turnstileLink").text.strip()
                titles.append(job_title)
            except AttributeError:
                titles.append("Not available")

    # retrieve the job summary
    summaries = []
    for row in job_results:
        try:
            summary = row.find('div', class_="paddedSummary").text.strip()
            summaries.append(summary)
        except AttributeError:
            summaries.append("Not available")

    # retrieve the company
    companies = []
    for row in job_results:
        try:
            company = row.find("span", class_="company").text.strip()
            companies.append(company)
        except AttributeError:
            companies.append("Not available")

    # retrive salary if provided
    salaries = []
    for row in job_results:
        try:
            salary = row.find("span", class_="salary no-wrap").text.strip()
            salaries.append(salary)
        except AttributeError:
            salaries.append("Not available")

    # retrieve the location
    locations = []
    for row in job_results:
        try:
            location = row.find("div", class_="location").text.strip()
            locations.append(location)
        except AttributeError:
            try:
                location = row.find("span", class_="location").text.strip()
                locations.append(location)
            except AttributeError:
                locations.append("Not available")

    # create a dataframe and output to csv
    # check if the lenght of all lists are same only then add it to dataframe
    if len(titles) == len(summaries) and \
            len(summaries) == len(companies) and \
            len(companies) == len(locations) and \
            len(locations) == len(salaries):

        iteration_results_df = pd.DataFrame({'Title': titles,
                                             'Summary': summaries,
                                             'Company': companies,
                                             'Location': locations,
                                             'Salary': salaries})
        # rearranging columns
        iteration_results_df = iteration_results_df[['Title', 'Summary', 'Company', 'Location', 'Salary']]

        # append to the original df
        job_results_df = job_results_df.append(iteration_results_df, ignore_index=True)
        print(f"Results of iteration {iteration} succesfully appended.\n")

    else:
        print(f"Counts mismatched for retrieved records in iteration {iteration}.\nCanceling the loop.\n")
        break

    # sleep for each iterative call
    sleeptime = random.randint(4, 8)

    # sleep before trying again
    print(f"Sleeping for {sleeptime} seconds... Zzzzzzz...")
    sleep(sleeptime)
    print("Awake now! Let's continue working.. \n")

# save to csv
output_file = f"Indeed_job_results_{today}.csv"
job_results_df.to_csv(output_file, index=False)

print("---------------------------------------------------------------------------------")
print(f"\n\nCongratulation!!!\nSuccesfully retrived {sum(job_results_counts)} results.\n")
print(f"Results are saved to {output_file}\nHave a nice day. :)")
print("---------------------------------------------------------------------------------")

# next changes --
# run the results of the first page
# take user input for the type of job results he/she needs
# create a log file
# create __main__ function
