import requests
from typing import Optional, List

class User:
    def __init__(
        self,
        username: str = "",
        host: str = "",
        summary: Optional[str] = None,
        icon_url: Optional[str] = None,
        outbox_url: Optional[str] = None,
    ):
        self.username = username
        self.host = host
        self.summary = summary
        self.icon_url = icon_url
        self.outbox_url = outbox_url
    
    def fetch_outbox_post(self) -> List['Post']:
        if not self.outbox_url:
            raise ValueError(f'outbox url of @{self.username}@{self.host} is not defined')
        
        res_outbox = requests.get(self.outbox_url)
        if not res_outbox.ok:
            raise LookupError(f'{self.outbox_url}: [{res_outbox.status_code}] {res_outbox.reason}')

        res_outbox_first = requests.get(res_outbox.json()['first'])
        if not res_outbox.ok:
            raise LookupError(f'{res_outbox.json()["first"]}: [{res_outbox.status_code}] {res_outbox.reason}')
        
        outbox_items = res_outbox_first.json()
        posts: List['Post'] = []
        for obj in outbox_items['orderedItems']:
            if obj['type'] != 'Create':
                continue
            posts.append(Post.parse(obj))
        
        return posts
            
    @staticmethod
    def parse(username, host, obj):
        '''Parse application/activity+json and return new User'''
        return User(
            username=username,
            host=host,
            summary=obj.get('name'),
            icon_url=obj.get('icon', {'url': None})['url'],
            outbox_url=obj['outbox']
        )

class Post:
    def __init__(
        self,
        id: str,
        actor: str,
        published: str,
        attachment: List[str] = [],
        summary: Optional[str] = None,
        content: Optional[str] = None,
        inReplyTo: Optional[str] = None,
    ):
        if attachment is None:
            attachment = []
        
        self.id = id
        self.actor = actor
        self.published = published
        self.attachment = attachment
        self.summary = summary
        self.content = content
        self.inReplyTo = inReplyTo

    def __str__(self):
        return f'Post(id={self.id}, actor={self.actor}, published={self.published}, summary={self.summary})'
        

    @staticmethod
    def parse(obj: dict):
        '''Parse application/activity+json and return new Post'''
        return Post(
            id=obj['id'],
            actor=obj['actor'],
            published=obj['published'],
            attachment=obj['object'].get('attachment', []),
            summary=obj['object'].get('summary', None),
            content=obj['object'].get('content'),
            inReplyTo=obj['object'].get('inReplyTo'),
        )