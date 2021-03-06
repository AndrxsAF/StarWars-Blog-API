"""empty message

Revision ID: 41f859d74004
Revises: 
Create Date: 2022-02-09 01:10:31.836520

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '41f859d74004'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('planetID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('terrain', sa.String(length=100), nullable=True),
    sa.Column('population', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('planetID')
    )
    op.create_table('user',
    sa.Column('userID', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('userID'),
    sa.UniqueConstraint('username'),
    sa.UniqueConstraint('username')
    )
    op.create_table('people',
    sa.Column('peopleID', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('height', sa.Integer(), nullable=True),
    sa.Column('mass', sa.Integer(), nullable=True),
    sa.Column('homeworld', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['homeworld'], ['planet.planetID'], ),
    sa.PrimaryKeyConstraint('peopleID')
    )
    op.create_table('favorite',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('userID', sa.Integer(), nullable=True),
    sa.Column('planetID', sa.Integer(), nullable=True),
    sa.Column('peopleID', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['peopleID'], ['people.peopleID'], ),
    sa.ForeignKeyConstraint(['planetID'], ['planet.planetID'], ),
    sa.ForeignKeyConstraint(['userID'], ['user.userID'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('favorite')
    op.drop_table('people')
    op.drop_table('user')
    op.drop_table('planet')
    # ### end Alembic commands ###
