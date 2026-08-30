"""adding foreign key to 'post' table

Revision ID: b5af443ef5f4
Revises: 2440cf4bba66
Create Date: 2026-08-30 11:37:48.575102

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5af443ef5f4'
down_revision: Union[str, Sequence[str], None] = '2440cf4bba66'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts' , sa.Column('owner_id' , sa.Integer() , nullable= False))
    op.create_foreign_key('post_users_fk' , source_table= 'posts' , referent_table= 'users' , local_cols= ['owner_id'] , remote_cols= ['id'] , ondelete= "CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('post_users_fk' , 'posts' , type_='foreignkey')
    op.drop_column( 'posts' ,  'owner_id')
    pass
