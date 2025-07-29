from sqlalchemy import ForeignKey
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column

class PKMSpecies(Base):
    __tablename__ = "pkmspecies"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    national_dex_number: Mapped[int] = mapped_column(unique=True)
    evolution_line_id: Mapped[int] = mapped_column(unique=True)
    name_es: Mapped[str]
    name_jp: Mapped[str]
    generation: Mapped[int]
    has_gender_differences: Mapped[bool]
    description: Mapped[str]
