# GenAI-Powered New Relic APM Troubleshooting Assistant

A Retrieval-Augmented Generation (RAG) based GenAI assistant designed to help engineers troubleshoot common New Relic APM issues using a curated troubleshooting knowledge base.

## Project Overview

This project demonstrates how Generative AI and RAG can be used in an IT Operations and Application Performance Monitoring (APM) use case.

The assistant retrieves relevant information from a New Relic troubleshooting knowledge base and uses Google's Gemini model through the Google AI Studio API to generate contextual troubleshooting guidance.

The current version is a proof-of-concept and does not depend on live New Relic telemetry.

---

## Architecture

```text
                    User
                     |
                     v
              Streamlit Chat UI
                     |
                     v
                RAG Engine
                     |
          +----------+----------+
          |                     |
          v                     v
     ChromaDB              Gemini LLM
   Vector Database       Google AI Studio
          |                     |
          +----------+----------+
                     |
                     v
             Troubleshooting
                  Response
