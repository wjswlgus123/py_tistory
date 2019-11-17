import requests
import re
import json

class Tistory():
    def __init__(self, m_client_id, m_redirect_uri, m_user_id, m_password, m_blogname):
        self.m_client_id = m_client_id
        self.m_redirect_uri = m_redirect_uri
        self.m_user_id = m_user_id
        self.m_password = m_password
        self.m_blogname = m_blogname
        self.m_access_token = self.getAccessToken()
        pass
    def getAccessToken(self,):
        print('Start getAccessToken')
        # TODO: To get Access token
        URL_0 = 'https://www.tistory.com/auth/login'
        URL_1 = 'https://www.tistory.com/oauth/authorize'
        loginParams = {
            'redirectUrl':self.m_redirect_uri,
            'loginId':self.m_user_id,
            'password':self.m_password,
            'fp' : 'mymackbook',
            }
        tokenParams = {
            'client_id':self.m_client_id,
            'redirect_uri':self.m_redirect_uri,
            'response_type':'token'
            }
        headers = {
            'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko'
        }
        rs = requests.session()
        r0 = rs.get(URL_1, params=tokenParams)
        #print(r0.url)
        r1 = rs.post(URL_0, headers=headers, data=loginParams)
        r2 = rs.get(URL_1, params=tokenParams)
        #print(r2.url)
        if r0.url == r2.url:
            print('please confirm the email and try again')
            return None
        else:
            match = re.match('(.*?)access_token=(?P<access_token>.*?)&state=', r2.url)
            gd = match.groupdict()
            access_token = gd['access_token']
            print('access_token: '+access_token)
            return access_token
    def getList(self,m_page_num):
        print("Start getList")
        # TODO: 글 목록
        url = "https://www.tistory.com/apis/post/list?access_token="+self.m_access_token+"&output=json"+"&blogName="+self.m_blogname+"&page="+str(m_page_num)
        #print(url)
        rd = requests.get(url)
        #print(rd.text)
        try:
            item = json.loads(rd.text)
            # print(item["tistory"]["status"])
            # print(item["tistory"]["item"])
            # print(item)
            return item
        except:
            print("Fail")
            return False
    def getPublishedPosts(self):
        m_published_posts = []
        print("Start getPublishedPosts")
        i =1
        while i:
            #print("I'm in while")
            item = self.getList(i)
            if str(item).find("posts") != -1:
                posts = item["tistory"]["item"]["posts"]
                #print("Start Print Posts")
                #print(posts)
                for post in posts:
                    m_visibility = str(post.get("visibility"))
                    if m_visibility == "20":
                        #print("published")
                        #print(post)
                        m_published_posts.append(post)
            else:
              return m_published_posts
            i = i+1

    def getRead():
        # TODO: 글 읽기
        return
    def writePost(self, m_title, m_content, m_category, m_tag):
        print("Start writePost")
        # TODO: 글쓰기
        # blogName: Blog Name (필수)
        # title: 글 제목 (필수)
        # content: 글 내용
        # visibility: 발행상태 (0: 비공개 - 기본값, 1: 보호, 3: 발행)
        # category: 카테고리 아이디 (기본값: 0)
        # published: 발행시간 (TIMESTAMP 이며 미래의 시간을 넣을 경우 예약. 기본값: 현재시간)
        # slogan: 문자 주소
        # tag: 태그 (',' 로 구분)
        # acceptComment: 댓글 허용 (0, 1 - 기본값)
        # password: 보호글 비밀번호
        params = {
            'blogName' : self.m_blogname,
            'title' : m_title,
            'content' : m_content,
            'tag' : m_tag,
            'category' : m_category,
            'visibility' : '0',
            #'published' : '',
            #'slogan' : '',
            #'acceptComment' : '1',
            #'password' : '',
            'access_token' : self.getAccessToken(),
            'output' : 'json'
        }
        data = json.dumps(params)
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        rd = requests.post('https://www.tistory.com/apis/post/write', data=data, headers=headers)
        if rd.status_code == 200:
            return True
        else:
            print(rd.status_code)
            print(rd.text)
            item = json.loads(rd.text)
            print(rd.status_code)
            print(item["tistory"]["error_message"])
            return False
    def modifyPost():
        # TODO: 글수정
        return
    def attach(self, m_imgname):
        # TODO: 파일첨부
        print("Start attach")
        m_filepath = './img/'+m_imgname
        files = {'uploadedfile': open(m_filepath, 'rb')}
        params = {'access_token': self.getAccessToken(), 'targetUrl':self.m_blogname, 'output':'json'}
        rd = requests.post('https://www.tistory.com/apis/post/attach', params=params, files=files)
        try:
            item = json.loads(rd.text)
            print(item["tistory"]["replacer"])
            print(item["tistory"]["url"])
            os.remove(m_filepath)
            return(item["tistory"]["replacer"])
        except:
            print("Success")
        return item["tistory"]["replacer"]
    def getCategoryList():
        # TODO: 카테고리 리스트
        return
    def getNewestComment():
        # TODO: 최근 댓글 목록 가져오기
        return
    def getCommnetList():
        # TODO:  댓글 목록
        return
    def writeCommnet():
        # TODO: 댓글 작성
        return
    def modifyCommnet():
        # TODO: 댓글 수정
        return
    def delComment():
        # TODO: 댓글 삭제
        return
