from sqlalchemy import ForeignKey
from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column

class PKMForms(Base):
    __tablename__ = "pkmforms"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    species_id: Mapped[int] = mapped_column(ForeignKey("pkmspecies.id", ondelete="CASCADE"), nullable=False)
    type1_id: Mapped[int] = mapped_column(ForeignKey("types.id", ondelete="RESTRICT"), nullable=False)
    type2_id: Mapped[int] = mapped_column(ForeignKey("types.id", ondelete="RESTRICT"), nullable=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("regions.id", ondelete="RESTRICT"), nullable=False)
    can_gigantamax: Mapped[bool] = mapped_column(default=False, nullable=False)
    can_mega: Mapped[bool] = mapped_column(default=False, nullable=False)
    is_default: Mapped[bool] = mapped_column(default=False, nullable=False)
