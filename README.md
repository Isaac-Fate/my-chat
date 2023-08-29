# My Chatbot 🤖

This is an LLM chatbot equipped with domain-specific knowledge, 
leveraging document and vector databases. 
Users can configure the chatbot's profile to elicit more tailored responses.

## Environment

One can set up the Anaconda environment from the file `environment.yml`:

```sh
conda env create -f environment.yml
```

## Usages

To insert the notes, run the command-line script `insert_notes.py` I have built:

```sh
python insert_notes.py "<Directory holding the note files>"
```

For more help messages, type the command:

```sh
python insert_notes.py --help
```

This app is built with Streamlit.
Type the following command to run the app in the browser:

```sh
streamlit run app.py
```

## Demo: Chatbot as a Cook 👨🏻‍🍳

Imagine wanting to learn how to prepare specific dishes. 
I've discovered a fantastic collection of recipes written in Markdown 
from [this outstanding repository](https://github.com/jeffThompson/Recipes/tree/master).
(All recipes, formatted as Markdown files, are housed within the `recipes` directory of this project.)
Although the collection is vast, 
I prefer NOT to sift through each recipe manually. 
This chatbot offers a solution.

In this demonstration, the chatbot takes on the role of a chef well-versed in a myriad of recipes. 
I can effortlessly inquire about the preparation of any particular dish.

Click the screenshot below to watch a video demo:

[![Chatbot in the Role of a Cook](https://i9.ytimg.com/vi_webp/hCRuXA-vi-E/mq1.webp?sqp=CNCesacG-oaymwEmCMACELQB8quKqQMa8AEB-AG4CYAC0AWKAgwIABABGGUgZShlMA8=&rs=AOn4CLA6HDVEYjDewHfwNjIMuo76kYsU1g)](https://www.youtube.com/watch?v=hCRuXA-vi-E)
