# LangChain ReAct Agent Implementation

## Overview

This project implements the ReAct (Reasoning and Acting) framework for Large Language Models (LLMs), based on the research paper ["ReAct: Synergizing Reasoning and Acting in Language Models"](https://arxiv.org/abs/2210.03629) by Shunyu Yao et al.

### What is ReAct?

ReAct is a novel paradigm that synergizes reasoning and acting in language models. The framework combines:

- **Reasoning**: The model's ability to generate thoughts and explanations
- **Acting**: The model's capability to take actions based on those thoughts

The process follows this pattern:

1. **Thought**: The model reasons about the current situation
2. **Action**: The model decides on an action to take
3. **Observation**: The model observes the result of the action
4. **Thought**: The model reasons about the observation and decides next steps

This creates a powerful loop of reasoning and action that leads to more reliable and explainable outcomes.

## Implementation Details

This implementation uses LangChain to create a ReAct agent with the following components:

### Tools
The agent has access to custom tools including:
- `get_text_length`: A tool that returns the length of a text string in characters

### Key Components

1. **Agent Setup**:
   - Uses ChatOpenAI (GPT-4-mini) as the base LLM
   - Implements zero-temperature setting for deterministic outputs
   - Uses custom callback handler for monitoring agent's progress

2. **Prompt Template**:
   - Implements a chain-of-thought prompt template
   - Includes few-shot examples in the format:
     - Question
     - Thought
     - Action
     - Action Input
     - Observation
     - Final Answer

3. **Agent Execution Flow**:
   - Implements an iterative execution loop
   - Uses `ReActSingleInputOutputParser` for structured output parsing
   - Maintains intermediate steps for tracking agent's reasoning process

## Requirements

- Python 3.x
- LangChain
- OpenAI API key (set via environment variables)
- Python-dotenv for environment management

## Usage

1. Set up your environment variables:
   ```bash
   OPENAI_API_KEY=your_api_key_here
   ```

2. Run the main script:
   ```bash
   python main.py
   ```

The example implementation demonstrates the agent determining the length of the word 'DOG' in characters, showcasing the ReAct framework's reasoning and action capabilities.

## Project Structure

- `main.py`: Core implementation of the ReAct agent
- `callbacks.py`: Custom callback handler for agent monitoring
- `.env`: Environment variables configuration (not tracked in git)

## Future Improvements

- Add more custom tools to expand agent capabilities
- Implement more complex reasoning chains
- Add error handling and retry mechanisms
- Expand the example use cases

## Contributing

Feel free to submit issues and enhancement requests!
