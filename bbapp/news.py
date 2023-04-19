import os
import re
import mrequests as requests

class News:
    
    def __init__(self, news_file):
        self.news=[]
        self.DEBUG=False
        self.news_fail_count=0
        self.news_file=news_file
        self.news_url="https://www.mlb.com/news/"
        if self.DEBUG:
            print(f"News File: {self.news_file}")
    
    def cleanup_news_files(self):
        if self.save_news_file():
            self.rm_old_news()
    
    def get_latest_news(self):
            if self.news:
                """ I. Articles are  in news[] """
                if self.news_file_is_current():
                    """ A. File date matches today's date """
                    print('News in news[] and file appears current') if self.DEBUG else None
                    return self.news
                else:
                    """ B. File date does not match today's date """
                    print('No news in news[]') if self.DEBUG else None
                    self.get_news_from_web()
                    self.news = self.get_news_from_file()
                    return self.news
            else:
                """ II. No Articles in news[] """
                if self.news_file_is_current():
                    """ A. File date matches today's date """
                    print('News file appears current ') if self.DEBUG else None
                    if self.len_news_file_is_non_zero():
                        """ 1. Articles in  News File """
                        print('News file is non zero') if self.DEBUG else None
                        self.news=self.get_news_from_file()
                        return self.news
                    else:
                        
                        """ 2. 0 Articles in  News File """
                        print('News file zero length') if self.DEBUG else None
                        self.get_news_from_web()
                        self.news = self.get_news_from_file()
                        return self.news
                else:
                    """ B. File date does not match today's date """
                    print('News file appears out of date or does not exist') if self.DEBUG else None
                    self.get_news_from_web()
                    self.news = self.get_news_from_file()
                    return self.news
        
    def get_news_from_file(self):
        print(f"Getting news from {self.news_file} as news file") if self.DEBUG else None
        try:
            with open(self.news_file) as fh:
                for line in fh:
                    story = re.search('data-headline="(.*?)"',line)
                    if story is not None:
                        self.news.append(story.group(1))
        except OSError as e:
            print(f"News Error {e}")
        else:
            print(f"news=[] len: {len(self.news)} stories") if self.DEBUG else None
            return self.news

    def get_news_from_web(self):
        
        def fail_news():
            self.news_fail_count+=1
            print(f"Request failed: {str(e)}, fail count: {self.news_fail_count}")
            if self.news_fail_count > 4:
                #d.crash_burn(f"Fatal NEWS Error: http code: {self.request.status_code}")
                print('crash burn')
                time.sleep(10)
                
        def msg(state):
            print(f"HTTP Request {state} -  http code: {self.request.status_code}")
                
        while True:
            try:
                print(f"Connecting to {self.news_url}")
                self.request = requests.get(self.news_url, headers={b"accept": b"text/html"})
            except OSError as e:
                fail_news()    
            else:
                if self.request.status_code != 200:
                    msg("Failed")
                    fail_news()
                else:
                    msg("Success")
                    self.cleanup_news_files()
                    break
            
    def len_news_file_is_non_zero(self):
        if os.stat(self.news_file)[6] == 0:
            return False
        return True
    
    def news_file_is_current(self):
        print(f"Checking {self.news_file} as news file") if self.DEBUG else None
        try:
            if os.stat(self.news_file):
                print(f"{os.stat(self.news_file)[6]/1024} k")
                print('News File Exists: OK')
                return True
        except OSError as e:
            print(f"{self.news_file} - Error: {e}")
            return False
                
        

    def rm_old_news(self):
        
        old_files = [ x for x in os.listdir('/') if 'news' in x and  self.news_file not in x ]
        print('old_files ',old_files)
        
        if len(old_files) > 0:
            for x in old_files:
                try:
                    os.unlink('/' + x)
                except OSError as e:
                    print(f"{x} - old news deletion Failed: {e}")
                else:
                    print(f"{x} - old news deleted OK")
                    
    def save_news_file(self):
        try:
            print(f"Trying to save news to {self.news_file}")
            self.request.save(self.news_file)
        except OSError:
            print(f"{self.news_file} - news save Failed: {e}")
            raise
        else:
            print(f"{self.news_file} - news saved OK")
            return True