# Conversational AI App

This project is a **Conversational AI** web application that uses OpenAI and Gemini APIs to generate responses to user input. The app selects the active language model (LLM) based on the environment configuration and falls back to Gemini AI in case of an error or if OpenAI is not available.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Error Handling](#error-handling)
- [Configuration](#configuration)
- [Environment Variables](#environment-variables)
- [License](#license)

## Overview

The application exposes a REST API to interact with AI models. It uses FastAPI to create the server, and integrates with the OpenAI and Gemini APIs for generating responses based on user queries. In case of failure with OpenAI, it automatically falls back to the Gemini API.

### Features:
- **OpenAI integration** for chat responses.
- **Gemini AI fallback** in case of OpenAI failure.
- **API error handling** for quota issues, unavailable services, and more.
- **Flexible configuration** to switch between OpenAI, Gemini, and other AI models.

## Getting Started

### Prerequisites

To get started with the app, you need to have the following installed:

- Python 3.x
- pip (Python package installer)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Kalyani694/Chat-with-AI.git
   cd conversational-ai-app
