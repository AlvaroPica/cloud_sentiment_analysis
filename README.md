# Text sentiment analysis on the Cloud

This respositoy explains with code and examples how to run a text sentiment analysis on any of the three main cloud analytics services providers and their differences. Small texts that could represent a tweet, a restaurante opinion or a movie reviews are analyzed on Amazon Web Services, Google Cloud Platform and Azure Portal.

Run:

    > python run.py --amazon
    > python run.py --azure
    > python run.py --google
    > python run.py --merge
    > python run.py --all

Each of the NLP Sentiment Analysis services provides a Score on the sentiment of the given text which ranges can vary according to the cloud provider:

- AMAZON: Categorical Score with categories POSITIVE; NEUTRAL AND NEGATIVE
- AZURE: Continous variable from 0 to 1, being 0 the most negative and 1 the most positve.
- GOOLE: Continous variable from -1 to 1, being -1 the most negative and 1 the most positive.

For each Cloud provider we will use python frameworks to call the Sentiment Analys services. Valid credentials will be needed to communicate with the provider. An example of these credentials are provided in this repository but none of them are anymore more valid. Instructions for generating the own credentials will be given in corresponding notebook.

The purpose of this reposity is merely educational with the intention of:

- Learn how to create an account and download valid credentials from each cloud provider.
- Learn how to connect with main cloud providers using Python frameworks.
- Execute some sentimental analysis to any of the cloud providers and gather their responses.
- Compare the difference between sentiment analysis accross the cloud providers.

Author:
Álvaro Picatoste Ruilope
Contact:
apicatoste@gmail.com
