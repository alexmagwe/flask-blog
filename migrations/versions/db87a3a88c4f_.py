"""empty message

Revision ID: db87a3a88c4f
Revises: 
Create Date: 2020-08-19 20:50:40.180300

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db87a3a88c4f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('posts',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.Text(), nullable=True),
    sa.Column('title', sa.String(length=100), nullable=True),
    sa.Column('stamp', sa.String(length=16), nullable=True),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('users_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['users_id'], ['users.id'], name=op.f('fk_posts_users_id_users')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_posts')),
    sa.UniqueConstraint('stamp', name=op.f('uq_posts_stamp'))
    )
    op.create_table('preview',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('caption', sa.String(length=100), nullable=True),
    sa.Column('img', sa.Text(), nullable=False),
    sa.Column('date_posted', sa.DateTime(), nullable=False),
    sa.Column('preview_of', sa.String(length=16), nullable=False),
    sa.ForeignKeyConstraint(['preview_of'], ['posts.stamp'], name=op.f('fk_preview_preview_of_posts')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_preview'))
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('preview')
    op.drop_table('posts')
    # ### end Alembic commands ###
