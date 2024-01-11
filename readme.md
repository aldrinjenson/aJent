# aJent: AJ's smart agent :)

**aJent** is an intelligent personal assistant - designed to make you more productive by gathering data and automating the boring actions using just simple natural langage ✨

## Demo

https://github.com/aldrinjenson/aJent/assets/53407417/10a77f75-1700-4e69-9406-caead50e6dc2

Check: [Demo Video](./demo.mp4)

This project was made as a prototype to explore GPT agents.
Currently custom functions have been added to add and manipulate todo information.
The aJent will intelligently decide when to use what functionality - hence being a smart and powerful assistant!

## Features

- **Local File System Interaction:** Execute bash commands to interact with the local file system effortlessly.

- **Web Browsing Capability:** Retrieve relevant information from the internet whenever needed.

- **Smart decision making:** aJent will intelligently decide when to use and call what tool to perform the action correctly.

- **Local Machine Actions:** Perform various actions on your local machine directly through aJent.

- **Wikipedia based Q&A Answering:** Retrieve relevant information from wikipedia whenever needed.

- **Conversational Memory:** Remember past interactions with aJent, allowing for a more personalized experience.

- **Custom GPT Functionality:** Utilize openAI based functions to add even more custom functionalities to add more custom actions like managing todos.


## Technologies Used

- **LangChain:** for LLM orchestration
- **Streamlit:** Building the user interface for aJent's seamless interaction.
- **OpenAI:** Currently it's based on OpenAI API since it uses function calling. But this can be easily swapped with most popular LLMs

## Installation

1. Clone the repository: `git clone https://github.com/aldrinjenson/aJent.git`
2. Navigate to the project directory: `cd aJent`
3. Copy the `.env.example` file to `.env`: `cp .env.example .env`
4. Open the `.env` file and add your OpenAI key.
5. Run the application: `streamlit run app.py`

## How to Use

- Start aJent by running the Streamlit app.
- Input your commands using natural language.
- Enjoy the power of aJent in performing a variety of tasks.

## Contributions

Contributions are welcome! Feel free to fork the repository and submit pull requests.

---

_What a time to be alive!_
