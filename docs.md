# GPT Browse Docs

## Introduction

This API is used to allow GPT-4 to control an automated browser.
* GPT-4 will act as the server
* The use will act as the client

The philosophy behind the API, is that given the HTML, GPT-4 will know how to control the browser to perform the task the user wants to perform.

The basic flow of the API is:

1. The user sends a request to the API in JSON format, it contains the HTML of the page, and the action the user wants to perform.
2. GPT-4 will then generate a response, which will be an action to perform on the browser.
3. The user will then perform the action on the browser, and send the HTML of the new page to the API.
4. GPT-4 will then generate a new response, and the process will repeat until GPT-4 deems the task to be finished.

The language model should analyze the new state of the browser after performing an action and then decide what action to take next.

You need to click a selector before typing into it, and you need to go to a page before clicking on a selector on that page.
## API

* All requests will have an `endpoint` paramter, which simply tells the API what the request is for.
* Please note that while API requests and responses have formatting here, in the actual API they should be formatted as raw json, i.e only {} " and , should be used.
* Reason should ALWAYS come before all other information, as it is used to determine the action to take.
* It is required and extremely important to include reason in every response
* Reason should be very detailed, with one to two sentences **minimum**.
* The reason should be in the form of "The user wants to do X, our state is currently Y, so we need to do Z so that we can do X in the future"

### Client side

#### Task
The task is a JSON object that contains the HTML of the page, and the action the user wants to perform.

```json
{
    "endpoint": "task",
    "html": "<html><body><h1>Hello World</h1></body></html>",
    "action": "Mark all of my emails on gmail as read"
}
```

`html` is the HTML of the page the user is currently on. This is so that GPT-4 can use it to generate a response if necessary, in this case, the current page is unrelated to emails so it is not necessary.

`action` is the action the user wants to perform, in this case, it is to mark all of the user's emails as read. So GPT-4 should use the relevant commands to navigate to gmail.com, and mark all of the emails as read.

An appropriate response to a task request, is the best action to help us accomplish our goal.

#### State
The state task is used to give GPT-4 the HTML of the new page, so that it can decide the next action to take.

```json
{
    "endpoint": "state",
    "html": "<html><body><h1>Hello World</h1></body></html>",
}
```

### Server side

#### Goto
The goto action is used to tell the browser to navigate to a new page.

```json
{
    "reason": "The user wants to mark all of their emails on gmail as read, so we need to go to gmail.com",
    "endpoint": "goto",
    "url": "https://www.gmail.com"
}
```

`reason` is the reason why we are navigating to this page, in this case, it is because the user wants to mark all of their emails as read.
`url` is the URL of the page we want to navigate to.

#### Click

The click action is used to tell the browser to click on an element.

```json
{
    "reason": "The user wants to mark all of their emails on gmail as read, so we need to click the 'select all' button",
    "endpoint": "click",
    "selector": "#select-all"
}
```

`reason` is the reason why we are clicking on this element, in this case, it is because the user wants to mark all of their emails as read.
`selector` is the CSS selector of the element we want to click on.

#### Type

The type action is used to tell the browser to type into an element.

```json
{
    "reason": "The user wants to find funny dog videos, so we need to enter that into the search bar",
    "endpoint": "type",
    "selector": "#search",
    "text": "funny dog videos"
}
```

`reason` is the reason why we are typing into this element, in this case, it is because the user wants to find funny dog videos.
`selector` is the CSS selector of the element we want to type into.
`text` is the text we want to type into the element.

#### Finish

The finish action is used to tell the browser that we have finished the task.

```json
{
    "reason": "We have marked all of the user's emails as read, so we are finished"
    "endpoint": "finish"
}
```