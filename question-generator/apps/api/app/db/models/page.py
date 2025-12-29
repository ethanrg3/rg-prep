from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.core import Base


class Page(Base):
    __tablename__ = "pages"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    page_number: Mapped[int] = mapped_column(Integer, index=True)
    text: Mapped[str] = mapped_column(String)
    source_pdf: Mapped[str] = mapped_column(String, index=True)
