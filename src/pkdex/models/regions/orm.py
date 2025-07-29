from ...db.session import Base
from sqlalchemy.orm import Mapped, mapped_column

class Regions(Base):
    __tablename__ = "regions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(unique=True)

