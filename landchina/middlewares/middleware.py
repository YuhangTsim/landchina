# encoding:utf-8ß
from random import *
from landchina.middlewares.user_agents import agents

class UserAgentMiddleware(object):
    '''换user-agent'''

    def process_request(self, request, spider):
        agent = choice(agents)
        request.headers["User-Agent"] = agent
