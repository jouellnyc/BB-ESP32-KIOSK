import os
import re
import time
import urequests as requests

from .time_funcs import game_day_now_nult, yr, mt, dy, gm_dt, short_yr

class News:
    
    def __init__(self, data_dir=""):
        self.news = set()
        self.DEBUG = True
        self.news_fail_count = 0
        self.max_retries = 3
        self.retry_delay = 3
        self.data_dir = data_dir
        if data_dir:
            self.news_file = f"{data_dir}/news-{yr}-{mt}-{dy}.txt"
        else:
            self.news_file = f"news-{yr}-{mt}-{dy}.txt"
        self.news_url = "https://www.mlb.com/news/"
        self.request = None
        if self.DEBUG:
            print(f"News File: {self.news_file}")
    
    def cleanup_news_files(self):
        self.rm_old_news()
        self.save_news_file()
        
    
    def get_latest_news(self):
        
        if self.news:
            # Articles are in news[]
            
            if self.news_file_is_current():
                # File date matches today's date
                if self.DEBUG:
                    print('News in news[] and file appears current')
                pass
            else:
                # File date does not match today's date
                if self.DEBUG:
                    print('News in news[] and file is out of date')
                if self.get_news_from_web():
                    self.get_news_from_file()
        else:
            
            if self.DEBUG:
                print('No News in news[]')
            
            # No Articles in news[]
            if self.news_file_is_current():
                
                # File date matches today's date
                if self.DEBUG:
                    print('News file appears current')
                
                if self.is_news_file_non_empty():
                    
                    # Articles in News File
                    if self.DEBUG:
                        print('News file is non zero')
                    self.get_news_from_file()
                    
                else:
                    
                    # 0 Articles in News File
                    if self.DEBUG:
                        print('News file zero length')
                    if self.get_news_from_web():
                        self.get_news_from_file()
                    
            else:
                # File date does not match today's date
                if self.DEBUG:
                    print('News file appears out of date or does not exist')
                if self.get_news_from_web():
                    self.get_news_from_file()
        
        return self.news
                    
        
        
    def get_news_from_file(self):
        if self.DEBUG:
            print(f"Getting news from {self.news_file} as news file")
        try:
            with open(self.news_file) as fh:
                for line in fh:
                    story = re.search('data-headline="(.*?)"', line)
                    if story is not None:
                        self.news.add(story.group(1))
        except OSError as e:
            print(f"OS News Error reading file: {str(e)}")
            return False
        else:
            if self.DEBUG:
                print("news=[] len:", len(self.news), "stories")
                print("self.news", self.news)
            return True
            

    def get_news_from_web(self):
        
        def msg(state):
            print("HTTP Request", state, "- http code:", self.request.status_code)
            
        self.news_fail_count = 0  # Reset counter for each attempt
        
        while self.news_fail_count < self.max_retries:
            
            try:
                if self.DEBUG:
                    print("Connecting to", self.news_url)
                self.request = requests.get(self.news_url, headers={"accept": "text/html"})
            except OSError as e:
                print("Connection error:", str(e))
                self.news_fail_count += 1
                if self.news_fail_count < self.max_retries:
                    time.sleep(self.retry_delay)
            else:
                if self.request.status_code != 200:
                    msg("Failed")
                    self.news_fail_count += 1
                    if self.DEBUG:
                        print("HTTP Error:", self.request.status_code)
                    if self.news_fail_count < self.max_retries:
                        time.sleep(self.retry_delay)
                else:
                    msg("Success")
                    self.cleanup_news_files()
                    return True
        
        print("Too many errors - failed to get news from web")
        return False
            
                
    def is_news_file_non_empty(self):
        try:
            stat_result = os.stat(self.news_file)
            return stat_result[6] > 0  # st_size is index 6 in MicroPython
        except OSError:
            return False
    
    def news_file_is_current(self):
        if self.DEBUG:
            print("Checking", self.news_file, "as news file")
            print("news-" + str(game_day_now_nult) + ".txt vs", self.news_file)
        
        try:
            stat_info = os.stat(self.news_file)
            if self.DEBUG:
                print(str(stat_info[6]/1024) + " k")
                print('News File Exists: OK')
            
            expected_filename = "news-" + str(game_day_now_nult) + ".txt"
            
            # Extract filename from path
            if "/" in self.news_file:
                actual_filename = self.news_file.split("/")[-1]
            else:
                actual_filename = self.news_file
            
            if expected_filename == actual_filename:
                if self.DEBUG:
                    print(self.news_file, "is current")
                return True
            else:
                if self.DEBUG:
                    print(self.news_file, "is not current")
                return False
                
        except OSError as e:
            if self.DEBUG:
                print(self.news_file, "- Error:", e)
            return False
                
        

    def rm_old_news(self):
        
        try:
            all_files = os.listdir(self.data_dir if self.data_dir else ".")
            old_files = []
            for x in all_files:
                if x.startswith('news-') and x.endswith('.txt'):
                    old_files.append(x)
            
            if self.DEBUG:
                print('old_files', old_files)
            
            # Extract current filename
            if "/" in self.news_file:
                current_file = self.news_file.split("/")[-1]
            else:
                current_file = self.news_file
            
            for filename in old_files:
                if filename != current_file:  # Don't delete current file
                    if self.data_dir:
                        filepath = self.data_dir + "/" + filename
                    else:
                        filepath = filename
                    try:
                        os.remove(filepath)
                        if self.DEBUG:
                            print(filename, "- old news deleted OK")
                    except OSError as e:
                        print(filename, "- old news deletion Failed:", e)
                        
        except OSError as e:
            print("Error listing directory:", e)
                    
    def save_news_file(self):
        if self.request is None:
            print("No request object available to save")
            return False
            
        try:
            if self.DEBUG:
                print("Trying to save news to", self.news_file)
            
            # Save the content
            with open(self.news_file, 'w') as f:
                f.write(self.request.text)
                
        except OSError as e:
            print(self.news_file, "- news save Failed:", e)
            return False
        else:
            if self.DEBUG:
                print(self.news_file, "- news saved OK")
            return True