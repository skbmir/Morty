import os
import time
import random
import re
from slackclient import SlackClient

class Morty():

    def __init__(self, token):
        self.token = token
        self.id = -1
        self.name = 'Morty'
        self._client = SlackClient(self.token)
    
    def connect(self):
        if self._client.rtm_connect(with_team_state=False):
            print('Morty connected.')

            self._query_id()
            print('My Slack id is: {}.'.format(self.id))

            return True
        else:
            print('Connection failed.')
            return False
        
    def main_loop(self):
        while True:
            command, channel = self._handle_events(self._client.rtm_read())

            if command:
                self._handle_commands(command, channel)
            
            time.sleep(0.5)

    def _query_id(self):
        self.id = self._client.api_call('auth.test')['user_id']
    
    def _handle_events(self, events):
        if len(events) > 0:
            for event in events:
                if event['type'] == 'message' and not 'subtype' in event:
                    user_id, message = self._get_mention(event['text'])

                    if user_id == self.id:
                        return message, event['channel']
        return None, None
    
    def _get_mention(self, msg):
        matches = re.search('^<@(.+)>.(.*)', msg)
        return (matches.group(1), matches.group(2).strip()) if matches else (None, None)
    
    def _handle_commands(self, cmd, chnl):
        def_msgs = [
            'хз че это. ¯\_(ツ)_/¯',
            '╮ (. ❛ ᴗ ❛.) ╭',
            '(・_・ヾ'
        ]

        response = None

        if cmd.startswith('/test'):
            response = 'tested. ヘ( ^o^)ノ＼(^_^ )'
        elif cmd.startswith('/help'):
            response = ''' Help:
            /help - эта справка
            /test - test bot
            привет - приветствие
            остальное - ему не понятно
            '''
        elif cmd.startswith('привет') or cmd.startswith('Привет'):
            response = 'Хуй тебе в ответ.'
        else:
            response = random.choice(def_msgs)
        
        self._client.api_call(
            'chat.postMessage',
            channel=chnl,
            text=response
        )
