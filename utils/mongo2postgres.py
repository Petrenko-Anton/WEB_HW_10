import datetime
import db.connect
from db.models import session, Author, Quote, PQuote, PTag, PAuthor

import logging


logger = logging.getLogger("mongo2postgres")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)

author_id_mapping = {}
quote_id_mapping = {}
tag_id_mapping = {}
authors = Author.objects.all()
quotes = Quote.objects.all()

for author in authors:
    new_author = PAuthor(fullname=author.fullname, born_date=author.born_date.strftime("%B %d, %Y"),
                         born_location=author.born_location, description=author.description)
    session.add(new_author)
    logger.info(f"author {new_author.fullname} saved")
    session.flush()
    author_id_mapping[author.id] = new_author.id

for quote in quotes:
    for tag_name in quote.tags:
        if tag_name not in tag_id_mapping:
            new_tag = PTag(name=tag_name)
            session.add(new_tag)
            logger.info(f"tag {new_tag.name} saved")
            session.flush()
            tag_id_mapping[tag_name] = new_tag.id

for quote in quotes:
    new_quote = PQuote(quote=quote.quote, author_id=author_id_mapping[quote.author.id])
    for tag_name in quote.tags:
        new_quote.tags.append(session.query(PTag).filter_by(name=tag_name).first())
    session.add(new_quote)
    logger.info(f"quote {new_quote.quote} saved")
    session.flush()
    quote_id_mapping[quote.id] = new_quote.id

session.commit()
