import re
import requests
from datetime import date
from datetime import datetime, timedelta
import os
import requests
import pymongo
from bson.objectid import ObjectId
import logging
import urllib, urllib.request, urllib.parse
import time
import random

# project_path = '/var/www/html/api/client_process/bing_news'
project_path = r'C:\Users\Admin\Desktop\kanalytics-work\scripts'

# MongoDb Connection
mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
dashboard = mongo_client["dashboard"]
cl_data = dashboard['core_w']


def log_func(log_path, created_on, current_time):
    # Create and configure logger 
    logging.basicConfig(filename=rf"{log_path}/{created_on}_{current_time}.log", format='%(asctime)s %(process)d %(message)s', filemode='w') 
    logger=logging.getLogger() 
    logger.setLevel(logging.INFO) 
    return logger


class Crawl:
    
    created_on = date.today().strftime("%Y-%m-%d")
    current_time = datetime.now().strftime("%H_%M_%S")
    headers = {
                'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36'
        }
    
    
    def scrap(self, regex, data):
        
        self.regex = regex
        self.data = data
        
        elem = re.search(self.regex, str(self.data), re.S)
        if elem: 
            elem = elem.group(1)
            return elem.strip()
        return ''
    
    
    def scrap_html(self, regex, data):
        
        self.regex = regex
        self.data = data
        
        elem = re.search(self.regex, str(self.data), re.S)
        if elem: 
            elem = elem.group(0)
            elem = re.sub(r'\n\s*\n', '\n'*2, elem).strip()
            return elem
        return ''


    def strip_html(self, text):
        
        self.text = text
        
        if self.text: 
            self.text = re.sub(r'<!--.*?-->','', self.text, flags = re.S)
            self.text = re.sub('<script.*?>.*?</script>','', self.text, flags = re.S)
            self.text = re.sub('<style.*?>.*?</style>','', self.text, flags = re.S)
            self.text = re.sub('<.*?>|&nbsp;', "", self.text, flags = re.S)
            self.text = re.sub(r'\n\s*\n', '\n'*2, self.text).strip()
            return self.text
        return ''
    
    
    # create directory if it does not exists and return the path
    def create_directory(self, path):
        self.path = path
        if not os.path.exists(self.path):os.mkdir(self.path) 
        return self.path
    
    
    def create_directories(self, project_path, client_id, site):
        
        self.project_path = project_path
        self.client_id = client_id
        self.site = site
        
        # Directory to store logs
        logs_path = self.create_directory(rf'{self.project_path}/logs') # store all the logs
        
        world_news_logs =  self.create_directory(rf'{logs_path}/world_news_logs')
        
        # create client_id directory
        id_log_path = self.create_directory(rf'{world_news_logs}/{self.client_id}')
        
        # inside world_news logs creating site directory
        log_path = self.create_directory(rf'{id_log_path}/{self.site}')
        
        return log_path
        
        
    def create_image_directories(self, project_path):
        
        self.project_path = project_path
        
        # create images folder if it does not exists
        image_directory = self.create_directory(rf'{self.project_path}/images')

        # creating year/month/day folder to store images
        for i in self.created_on.split('-'):
            image_directory = self.create_directory(image_directory + '/' +i)

        return image_directory
    
    
    def create_pdf_directories(self, project_path, site):
        
        self.site = site
        self.project_path = project_path

        # create pdf folder if it does not exists
        pdfs = self.create_directory(rf'{self.project_path}/pdfs')
        pdf_path = self.create_directory(rf'{pdfs}/{self.site}')
        
        return pdf_path
    
    
    def download_page(self, url):
    
        self.url = url
        
        try:
            r = requests.get(self.url, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch {self.url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch {self.url} Error code: {r.status_code}')
            else:
                r.encoding = r.apparent_encoding
                return str(r.text)
        except:
            return f'Unable to fetch {self.url} Unknown error\n'
            # print(f'Unable to fetch {self.url} Unknown error\n')
            
            
    def download_json(self, url):
    
        self.url = url
        
        try:
            r = requests.get(self.url, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch {self.url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch {self.url} Error code: {r.status_code}')
            else:
                r.encoding = r.apparent_encoding
                return r.json()
        except:
            return f'Unable to fetch {self.url} Unknown error\n'
            # print(f'Unable to fetch {self.url} Unknown error\n')
        
    
    def download_page_post(self, url, dic):
    
        self.url = url
        self.dic = dic
        
        try:
            r = requests.post(self.url, self.dic, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch {self.url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch {self.url} Error code: {r.status_code}')
            else:
                r.encoding = r.apparent_encoding
                return str(r.text)
        except:
            return f'Unable to fetch {self.url} Unknown error\n'
            # print(f'Unable to fetch {self.url} Unknown error\n')
            
    
    def download_json_post(self, url, dic):
    
        self.url = url
        self.dic = dic
        
        try:
            r = requests.post(self.url, self.dic, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch {self.url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch {self.url} Error code: {r.status_code}')
            else:
                r.encoding = r.apparent_encoding
                return r.json()
        except:
            return f'Unable to fetch {self.url} Unknown error\n'
            # print(f'Unable to fetch {self.url} Unknown error\n')
        
        
    def download_image(self, image_url, image_path):  # image_path = path/image.extension 
        
        self.image_url = image_url
        self.image_path = image_path
        
        time.sleep(random.randint(1,3))
        
        try:
            r = requests.get(self.image_url, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch image {self.image_url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch image {self.image_url} Error code: {r.status_code}')
            else:
                r = r.content
                with open(self.image_path, 'wb') as f:
                    f.write(r)
        except:
            return f'Unable to fetch image {self.image_url} Unknown error\n'
            # print(f'Unable to fetch image {self.image_url} Unknown error\n')
        
        
    def update_images(self, image_urls, image_directory, dic_obj, html_content, logger, domain):        
        
        self.image_urls = image_urls
        self.html_content  = html_content
        self.image_directory = image_directory
        self.logger = logger
        self.domain = domain
        
        unable_to_download_image = 0
        len_image_urls = len(self.image_urls)  
        images_path = []
        img_download_failed = 0

        # iterating through image_urls, downloading images and storing images_path
        for i in range(len_image_urls):         

            image_path = rf'{self.image_directory}/{dic_obj}_{i}.png'
            temp_img_url = self.image_urls[i]
            
            if self.domain not in self.image_urls[i]:
                temp_img_url = self.domain + self.image_urls[i]
                   
            # calling download_image function
            download_message = self.download_image(temp_img_url, image_path)

            # writing download_message with error code if error occurs.
            if download_message:
                unable_to_download_image += 1
                img_download_failed += 1
                self.html_content = self.html_content.replace(self.image_urls[i], '')
                self.logger.info(download_message)
                continue

            images_path.append(image_path)
            
            # replace image url with image path
            self.html_content = self.html_content.replace(self.image_urls[i], image_path)

        if img_download_failed != len_image_urls:
            # update images_path in database
            cl_data.update_one({'_id': ObjectId(dic_obj)},  {'$set': {"images_path": images_path}})
            cl_data.update_one({'_id': ObjectId(dic_obj)},  {'$set': {"html_content": self.html_content}})
        
        return unable_to_download_image
        
        
    def download_images_viedoes(self, image_urls, image_directory, dic_obj, html_content, logger, domain):        
        
        self.image_urls = image_urls
        self.html_content  = html_content
        self.image_directory = image_directory
        self.logger = logger
        self.domain = domain
        
        unable_to_download_image = 0
        len_image_urls = len(self.image_urls)  
        images_path = []
        img_download_failed = 0

        # iterating through image_urls, downloading images and storing images_path
        for i in range(len_image_urls):         

            image_path = rf'{self.image_directory}/{dic_obj}_{i}.png'
            temp_img_url = self.image_urls[i]
            
            if self.domain not in self.image_urls[i]:
                temp_img_url = self.domain + self.image_urls[i]
                   
            # calling download_image function
            download_message = self.download_image(temp_img_url, image_path)

            # writing download_message with error code if error occurs.
            if download_message:
                unable_to_download_image += 1
                img_download_failed += 1
                self.html_content = self.html_content.replace(self.image_urls[i], '')
                self.logger.info(download_message)
                continue

            images_path.append(image_path)
            
            # replace image url with image path
            self.html_content = self.html_content.replace(self.image_urls[i], image_path)

        if img_download_failed != len_image_urls:
            # update images_path in database
            cl_data.update_one({'_id': ObjectId(dic_obj)},  {'$set': {"images_path": images_path}})
            cl_data.update_one({'_id': ObjectId(dic_obj)},  {'$set': {"html_content": self.html_content}})
        
        return unable_to_download_image
        
    def download_pdf(self, pdf_url, pdf_path):  # pdf_path = path/pdf.extension 
        
        self.pdf_url = pdf_url
        self.pdf_path = pdf_path
        
#         try:
        r = requests.get(self.pdf_url, headers=self.headers, timeout=120)
        response_code = r.status_code
        if response_code != 200:
            return f'Unable to fetch pdf {self.pdf_url} Error code: {r.status_code}\n'
            # print(f'Unable to fetch pdf {self.pdf_url} Error code: {r.status_code}')
        else:
            r = r.content
            with open(self.pdf_path, 'wb') as f:
                f.write(r)
            return 'True'
#         except:
#             return f'Unable to fetch pdf {self.pdf_url} Unknown error\n'
#             # print(f'Unable to fetch pdf {self.pdf_url} Unknown error\n')
 
    def download_session_page(self, url, session_obj):

        self.url = url
        self.session_obj = session_obj

        try:
            r = self.session_obj.get(self.url, headers=self.headers, timeout=60)
            response_code = r.status_code
            if response_code != 200:
                return f'Unable to fetch {self.url} Error code: {r.status_code}\n'
                # print(f'Unable to fetch {self.url} Error code: {r.status_code}')
            else:
                r.encoding = r.apparent_encoding
                return str(r.text)
        except:
            return f'Unable to fetch {self.url} Unknown error\n'
            # print(f'Unable to fetch {self.url} Unknown error\n')