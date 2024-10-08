from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import json
import time
class ReviewsScraper:
    def __init__(self, asin) -> None:
        self.asin = asin
        self.driver = webdriver.Chrome()
        self.url = f'http://www.amazon.ca/product-reviews/{self.asin}/ref=cm_cr_dp_d_show_all_btm?ie=UTF-8&reviewerType=all_reviews&sortBy=recent&pageNumber='

    def pagination(self, page):
        self.driver.get(self.url+str(page))
        
        if not self.driver.find_elements(By.CSS_SELECTOR, 'div[data-hook=review]'):
            return False
        else:
            return self.driver.find_elements(By.CSS_SELECTOR, 'div[data-hook=review]'), self.has_next_page()
    
    def has_next_page(self):
        try:
            self.driver.find_element(By.CSS_SELECTOR, '.a-last a')
            return True
        except NoSuchElementException:
            return False
        
    def click_next_page(self):
        next_button = self.driver.find_element(By.CSS_SELECTOR, '.a-last a')
        next_button.click()

    def scrape_reviews(self):
        page=1
        all_reviews=[]
        while True:
            reviews, has_next_page = self.pagination(page)
            if reviews:
                parsed_reviews = self.parse_reviews(reviews)
                all_reviews.extend(parsed_reviews)
                #print(parsed_reviews)

            if has_next_page:
                page += 1
                time.sleep(5)
                self.click_next_page()
            else:
                break
        self.save_reviews(all_reviews)
    
    def save_reviews(self,reviews):
        with open(f'{self.asin}_data.json','w') as f:
            json.dump(reviews,f,indent=4)

    def parse_reviews(self, reviews):
        total = []
        for review in reviews:
            review_title = review.find_element(By.CSS_SELECTOR, 'a[data-hook=review-title]').text
            review_rating = review.find_element(By.CSS_SELECTOR, 'i[data-hook=review-star-rating] span').get_attribute('innerHTML')
            #review_rating=review_rating_element.get_attribute('innerText').strip if review_rating_element.text else None
            review_body = review.find_element(By.CSS_SELECTOR, 'span[data-hook=review-body] span').text.replace('\n', '').strip()

            data = {
                'review_title': review_title,
                'review_rating': review_rating,
                'review_body': review_body
            }
            print(data)
            total.append(data)
        return total
    
if __name__ == '__main__':
        aprw = ReviewsScraper("B09Z72BK8K")
    #print(reviews)
        aprw.scrape_reviews()

        aprw.driver.quit()  # Quit the WebDriver once you're done
