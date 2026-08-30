"""adding remaining columns of post table to it .. 

Revision ID: b10a5d7ef227
Revises: b5af443ef5f4
Create Date: 2026-08-30 11:45:52.820719

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b10a5d7ef227'
down_revision: Union[str, Sequence[str], None] = 'b5af443ef5f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts' , sa.Column('published' , sa.Boolean() , nullable=False , server_default = 'True') )
    op.add_column('posts' , sa.Column('created_at' , sa.TIMESTAMP(timezone=True) , nullable=False , server_default = sa.text('NOW()')))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts' , 'published' ) 
    op.drop_column('posts', 'created_at')
    pass
