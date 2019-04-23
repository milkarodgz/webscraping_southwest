from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re


driver= webdriver.Chrome()

driver.get('https://www.tripadvisor.com/Airline_Review-d8729156-Reviews-Southwest-Airlines')

airline_rating =  driver.find_element_by_xpath('//span[@class="flights-airline-review-page-overview-module-OverviewModule__review_num--2Ga7T"]').text
csv_file = open('swreviews.csv', 'w', encoding= 'utf-8', newline='')
writer= csv.writer(csv_file)



index=1


while True:
    
    print("Scraping Page number "+ str(index))
    index=index+1

    
    read_more = WebDriverWait(driver,10)
    read_more = read_more.until(EC.presence_of_element_located((By.XPATH,'//span[@class="location-review-review-list-parts-ExpandableReview__cta--2mR2g"]')))
    read_more.click()

   

    
    swreviews = driver.find_elements_by_xpath('//div[@class="location-review-card-Card__ui_card--2Mri0 location-review-card-Card__card--o3LVm location-review-card-Card__section--NiAcw"]')
    
    for swreview in swreviews:
        
        review_dict={}
        try:
            
            title = swreview.find_element_by_xpath('.//a[@class="location-review-review-list-parts-ReviewTitle__reviewTitleText--2tFRT"]/span/span').text
        except:
            
            print("Could not find title for review on page {}".format(index))
            continue

        text= swreview.find_element_by_xpath('.//div[@class="common-text-ReadMore__content--2X4LR"]').text

        username=swreview.find_element_by_xpath('.//a[@class="ui_header_link social-member-event-MemberEventOnObjectBlock__member--35-jC"]').text

        
        rating=swreview.find_element_by_xpath('.//div[@class="location-review-review-list-parts-RatingLine__bubbles--GcJvM"]/span').get_attribute('class')
     
        rating= int(re.search('.+(\d{2})$', rating).group(1))/10
        
        review_dict['title']= title
        review_dict['text']= text
        review_dict['username']= username
        
        review_dict['rating']= rating
       
        
        
        writer.writerow(review_dict.values())
        print(review_dict)
    
    try:

    
        next_button = driver.find_element_by_xpath('//a[@class="ui_button nav next primary "]')
        next_button.click()
    except: print('no more reviews')

csv_file.close()
driver.close()


