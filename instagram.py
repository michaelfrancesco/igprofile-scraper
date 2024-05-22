import pandas as pd

# # Read links from Excel file
# excel_file = "links.xlsx"
# df = pd.read_excel(excel_file)


# links = ["https://www.instagram.com/gosballfc/", "https://www.instagram.com/gosipfootball/", "https://www.instagram.com/futboll.indonesiaa/"]

# # Function to extract bio and number of followers from a given link
# def extract_info(link):
#     try:
#         #Send request to the webpage
#         response = requests.get(link)
#         soup = BeautifulSoup(response.text, 'html.parser')

#         #Find bio and number of followers
#         bio = soup.find('meta', property='og:description')['content']
#         followers_count = soup.find('meta', property='og:rich_attachment')['content']
        
#         return bio, followers_count
#     except Exception as e:
#         print(f"Error processing {link}: {e}")
#         return None, None

# # Iterate over links and extract information
# results = []
# extract_info("https://www.instagram.com/gosballfc/")

# start = '"edge_followed_by":{"count":'
# end = '},"followed_by_viewer"'
# followers= r[r.find(start)+len(start):r.rfind(end)]

# for index, row in df.iterrows():
#     link = row['Link']
#     bio, followers_count = extract_info(link)
#     results.append({'Link': link, 'Bio': bio, 'Followers': followers_count})

# for link in links:
#     bio, followers_count = extract_info(link)
#     print(bio, ", " ,followers_count)
#     results.append({'Link': link, 'Bio': bio, 'Followers': followers_count})



# # Create a DataFrame from the results
# result_df = pd.DataFrame(results)

# # Write the result to a new Excel file
# result_df.to_excel("extracted_info.xlsx", index=False)



# importing libraries
from bs4 import BeautifulSoup
import requests
import re
 
# instagram URL
URL = "https://www.instagram.com/{}/"
 
# parse function
def parse_data(s):
    # creating a dictionary
    data = {}
    # splitting the content 
    # then taking the first part
    s = s.split("-")[0]
    # again splitting the content 
    s = s.split(" ")
    # assigning the values
    data['Followers'] = s[0]
    data['Following'] = s[2]
    data['Posts'] = s[4]
     
    # returning the dictionary
    return data
 
def remove_suffix(s):
    return re.sub(r'[MK]$', '', s)

def formating(data):
    # Follower 
    follower_count = data['Followers']
    last_character = follower_count[-1:]
    last_character = last_character.strip()
    follower_count = remove_suffix(follower_count)
    
    if last_character == "M" or last_character == "m"  :
        output_string_follower = f"{follower_count}.000.000"

    elif last_character == "K" or last_character == "k"  :
        output_string_follower = f"{follower_count}.000"
    else : 
        output_string_follower = follower_count

    # Following
    following_count = data['Following']
    last_character = following_count[-1:]
    last_character = last_character.strip()
    following_count = remove_suffix(following_count)

    if last_character == "M" or last_character == "m"  :
        output_string_following = f"{following_count}.000.000"
    elif last_character == "K" or last_character == "k"  :
       output_string_following = f"{following_count}.000"
    else : 
        output_string_following = following_count

    # Post
    post_count = data['Posts']
    last_character = post_count[-1:]
    last_character = last_character.strip()
    post_count = remove_suffix(post_count)

    if last_character == "M" or last_character == "m"  :
        output_string_post = f"{post_count}.000.000"

    elif last_character == "K" or last_character == "k"  :
        output_string_post = f"{post_count}.000"
    else : 
        output_string_post = post_count

    return("follower: " + output_string_follower, "following: " + output_string_following, "post: " +output_string_post)

def scrape_data(username):
     
    # getting the request from url
    r = requests.get(URL.format(username))
    # converting the text
    s = BeautifulSoup(r.text, "html.parser")
    # finding meta info
    meta = s.find("meta", property ="og:description")
    # calling parse method
    return parse_data(meta.attrs['content'])

def scrape_instagram_links(profile_link):
    try:
        # Send a GET request to the Instagram profile link
        response = requests.get(profile_link)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all anchor elements (links) inside the profile section
        profile_section = soup.find('section', class_='zwlfE')
        if profile_section:
            links = profile_section.find_all('a', href=True)

            # Extract the href attribute from each link
            link_list = [link['href'] for link in links]
            return link_list
        else:
            print("Profile section not found")
            return None
    except Exception as e:
        print(f"Error scraping Instagram links: {e}")
        return None

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions

def get_instagram_bio_link(username):
    url = f"https://www.instagram.com/{username}/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            print("soup", soup)
            bio_link_element = soup.find('a', attrs={'href': True, 'rel': 'me nofollow noopener noreferrer'})
            print("Biolinkelement", bio_link_element)
            if bio_link_element:
                return bio_link_element['href']
            else:
                return "Bio link not found"
        else:
            return f"Failed to fetch Instagram profile. Status code: {response.status_code}"
    except Exception as e:
        return f"Error occurred: {str(e)}"


# main function
if __name__=="__main__":

    # Example usage
    profile_link = "https://www.instagram.com/wkwkbol/"
    links = scrape_instagram_links(profile_link)
    if links:
        print("Instagram Links:")
        for link in links:
            print(link)


    # user name
    username = "wkwkbol"
    # calling scrape function
    data = scrape_data(username)
    data = formating(data)
    # printing the info
    bio_link = get_instagram_bio_link(username)
    print(bio_link)
