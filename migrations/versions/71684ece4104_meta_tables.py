"""Meta tables

Revision ID: 71684ece4104
Revises: 
Create Date: 2022-07-28 02:02:59.679093

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '71684ece4104'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('exercise', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('exercise', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('exercise', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('exercise', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('exercise_def', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('exercise_def', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('exercise_def', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('exercise_def', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('routine', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('routine', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('routine', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('routine', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('session', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('session', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('session', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('session', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('set', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('set', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('set', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('set', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('user', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.add_column('workout', sa.Column('deleted', sa.Boolean(), nullable=True))
    op.add_column('workout', sa.Column('deleted_date', sa.DateTime(), nullable=True))
    op.add_column('workout', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('workout', sa.Column('updated_at', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('workout', 'updated_at')
    op.drop_column('workout', 'created_at')
    op.drop_column('workout', 'deleted_date')
    op.drop_column('workout', 'deleted')
    op.drop_column('user', 'updated_at')
    op.drop_column('user', 'created_at')
    op.drop_column('user', 'deleted_date')
    op.drop_column('user', 'deleted')
    op.drop_column('set', 'updated_at')
    op.drop_column('set', 'created_at')
    op.drop_column('set', 'deleted_date')
    op.drop_column('set', 'deleted')
    op.drop_column('session', 'updated_at')
    op.drop_column('session', 'created_at')
    op.drop_column('session', 'deleted_date')
    op.drop_column('session', 'deleted')
    op.drop_column('routine', 'updated_at')
    op.drop_column('routine', 'created_at')
    op.drop_column('routine', 'deleted_date')
    op.drop_column('routine', 'deleted')
    op.drop_column('exercise_def', 'updated_at')
    op.drop_column('exercise_def', 'created_at')
    op.drop_column('exercise_def', 'deleted_date')
    op.drop_column('exercise_def', 'deleted')
    op.drop_column('exercise', 'updated_at')
    op.drop_column('exercise', 'created_at')
    op.drop_column('exercise', 'deleted_date')
    op.drop_column('exercise', 'deleted')
    # ### end Alembic commands ###
