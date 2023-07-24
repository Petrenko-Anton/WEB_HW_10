import datetime
import db.connection
from db.models import session, Author, Quote, PQuote, PTag, PAuthor
from sqlalchemy import select

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


def main():

    for author in authors:
        existing_author = session.execute(select(PAuthor).where(PAuthor.fullname == author.fullname)).scalar_one_or_none()
        if existing_author:
            author_id_mapping[author.id] = existing_author.id
        else:
            new_author = PAuthor(fullname=author.fullname, born_date=author.born_date.strftime("%B %d, %Y"),
                                 born_location=author.born_location, description=author.description)
            session.add(new_author)
            logger.info(f"author {new_author.fullname} saved")
            session.flush()
            author_id_mapping[author.id] = new_author.id

    for quote in quotes:
        # Перевірка чи існує цитата з таким текстом
        existing_quote = session.execute(select(PQuote).where(PQuote.quote == quote.quote)).scalar_one_or_none()
        if existing_quote:
            quote_id_mapping[quote.id] = existing_quote.id
        else:
            new_quote = PQuote(quote=quote.quote, author_id=author_id_mapping[quote.author.id])
            for tag_name in quote.tags:
                # Перевірка чи існує тег з таким name
                existing_tag = session.execute(select(PTag).where(PTag.name == tag_name)).scalar_one_or_none()
                if existing_tag:
                    new_quote.tags.append(existing_tag)
                else:
                    new_tag = PTag(name=tag_name)
                    session.add(new_tag)
                    logger.info(f"tag {new_tag.name} saved")
                    session.flush()
                    tag_id_mapping[tag_name] = new_tag.id
                    new_quote.tags.append(new_tag)
            session.add(new_quote)
            logger.info(f"quote {new_quote.quote} saved")
            session.flush()
            quote_id_mapping[quote.id] = new_quote.id

    session.commit()


if __name__ == "__main__":
    main()