from playwright.sync_api import sync_playwright
import openai
import json
import time

with open('docs.md') as f:
    docs = f.read()


class GPTBrowser:
    def __init__(self):
        playwright = sync_playwright().start()
        chromium = playwright.firefox  # or "firefox" or "webkit".
        browser = chromium.launch(headless=False)
        page = browser.new_page()
        self.page = page

        self.handlers = {
            'goto': self.goto,
            'click': self.click,
            'type': self.type,
        }


    def create_task(self, action):
        task = str({
            "endpoint": "task",
            "html": self.page.content(),
            "action": action
        })
        messages = [
            {
                "role": "system",
                "content": 'You are no longer chatGPT, you are the server running the API specified in this documnetation, your future responses will only be the corresponding response from this API, you should not give any of your own text, only that that is included in the API or you will break the program. Here is the documentation:' + docs
            },
            {
                "role": "user",
                "content": task
            }
        ]

        self.get_response(messages)

    def get_response(self, messages):
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo-16k', messages=messages)

        action = response['choices'][0]['message']['content']
        print(action)
        action = json.loads(action)
        messages.append(response['choices'][0]['message'])

        if action['endpoint'] == 'finish':
            return
        else:
            self.handlers[action['endpoint']](action)

        time.sleep(3) # give page time to load
        messages.append(self.get_state())
        self.get_response(messages)

    def get_state(self):
        state = str({
            'endpoint': 'state',
            'html': self.page.content()
        })

        return {
            "role": "user",
            "content": state
        }





    def goto(self, response):
        url = response['url']
        self.page.goto(url)

    def click(self, response):
        selector = response['selector'].strip().replace(':', '\\:')
        print(selector)
        self.page.click(selector)
        #self.page.evaluate(f"document.querySelector('{selector}').click()'")

    def type(self, response):
        selector = response['selector'].strip().replace(':', '\\:')
        text = response['text'].strip()

        #self.page.evaluate(f"document.querySelector('{selector}').value = '{text}'")
        self.page.type(selector, text)


g = GPTBrowser()

g.create_task(input('What task would you like the browser to perform?: '))