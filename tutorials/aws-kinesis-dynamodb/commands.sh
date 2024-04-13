pip install glassflow python-dotenv boto3 faker pandas

glassflow space create netflixmetrics

glassflow pipeline create analyzewatchfrequency —space-id={your_space_name} --function=transform.py