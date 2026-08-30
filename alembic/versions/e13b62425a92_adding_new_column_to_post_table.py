""" adding new column to post table .. 

Revision ID: e13b62425a92
Revises: 340ac8e26720
Create Date: 2026-08-26 11:06:17.191564

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e13b62425a92'
down_revision: Union[str, Sequence[str], None] = '340ac8e26720' # if we want to go down a step.. 
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts' , sa.Column('content' , sa.String() , nullable= False))
    
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts' , 'content')
    pass
