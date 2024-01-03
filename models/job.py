from pydantic import BaseModel

class Job(BaseModel):
    title: str = ''
    link: str = ''
    description: str = ''
    icon: str = ''
    footer: str = ''
    channel_id: int = 0
