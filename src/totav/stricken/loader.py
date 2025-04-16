from typing import Annotated, ClassVar
from pathlib import Path

import yaml
from sqlalchemy.orm import declared_attr

from totav.stricken.engine import with_session, create_db_and_tables
from totav.stricken.models import TOTAV_MODEL_REGISTRY


class FixtureLoader:

    def load(self, doc):
        with with_session() as session:
            model_name = doc.pop("model_name")
            model = TOTAV_MODEL_REGISTRY[model_name]
            model.load(doc, session)

def main(argv):

    create_db_and_tables()


    F = FixtureLoader()
    doc = yaml.safe_load(Path(argv[1]).read_text())
    F.load(doc)


if __name__ == "__main__":
    import sys
    main(sys.argv)