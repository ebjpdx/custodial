from sqlalchemy import Table, Column, Integer, String, Date, MetaData

metadata = MetaData()

bookmarks = Table('bookmarks', metadata,
                  Column('id', Integer, primary_key=True),
                  Column('url', String, nullable=False),
                  Column('first_week_observed', Date),
                  Column('latest_week_observed', Date),
                  Column('weeks_observed', Integer)
                  )

bookmark_exclusions = Table('bookmark_exclusions', metadata,
                            Column('url_pattern', String, primary_key=True),
                            Column('pattern_type', String, nullable=False)
                            )
